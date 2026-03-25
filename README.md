# YouTube Buyume Asistani - @hillmotivasyon

Kisisel Gelisim ve Finans/Yatirim nisi icin ozel YouTube kanal buyutme araci.
Global trendleri analiz eder, rakip kanallari kesfeder ve viral video fikirleri uretir.

## Ozellikler

- **Trend Analizi**: Global YouTube trendlerini toplar ve analiz eder (Hindi icerik otomatik filtrelenir)
- **Video Fikri Uretici**: Trendlerden, kendi videolarinizdan ve rakiplerden fikir uretir
- **Kanal Kesfi**: Nisinize uygun global kanallari otomatik kesfeder
- **Rakip Analizi**: Benzer kanallari bulur ve basarili videolarini analiz eder
- **Otomatik Veri Toplama**: Her gun sabah 08:00'de trend toplar, her Pazartesi kanal kesfeder
- **Dashboard**: Tum verileri tek ekranda gormenizi saglar

## Kurulum

### 1. YouTube Data API Anahtari Alma (Ucretsiz)

1. [Google Cloud Console](https://console.cloud.google.com/) adresine gidin
2. Yeni bir proje olusturun (ornegin "YouTube Growth")
3. Sol menudan **APIs & Services > Library** secin
4. **YouTube Data API v3** arayin ve **Enable** tiklayin
5. Sol menudan **APIs & Services > Credentials** secin
6. **+ CREATE CREDENTIALS > API Key** tiklayin
7. Olusturulan anahtari kopyalayin

### 2. Projeyi Kurun

```bash
# Repoyu klonlayin
git clone <repo-url>
cd youtube

# Bagimliliklari yukleyin
npm install

# .env dosyasini olusturun
cp .env.example .env

# .env dosyasina API anahtarinizi yazin
# YOUTUBE_API_KEY=sizin_anahtar_buraya
```

### 3. Uygulamayi Baslatın

```bash
# Normal mod
npm start

# Gelistirme modu (otomatik yeniden baslama)
npm run dev
```

Tarayicinizda `http://localhost:3000` adresini acin.

## Kullanim

### Ilk Kurulum
1. Dashboard'da **"Kanalimi Kur"** butonuna basin
2. Kanalinizin videolari otomatik olarak toplanacak

### Trend Toplama
1. **"Trend Topla"** butonuna basin
2. Global trendler toplanip analiz edilecek
3. Trendler sayfasindan sonuclari inceleyin

### Video Fikri Uretme
3 farkli kaynaktan fikir uretebilirsiniz:
- **Trendlerden**: Global trendlere dayali fikirler
- **Videolarimdan**: En cok izlenen videolariniza dayali spin-off fikirler
- **Rakiplerden**: Rakip kanallarin basarili videolarindan ilham

### Kanal Kesfi
1. **"Kanal Kesfet"** ile global kanallari bulun
2. **"Benzer Kanal Bul"** ile size yakin kanallari tespit edin
3. **"Rakipleri Analiz Et"** ile rakip videolari inceleyin

## API Kota Bilgisi

YouTube Data API v3 ucretsiz katmani gunluk **10.000 birim** kota saglar.
- Arama islemi: 100 birim
- Video/kanal bilgisi: 1 birim
- Uygulama kota kullanimini otomatik takip eder

## Teknik Yapi

```
src/
  server.js              # Express sunucu + cron gorevler
  db/database.js         # SQLite veritabani
  services/
    youtube-api.js       # YouTube Data API entegrasyonu
    trend-analyzer.js    # Trend analiz motoru
    idea-generator.js    # Video fikri uretici
    channel-discovery.js # Kanal kesif sistemi
  routes/api.js          # REST API endpoint'leri
public/
  index.html             # Ana sayfa
  css/style.css          # Stiller
  js/app.js              # Frontend JavaScript
```

## Lisans

MIT
