import streamlit as st
from transformers import pipeline
import easyocr
from PIL import Image
import numpy as np
import re

st.set_page_config(page_title="TextRevive", page_icon="📜", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { min-width: 260px; max-width: 260px; }
        .stButton>button { width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    dil_secimi = st.radio("📚 Dil ve Tarihi Dönem:", ("Türkçe (Osmanlı/Türkiye Tarihi)", "İngilizce (Antik Roma Tarihi)"))
    st.markdown("---")

st.title("📜 TextRevive")
st.subheader("Hasarlı belgeleri yükleyin veya yazın, yapay zeka ile otomatik onarın.")

@st.cache_resource
def load_nlp_model(secilen_dil):
    if "İngilizce" in secilen_dil:
        return pipeline('fill-mask', model='./textrevive_tam_model', tokenizer='./textrevive_tam_model')
    else:
        return pipeline('fill-mask', model='./textrevive_tr_model', tokenizer='./textrevive_tr_model')

@st.cache_resource
def load_ocr_model(secilen_dil):
    lang_list = ['en'] if "İngilizce" in secilen_dil else ['tr']
    return easyocr.Reader(lang_list, gpu=False)

unmasker = load_nlp_model(dil_secimi)
reader = load_ocr_model(dil_secimi)

uploaded_file = st.file_uploader("📸 Hasarlı Belgenin Fotoğrafını Yükleyin (JPG, PNG)", type=["png", "jpg", "jpeg"])
input_text = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Belge", width=400)
    
    with st.spinner("Görüntü işleniyor ve hasarlı bölgeler tespit ediliyor..."):
        img_array = np.array(image)
        ocr_results = reader.readtext(img_array)
        
        olusturulan_metin = []
        for (bbox, text, prob) in ocr_results:
            if prob < 0.50 or re.search(r'[^a-zA-ZğüşıöçĞÜŞİÖÇ\s.,]', text):
                olusturulan_metin.append("[MASK]")
            else:
                olusturulan_metin.append(text)
        
        input_text = " ".join(olusturulan_metin)
        st.warning(f"**OCR Tarafından Tespit Edilen Hasarlı Metin:** {input_text}")

final_input = st.text_area("Düzenlenecek Metin (Manuel olarak [MASK] ekleyebilirsiniz):", value=input_text, height=150)

if st.button("🚀 Restorasyonu Başlat", type="primary"):
    if "[MASK]" not in final_input:
        st.error("Lütfen onarılacak yerleri belirtmek için metne en az bir tane `[MASK]` ekleyin.")
    else:
        with st.spinner("Tarihi arşivler taranıyor..."):
            results = unmasker(final_input)
            st.markdown("### ✨ Restore Edilmiş Metin")
            restored_text = final_input
            
            if isinstance(results[0], list):
                for mask_sonuclari in results:
                    best = mask_sonuclari[0]['token_str']
                    restored_text = restored_text.replace("[MASK]", f"<span style='color:#15803d; font-weight:bold; background-color:#dcfce7; padding: 2px 6px; border-radius: 4px;'>{best.upper()}</span>", 1)
                
                st.markdown(f"<div style='background-color: #f0fdf4; padding: 15px; border-radius: 8px; border: 1px solid #bbf7d0;'>✅ {restored_text}</div>", unsafe_allow_html=True)
                st.write("")
                
                with st.expander("📊 Detaylı Yapay Zeka Analizi ve Alternatifleri Gör"):
                    st.write("**En Yüksek Olasılıklı 5 Öneri ve Güven Skorları:**")
                    
                    for i, mask_sonuclari in enumerate(results):
                        st.write(f"**🔍 {i+1}. Boşluk Alternatifleri**")
                        for res in mask_sonuclari[:5]: 
                            col1, col2 = st.columns([1, 4])
                            col1.code(f"{res['token_str'].upper()}")
                            if res['score'] < 0.15:
                                col2.progress(res['score'], text=f"⚠️ Düşük Güven: %{res['score']*100:.2f}")
                            else:
                                col2.progress(res['score'], text=f"Güven Skoru: %{res['score']*100:.2f}")
                        st.divider()
            
            else:
                best = results[0]['token_str']
                restored_text = restored_text.replace("[MASK]", f"<span style='color:#15803d; font-weight:bold; background-color:#dcfce7; padding: 2px 6px; border-radius: 4px;'>{best.upper()}</span>")
                
                st.markdown(f"<div style='background-color: #f0fdf4; padding: 15px; border-radius: 8px; border: 1px solid #bbf7d0;'>✅ {restored_text}</div>", unsafe_allow_html=True)
                st.write("")
                
                with st.expander("📊 Detaylı Yapay Zeka Analizi ve Alternatifleri Gör"):
                    st.write("**En Yüksek Olasılıklı 5 Öneri ve Güven Skorları:**")
                    for res in results[:5]: 
                        col1, col2 = st.columns([1, 4])
                        col1.code(f"{res['token_str'].upper()}")
                        if res['score'] < 0.15:
                            col2.progress(res['score'], text=f"⚠️ Düşük Güven: %{res['score']*100:.2f}")
                        else:
                            col2.progress(res['score'], text=f"Güven Skoru: %{res['score']*100:.2f}")