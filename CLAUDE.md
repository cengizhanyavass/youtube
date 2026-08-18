# Bu repoda çalışma kuralları (token tasarrufu odaklı)

## Temel ilke
Veriyi model değil, script işler. Asla `data/cache/*.json` dosyalarını okuma —
bunlar megabaytlarca ham yt-dlp çıktısıdır. Bunun yerine `tools/` altındaki
analiz komutlarını çalıştır ve **sadece** kısa tablo çıktısını kullan.

## Komut haritası
| İhtiyaç | Komut |
|---|---|
| kanal analizi | `.venv/bin/python tools/channel_analyze.py <kanal_url> --limit 80` |
| rakip listesi | `.venv/bin/python tools/competitors.py --from-channel <kanal_url>` |
| niş taraması | `.venv/bin/python tools/niche_finder.py "<tohum kelime>"` |
| video/arama verisi | `.venv/bin/python tools/yt_fetch.py search "<terim>"` |
| animasyon önizleme | `.venv/bin/python tools/stickman.py --action <aksiyon> --seconds 3` |
| final video | `.venv/bin/python tools/build_video.py scripts/<x>.json` |

## Alışkanlıklar
- Video denemelerini önce `--fast` ile üret (640x360@15fps, saniyeler sürer),
  onay gelince tam çözünürlükte bas.
- Yeni video isteği geldiğinde `scripts/` altına yeni bir JSON yaz; mevcut
  senaryoyu bozma. `scripts/example.json` şablon olarak kalsın.
- Uzun script metinlerini sohbete yapıştırma, doğrudan JSON dosyasına yaz.
- Analiz çıktısını özetlerken tabloyu tekrar basma; sadece çıkarımı ve
  aksiyon maddelerini yaz.
- Yeni aksiyon gerekirse `tools/stickman.py` içindeki `ACTIONS` sözlüğüne
  faz fonksiyonu ekle; ayrı dosya açma.
