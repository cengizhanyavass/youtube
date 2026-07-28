# Seslendirme + Görsel Video Editörü

`1.wav ... 11.wav` seslendirme dosyalarını görsellerle birleştirip tek video üretir.

Her ses dosyası bir **bölüm**. Bölümün süresi kadar görsel ekranda kalır, görselin
**odak noktasına** doğru yavaş bir zoom (Ken Burns) uygulanır, bölümler arası
**yumuşak geçiş** (crossfade) yapılır. Ses hiç kesilmez — video süresi seslerin
toplamına birebir eşitlenir, kayma olmaz.

## Kurulum

```bash
bash setup.sh
```

Sistemde ffmpeg olmasa da çalışır (`imageio-ffmpeg` kendi binary'sini getirir).

## Dosyaları yerleştir

```
assets/audio/    1.wav  2.wav  ...  11.wav
assets/images/   1.jpg  2.jpg  ...  (jpg/png/webp)
```

Sıralama sayıya göre yapılır, yani `10.wav` `2.wav`'dan sonra gelir.

## Kullanım

```bash
python3 kenburns_edit.py --plan       # önce planı gör (render yok, saniyeler sürer)
python3 kenburns_edit.py --preview    # hızlı 540p ön izleme -> out/preview.mp4
python3 kenburns_edit.py              # final 1080p -> out/final.mp4
```

`--plan` çıktısı şuna benzer:

```
11 ses / 11 gorsel / 11 cekim  toplam 1:05.06
    1. 1.wav      1.jpg      4.81s  in  zoom->1.14  odak=(0.44,0.51)
    2. 2.wav      2.jpg      8.09s  out zoom->1.14  odak=(0.48,0.46)
```

## Görsel dağılımı

- **Görsel sayısı = ses sayısı** → her bölüme bir görsel.
- **Görsel daha fazla** → fazladan görseller bölümlerin içine dağıtılır, bölüm
  süresi aralarında eşit bölünür. `--min-shot` (varsayılan 4sn) altına düşen
  bölünmeler yapılmaz, görsel çok hızlı geçmez.
- **Görsel daha az** → görseller sırayla tekrar kullanılır.

## Zoom / odak nasıl belirleniyor

Görselin detay yoğunluğu en yüksek bölgesi (yüz, ana obje, yazı genelde oraya
düşer) otomatik bulunur ve kadraj o noktaya doğru kayarak yaklaşır. Yön her
çekimde değişir: bir yaklaşır, bir uzaklaşır — böylece izleyicide monotonluk
olmaz. Kadraj her zaman görselin içinde kalır, siyah bant çıkmaz.

Otomatik seçimi beğenmezsen `edit.json` ile görsel bazında geç:

```json
{
  "images": {
    "3.jpg": { "focus": [0.35, 0.28], "move": "in",  "zoom": 1.22 },
    "7.png": { "focus": [0.70, 0.55], "move": "out", "zoom": 1.10 }
  }
}
```

- `focus`: `[x, y]`, sol üst `[0,0]`, sağ alt `[1,1]`.
- `move`: `in` (yakınlaş) veya `out` (uzaklaş).
- `zoom`: hareket sonundaki büyütme oranı.

## Ayarlar

| Seçenek | Varsayılan | Ne yapar |
|---|---|---|
| `--zoom` | `1.14` | Maksimum zoom oranı. 1.25 üstü belgesel için sert kaçar. |
| `--transition-duration` | `1.0` | Geçiş süresi (saniye). |
| `--transition` | `fade` | ffmpeg xfade geçişi (`fade`, `fadeblack`, `dissolve`, `wipeleft`...). |
| `--min-shot` | `4.0` | Bir görselin ekranda kalacağı minimum süre. |
| `--width` / `--height` | `1920` / `1080` | Çıktı çözünürlüğü. |
| `--fps` | `30` | Kare hızı. |
| `--crf` | `18` | Kalite; küçük = daha iyi + daha büyük dosya. |
| `--preset` | `medium` | x264 hız/kalite dengesi. |
| `--audio-dir` / `--image-dir` | `assets/...` | Kaynak klasörler. |
| `--out` | `out/final.mp4` | Çıktı yolu. |

## Notlar

- Render öncesi mutlaka `--preview` çalıştır; 540p ön izleme finalden kat kat
  hızlı biter ve odak/geçiş hatalarını orada yakalarsın.
- Farklı en-boy oranındaki görseller ortadan kırpılarak 16:9'a doldurulur;
  odak noktası kırpma sonrasına göre yeniden hesaplanır.
- Görsel sayısı bölümlerin taşıyabileceğinden fazlaysa artanlar kullanılmaz ve
  ekrana uyarı düşer; hepsini kullanmak için `--min-shot` değerini düşür.
- Render hızı kabaca gerçek zamanın 0.7 katı (1080p, `medium` preset): 30
  dakikalık bir video ~25 dakikada biter. Acelen varsa `--preset veryfast`.
- `out/` git'e girmez (bkz. `.gitignore`), video dosyalarını repoya basma.
