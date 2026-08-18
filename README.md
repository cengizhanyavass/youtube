# YouTube Stickman Pipeline

Rakip araştırması, niş bulma, kanal analizi ve 2D çöp adam (stickman) video
üretimini tek repoda toplayan **tamamen ücretsiz** araç seti.
API anahtarı yok, abonelik yok, bulut servisi yok — her şey kendi makinende çalışır.

## Kurulum

```bash
bash setup.sh
```

Kurulan bileşenler:

| Bileşen | Ne işe yarar | Lisans |
|---|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | YouTube metadata (kanal, video, arama) — anahtarsız | Unlicense |
| [ffmpeg](https://ffmpeg.org) | video/ses birleştirme, kodlama | LGPL/GPL |
| [edge-tts](https://github.com/rany2/edge-tts) | ücretsiz seslendirme (Microsoft Edge sesleri) | GPL-3.0 |
| Pillow + numpy | stickman çizim motoru | HPND / BSD |

## Araçlar

Hepsi `tools/` altında, hepsi kısa ve tablo biçiminde çıktı verir.

```bash
V=.venv/bin/python

# 1) Kendi kanalının analizi
$V tools/channel_analyze.py https://www.youtube.com/@KANALIN --limit 80

# 2) Rakip araştırması (kanalın başlıklarından otomatik terim üretir)
$V tools/competitors.py --from-channel https://www.youtube.com/@KANALIN

# 3) Niş bulma (talep / rekabet skoru)
$V tools/niche_finder.py "stickman" "stick figure"

# 4) Tek video / arama metadata
$V tools/yt_fetch.py video https://youtu.be/VIDEOID
$V tools/yt_fetch.py search "stickman animation" --limit 25

# 5) Stickman animasyon önizleme
$V tools/stickman.py --action walk --seconds 4 --bubble "Selam" --out out/test.mp4

# 6) Senaryodan bitmiş video (görüntü + ses + altyazı)
$V tools/build_video.py scripts/example.json --fast     # taslak, saniyeler içinde
$V tools/build_video.py scripts/example.json            # 1080p final
```

## Senaryo formatı

`scripts/example.json` — her sahne bir JSON nesnesi:

```json
{
  "title": "Ekranda başlık",
  "say": "Seslendirilecek ve altyazıya düşecek metin",
  "duration": 4,
  "actors": [
    { "action": "wave", "x": 0.5, "bubble": "Selam!", "cycles": 3 }
  ]
}
```

Sahne süresi verilmezse seslendirmenin uzunluğundan otomatik hesaplanır.

**Aktör alanları:** `action`, `x` (0–1 yatay konum), `y` (ayak hizası),
`height` (boy oranı), `color`, `flip` (aynala), `cycles` (hareket hızı),
`bubble` (konuşma balonu), `label` (isim etiketi).

**Hazır aksiyonlar:** `idle`, `talk`, `wave`, `walk`, `run`, `jump`, `think`,
`cheer`, `fall`, `shrug`, `sit`, `point_right`, `point_left`.

Yeni aksiyon eklemek: `tools/stickman.py` içine faz (0–1) alıp poz döndüren bir
fonksiyon yaz ve `ACTIONS` sözlüğüne ekle. Açı sistemi: 0 = aşağı, 90 = sağa,
180 = yukarı, −90 = sola.

## Türkçe seslendirme

```bash
$V tools/tts.py --list tr-TR          # mevcut Türkçe sesler
$V tools/tts.py "Merhaba" --voice tr-TR-EmelNeural --out out/a.mp3
```

Ağ engelliyse araç sessiz parça üretip videoyu yine de tamamlar (`--no-tts` ile
seslendirmeyi tümden kapatabilirsin).

## Token tasarrufu

Bu repo, Claude'a **ham veri değil özet** göstermek üzere tasarlandı:

- yt-dlp'nin megabaytlık JSON'u `data/cache/` içine yazılır, ekrana basılmaz.
- Analiz araçları 20–40 satırlık tablo döndürür (~300–600 token).
- Aynı sorgu ikinci kez çalıştırıldığında cache'ten okunur (`--refresh` ile tazele).
- Video üretimi tamamen yerelde; model hiçbir kareyi görmez.

Tipik iş akışı: komutu terminalde çalıştır → sadece tabloyu Claude'a yapıştır →
strateji/başlık/senaryo iste. Böylece bir analiz turu binlerce değil, birkaç yüz
token tutar.

## Bilinen sınır

Bu repo Claude Code'un bulut ortamında geliştirildi; oradaki ağ politikası
`youtube.com` ve TTS servisine çıkışı engelliyor. Analiz ve seslendirme
komutları **kendi makinende** çalıştırıldığında sorunsuz çalışır; çizim ve video
üretim hattı her yerde çalışır (demo `out/demo.mp4` ile doğrulandı).
