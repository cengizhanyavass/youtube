# YouTube Video Üretici

MoneyPrinterTurbo tabanlı otomatik YouTube video üretim sistemi.

Bir konu girin, yapay zeka senaryo yazsın, seslendirsin, görüntüler bulsun ve videoyu otomatik oluştursun.

---

## Hızlı Başlangıç

### 1. Kurulum

```bash
bash setup.sh
```

### 2. API Anahtarlarını Ayarla

`MoneyPrinterTurbo/config.toml` dosyasını düzenle:

```toml
[app]
# Pexels ücretsiz video için (zorunlu)
# Kayıt: https://www.pexels.com/api/
pexels_api_keys = ["SENIN_PEXELS_API_ANAHTARIN"]

# Yapay zeka için bir tane seç:
llm_provider = "openai"
openai_api_key = "sk-..."
openai_model_name = "gpt-4o-mini"

# veya DeepSeek (daha ucuz):
# llm_provider = "deepseek"
# deepseek_api_key = "..."
```

### 3. Sunucuyu Başlat

```bash
cd MoneyPrinterTurbo
python main.py
```

### 4. Video Üret

```bash
# Tek konu
python generate_video.py --konu "Yapay Zekanın Geleceği" --stil shorts

# Dil ile
python generate_video.py --konu "How AI Changes the World" --stil uzun --dil en

# Toplu üretim (dosyadan)
python generate_video.py --liste konular_ornek.txt --stil motivasyon
```

---

## Video Stilleri

| Stil         | Format | Açıklama                              |
|--------------|--------|---------------------------------------|
| `shorts`     | 9:16   | YouTube Shorts / TikTok dikey video   |
| `uzun`       | 16:9   | YouTube uzun format yatay video       |
| `belgesel`   | 16:9   | Yavaş tempolu bilgi verici format     |
| `motivasyon` | 9:16   | Hızlı tempolu ilham verici short      |
| `haber`      | 16:9   | Profesyonel haber / bilgi formatı     |

```bash
# Tüm stilleri listele
python generate_video.py --stiller
```

---

## Komut Parametreleri

```
python generate_video.py [seçenekler]

  --konu, -k    Video konusu
  --stil, -s    Video stili (varsayılan: shorts)
  --dil, -d     Dil kodu: tr, en, de, fr... (varsayılan: tr)
  --ses         Ses adı (boş = otomatik)
  --kaynak      pexels veya pixabay (varsayılan: pexels)
  --adet        Üretilecek video sayısı (varsayılan: 1)
  --liste, -l   Konu listesi dosyası
  --stiller     Mevcut stilleri göster
```

---

## Web Arayüzü

Sunucu çalışırken tarayıcıda aç:
- **Web UI**: http://localhost:8501
- **API Docs**: http://localhost:8080/docs

---

## Desteklenen Yapay Zeka Sağlayıcıları

| Sağlayıcı   | Öneri | Link |
|-------------|-------|------|
| OpenAI      | gpt-4o-mini ucuz ve hızlı | platform.openai.com |
| DeepSeek    | Çok ucuz, Türkçe iyi | platform.deepseek.com |
| Gemini      | Ücretsiz kota var | aistudio.google.com |
| Ollama      | Tamamen ücretsiz, yerel | ollama.ai |

---

## Proje Yapısı

```
youtube/
├── MoneyPrinterTurbo/   # Ana video üretim motoru
│   ├── config.toml      # Yapılandırma (API anahtarları)
│   ├── main.py          # Sunucu başlatıcı
│   └── app/             # Uygulama kodu
├── generate_video.py    # Kolay kullanım scripti
├── setup.sh             # Otomatik kurulum
├── konular_ornek.txt    # Örnek konu listesi
└── README.md
```
