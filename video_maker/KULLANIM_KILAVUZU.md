# 🦉 BeastTales Video Maker — Kullanım Kılavuzu

Görsellerini + seslendirmeni otomatik olarak birleştirip
Full HD (1920×1080) YouTube videosu oluşturan uygulama.

---

## Gereksinimler

- **Python 3.10 veya üzeri** — [indir](https://www.python.org/downloads/)
- Windows 10/11 veya macOS 12+
- En az 4 GB RAM

---

## İlk Kurulum (Sadece 1 kez yapılır)

### Windows
1. `video_maker` klasörünü aç
2. `kur_ve_calistir_WINDOWS.bat` dosyasına **çift tıkla**
3. Siyah pencere açılır, kütüphaneler kurulur (2-3 dk)
4. Tarayıcıda uygulama otomatik açılır

### Mac
1. Terminal'i aç
2. Şu komutu yaz:
```
cd Desktop/youtube/video_maker
chmod +x kur_ve_calistir_MAC.sh
./kur_ve_calistir_MAC.sh
```

---

## Sonraki Kullanımlar

Kurulum bitti mi? Artık sadece BAT dosyasına çift tıkla.
Tarayıcı otomatik açılır.

---

## Nasıl Kullanılır

### Adım 1 — Görsel Hazırlığı
- Ideogram veya Leonardo'dan görselleri indir
- Dosyaları **sıralı şekilde adlandır:**
  - `001.jpg`, `002.jpg`, `003.jpg`, ...
  - veya `a.jpg`, `b.jpg`, `c.jpg`
- **Kaç görsel hazırlamalısın?**

| Video Süresi | Görsel Sayısı |
|-------------|---------------|
| 10 dakika   | ~90 görsel    |
| 12 dakika   | ~108 görsel   |
| 13 dakika   | ~117 görsel   |
| 14 dakika   | ~126 görsel   |
| 15 dakika   | ~135 görsel   |

### Adım 2 — Ses Hazırlığı
- Minimax.io'dan seslendirmeyi MP3 olarak indir
- Bir adet tek dosya olmalı (tam video sesi)

### Adım 3 — Uygulamayı Kullan
1. Tarayıcıda uygulamayı aç
2. **"Görselleri Seç"** bölümünde tüm görsel dosyalarını seç
3. **"Seslendirmeyi Seç"** bölümünde MP3 dosyasını seç
4. Geçiş süresini ayarla (önerilen: 0.4 saniye)
5. **"Video Oluştur"** butonuna bas
6. Bekleme süresi: ~10-20 dakika (görsel sayısına göre)
7. **"MP4 İndir"** butonuyla videoyu kaydet

---

## Üretim Akışı (Tam Pipeline)

```
Claude
  └─ Script yaz (Part 1)
  └─ Görsel promptları üret (Part 2)
       │
       ▼
Ideogram / Leonardo
  └─ Görselleri üret
  └─ 001.jpg, 002.jpg... diye sırala
       │
       ▼
Minimax.io
  └─ İngilizce seslendirme üret
  └─ MP3 olarak indir
       │
       ▼
BeastTales Video Maker (bu uygulama)
  └─ Görseller + ses → Full HD MP4
       │
       ▼
CapCut (isteğe bağlı son dokunuşlar)
  └─ Renkli altyazı ekle
  └─ Intro/outro ekle
  └─ Müzik ekle (arka plan)
       │
       ▼
YouTube'a Yükle
```

---

## Sık Sorulan Sorular

**S: Görsel sayısı ile ses uyuşmazsa ne olur?**
C: Uygulama sesi eşit böler. 100 görsel varsa her biri
   ses süresinin 1/100'ü kadar ekranda durur.

**S: Hangi görsel formatları destekleniyor?**
C: JPG, JPEG, PNG, WEBP

**S: Video çok yavaş oluşuyor?**
C: Normal, moviepy CPU kullanır. 120 görsel için 10-20 dk bekle.

**S: Hata alıyorum?**
C: Bozuk görsel dosyası olabilir. Görsellerin tamamen
   indirildiğinden emin ol.

---

*BeastTales Video Maker — Otomatik YouTube Video Üretim Sistemi*
