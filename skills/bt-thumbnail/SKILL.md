# Skill: bt-thumbnail — BeastTales Thumbnail Üretici

## Tetikleyiciler (Türkçe / English)
- `bt-thumbnail [konu]` veya `/bt-thumbnail [konu]`
- "thumbnail üret [konu]"
- "kapak görseli oluştur [konu]"
- "generate thumbnail for [topic]"

## Token Kuralı
Sadece şunları oku:
1. `channels/beasttales/profile.md` → thumbnail stil bölümü
2. `wiki/beasttales/topics/[konu-adı].md` → konu kartı

~150 satır toplam. Başka dosya okuma.

## Thumbnail Formülü
```
ELEMAN 1 (karedinin %60'ı): Hayvan yüzü — extreme close-up, gözler direkt bakış
ELEMAN 2 (karedinin %40'ı arka plan): Medeniyet unsuru silueti veya epik sahne
ELEMAN 3 (metin): Maksimum 3 kelime — yüksek kontrast, kalın
ELEMAN 4 (renk): Karanlık dramatik arka plan + tek vurgu rengi
```

## Metin Overlay Kuralları
- Maksimum 3 kelime
- Sayı olduğunda mükemmel: "50,000 DEAD" / "1 ANIMAL" / "3 DAYS"
- Çelişki tetikleyicileri: "THEY WERE WRONG" / "THE REAL CAUSE" / "NOBODY KNEW"
- Merak/korku: "WHAT KILLED ROME?" / "THE HIDDEN KILLER" / "HISTORY LIED"

---

## 3 KAVRAM ÜRETİLECEK

### KAVRAM A — YÜZE ODAK (çoğu konu için en iyi)
Hayvan extreme close-up, bir göz baskın, medeniyet harabeleri arka planda, karanlık dramatik

### KAVRAM B — ÖLÇEK KARŞITLIĞI (kitlesel olaylar için)
Hayvan küçük ön planda, devasa medeniyet sahnesi arkada — "bu küçük şey nasıl..." hissi

### KAVRAM C — YÜZLEŞME (savaş/çatışma konular için)
Hayvan ve insan/medeniyet unsuru karşı karşıya, gerilim

---

## MİDJOURNEY THUMBNAIL PROMPTLARI

### KAVRAM A — YÜZE ODAK
```
dramatic extreme close-up [HAYVAN TÜRÜ] face, one eye dominant, intense direct gaze,
[STİL: comic book ink linework and graphic novel art / 
       natural history engraving and editorial illustration],
[MEDENİYET: crumbling Roman columns / Egyptian pyramid silhouette / 
            Viking longship burning / Mongol steppe horizon / Ottoman minaret] in background,
dark dramatic stormy sky, bold chiaroscuro lighting, 
single accent color [RENK: deep red / gold ochre / electric blue / blood orange],
space for text overlay at top or bottom,
16:9 cinematic thumbnail composition
--ar 16:9 --style raw --v 6
```

### KAVRAM B — ÖLÇEK KARŞITLIĞI
```
tiny [HAYVAN TÜRÜ] in extreme foreground, 
massive [MEDENİYET SAHNESİ] behind — army formation / burning city / collapsing empire,
[STİL: comic book ink style / natural history illustration],
bird's eye view or low dramatic angle,
overwhelming sense of scale — small creature, vast consequence,
dark storm atmosphere, accent color [RENK],
16:9 cinematic thumbnail --ar 16:9 --style raw --v 6
```

### KAVRAM C — YÜZLEŞME
```
[TARİHİ KARAKTER: armored soldier / emperor / emperor on throne] 
facing [HAYVAN TÜRÜ], tension and confrontation,
[STİL: comic book ink linework / natural history editorial],
dramatic backlight, fire or lightning in background,
faces in profile showing fear vs predatory calm,
dark moody atmosphere, accent color [RENK],
16:9 aspect ratio --ar 16:9 --style raw --v 6
```

---

## IMAGEN 4 THUMBNAIL PROMPTLARI

### Kavram A — Imagen4
```
A dramatic extreme close-up of a [HAYVAN TÜRÜ], 
one eye filling most of the frame, intense piercing gaze directly at viewer,
illustrated in [comic book ink and graphic novel style / 
               natural history book engraving style],
[MEDENİYET UNSURU] visible in the dark background,
dramatic storm lighting, single [RENK] color accent,
dark moody atmosphere, cinematic 16:9 composition,
space left at top and bottom for text overlay
```

### Kavram B — Imagen4
```
A tiny [HAYVAN TÜRÜ] in the close foreground with a massive 
[MEDENİYET SAHNESİ: burning ancient city / collapsed empire ruins / 
                    vast army marching / plague-ravaged streets] 
visible far behind it,
illustrated in graphic novel or historical documentary art style,
bird's eye dramatic angle, overwhelming sense of scale,
dark dramatic atmosphere with [RENK] accent lighting, 16:9 ratio
```

---

## RENK AKSANI REHBERİ

| Medeniyet / Tema | Renk |
|-----------------|------|
| Roma | `deep crimson red` |
| Mısır | `gold ochre` |
| Moğol | `electric blue` |
| Osmanlı | `deep turquoise` |
| Viking | `steel grey blue` |
| Veba / Ölüm | `sickly yellow green` |
| Savaş / Çöküş | `blood orange` |
| Doğa / Ekoloji | `deep forest green` |
| Orta Asya | `warm amber` |

---

## ÇIKTI FORMATI

Şuraya kaydet: `wiki/beasttales/thumbnails/[konu-adı]-thumbnail.md`

```markdown
# [Konu] — Thumbnail Konseptleri

## KAVRAM A — YÜZE ODAK
**Metin Overlay:** [3 kelime]
**Renk Aksanı:** [renk]
**Midjourney Prompt:**
[prompt]
**Imagen4 Prompt:**
[prompt]

## KAVRAM B — ÖLÇEK KARŞITLIĞI
**Metin Overlay:** [3 kelime]
**Renk Aksanı:** [renk]
**Midjourney Prompt:**
[prompt]
**Imagen4 Prompt:**
[prompt]

## KAVRAM C — YÜZLEŞME
**Metin Overlay:** [3 kelime]
**Renk Aksanı:** [renk]
**Midjourney Prompt:**
[prompt]
**Imagen4 Prompt:**
[prompt]

## ÖNERİLEN: Kavram [A/B/C]
**Neden:** [Bu konu için neden bu thumbnail kazanır]

## A/B Test Önerisi
İlk 48 saatte Kavram [X] vs Kavram [Y] test et. Kazanan: analytics'te daha yüksek CTR.
```
