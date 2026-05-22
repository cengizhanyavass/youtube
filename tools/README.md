# YouTube Otomasyon Araçları

Bu klasör YouTube kanalı yönetimi, içerik üretimi ve otomasyon için en iyi açık kaynak araçları içerir.

## Araçlar

### 1. claude-youtube (AgriciDaniel)
Claude Code'u YouTube büyüme danışmanına dönüştürür.
- Kanal denetimi, SEO optimizasyonu, senaryo yazımı
- Thumbnail brief, içerik stratejisi, analitik yorumlama
- YouTube API entegrasyonu
- **Kaynak:** https://github.com/AgriciDaniel/claude-youtube

### 2. shortgpt (RayVentura) ⭐ 7.3k
YouTube Shorts ve TikTok için yapay zeka otomasyon framework'ü.
- Senaryo oluşturma, seslendirme, altyazı
- 30+ dil desteği
- Görsel ve video varlık otomatik bulma
- **Kaynak:** https://github.com/RayVentura/ShortGPT

### 3. money-printer (FujiwaraChoki) ⭐ 13.3k
YouTube Shorts otomatik oluşturma aracı.
- Konu ver → video otomatik oluşturulur
- Ollama ile yerel AI modelleri (ücretsiz)
- Docker ile kolay kurulum
- **Kaynak:** https://github.com/FujiwaraChoki/MoneyPrinter

### 4. money-printer-v2 (FujiwaraChoki) ⭐ 30.5k
Tam YouTube otomasyon paketi.
- YouTube Shorts otomatik oluşturma + CRON ile zamanlama
- Otomatik yükleme ve metadata
- **Kaynak:** https://github.com/FujiwaraChoki/MoneyPrinterV2

## Kullanım Önceliği

| Amaç | Araç |
|------|------|
| Claude ile kanal stratejisi | `claude-youtube` |
| Kısa video otomasyonu | `shortgpt` veya `money-printer` |
| Tam otomasyon (oluştur + yükle) | `money-printer-v2` |
