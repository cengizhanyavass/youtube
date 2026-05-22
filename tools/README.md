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

### 5. faceless-video (SamurAIGPT) ⭐ 438
Yapay zeka ile yüzsüz video üretimi.
- Senaryo + ses + konuşan yüz tamamen AI ile
- Faceless kanal formatı için ideal
- **Kaynak:** https://github.com/SamurAIGPT/AI-Faceless-Video-Generator

### 6. advertools (eliasdabbas) ⭐ 1.4k
YouTube SEO ve analiz araçları.
- Anahtar kelime araştırması
- Rakip kanal analizi
- Online pazarlama verimliliği
- **Kaynak:** https://github.com/eliasdabbas/advertools

### 7. viral-shorts (Dark2C)
Viral faceless YouTube Shorts üretici.
- Trend konulardan otomatik Shorts
- AI senaryo + TTS + FFmpeg pipeline
- **Kaynak:** https://github.com/Dark2C/Viral-Faceless-Shorts-Generator

### 8. youtube-mcp (pauling-ai)
YouTube için 40 araçlı MCP server.
- Kanal analitiği ve video yayınlama API'si
- Claude Code ile direkt entegrasyon
- **Kaynak:** https://github.com/pauling-ai/youtube-mcp-server

## Kullanım Önceliği

| Amaç | Araç |
|------|------|
| Claude ile kanal stratejisi | `claude-youtube` |
| Kısa video otomasyonu | `shortgpt` veya `money-printer` |
| Tam otomasyon (oluştur + yükle) | `money-printer-v2` |
| Yüzsüz video üretimi | `faceless-video` |
| SEO araştırması | `advertools` |
| Viral Shorts | `viral-shorts` |
| YouTube API entegrasyonu | `youtube-mcp` |
