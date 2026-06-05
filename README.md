 TextRevive: OCR ve NLP Destekli Tarihi Metin Restorasyonu
Bu proje, fiziksel deformasyona (silinme, yıpranma, lekelenme) uğramış tarihi ve epigrafik metinlerin onarım sürecindeki manuel ve sübjektif insan tahminlerini ortadan kaldırmak amacıyla geliştirilmiş uçtan uca bir yapay zeka sistemidir.

 Projenin Amacı ve Çözdüğü Problem
Mevcut Optik Karakter Tanıma (OCR) teknolojileri, hasarlı belgelerde yüksek oranda hata üretmekte ve anlamsız karakter dizileri oluşturmaktadır. TextRevive, OCR'ın yarattığı bu "kirli çıktıyı" girdi olarak alıp, anlamsal bir süzgeçten geçirerek (Post-OCR Correction) onarır. Klasik kelime tamamlama araçlarından farklı olarak, sadece sözlük yapısına değil; kelimenin tarihsel bağlamına ve cümlenin istatistiksel olasılığına odaklanır.

 Temel Özellikler:
Görüntü İşleme Entegrasyonu: EasyOCR ile yüklenen belge üzerindeki silik kısımlar tespit edilir ve okuma güveni düşük olan bölgeler otomatik olarak [MASK] etiketiyle işaretlenir.

Bağlam Farkındalıklı Onarım: Çift yönlü (Bidirectional) Maskeli Dil Modelleri kullanılarak boşluklar cümlenin gidişatına en uygun şekilde doldurulur.

Çift Dilli Mimari: Türkçe (Osmanlı/Türkiye Tarihi) ve İngilizce (Antik Roma Tarihi) olmak üzere spesifik veri setleriyle eğitilmiş iki ayrı model barındırır.

Şeffaf Analiz Paneli: Araştırmacılara sadece tek bir kelime dayatmaz; en yüksek olasılıklı 5 alternatifi matematiksel güven skorlarıyla birlikte sunar.

 Doğruluk Metrikleri (Accuracy Metrics)
Sistemimiz uçtan uca iki aşamalı bir metrik değerlendirmesi yapmaktadır:

OCR Doğruluk Metriği: EasyOCR motorunun okuma güven skoru (Confidence Score) %50'nin altında olan her bölge, algoritma tarafından hasarlı kabul edilerek otomatik maskelenir.

Dil Modeli Doğruluk Metriği: Transformer mimarisinin [MASK] alanlarına atadığı kelimeler, çıkış katmanındaki (output layer) Softmax fonksiyonundan elde edilen olasılık yüzdeleriyle ölçülür. Düşük güven skorları (%15 altı) arayüzde özel olarak işaretlenerek "Güvenli Yapay Zeka" (Trustworthy AI) prensibi sağlanır.

 Kurulum ve Çalıştırma

 ⚠️ Önemli Not (Model Dosyaları):
GitHub'ın 100 MB dosya sınırı nedeniyle, eğitilmiş yapay zeka modelleri (textrevive_tam_model ve textrevive_tr_model) repoya yüklenememiştir. Projeyi çalıştırmadan önce lütfen modelleri indirin ve projenin ana dizinine klasör olarak çıkartın.
Model 1: https://drive.google.com/file/d/1gbNDPr3lS8Y4ahv8gjPiBD-Q4lZi0FKi/view?usp=sharing

Model 2: https://drive.google.com/file/d/15fJS2j-juLxgqw2TTdjM7tkWdcw_RCgx/view?usp=sharing

1. Gereksinimleri Yükleyin:
Projeyi klonladıktan sonra terminal veya komut satırınızda dizin içerisine girerek şu komutu çalıştırın:
pip install -r requirements.txt

2. Uygulamayı Başlatın:
Terminal üzerinden şu komutla arayüzü ayağa kaldırın:
streamlit run app.py

(Not: Kullanılan dil modellerinin dosya boyutları yüksek olduğundan, textrevive_tam_model ve textrevive_tr_model klasörlerinin projenin ana dizininde bulunduğundan emin olun.)

 Kullanılan Teknolojiler
Arayüz: Streamlit

Doğal Dil İşleme (NLP): Hugging Face Transformers, PyTorch

Görüntü İşleme (OCR): EasyOCR, OpenCV, NumPy

Görüntü Yönetimi: Pillow (PIL)
