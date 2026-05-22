# Skill: bt-visuals — BeastTales Video Görselleri

## Tetikleyiciler (Türkçe / English)
- `bt-visuals [konu]` veya `/bt-visuals [konu]`
- "görseller üret [konu]"
- "sahne promptları [konu]"
- "generate visuals for [topic]"
- "midjourney prompts for [topic]"
- "imagen4 prompts for [topic]"

## Token Kuralı
Sadece şunları oku:
1. `channels/beasttales/profile.md` → görsel stil bölümü
2. `wiki/beasttales/scripts/[konu]-script.md` → senaryo

Başka hiçbir dosya okuma.

## Görsel Stil: İki Seçenek

### STİL A — "Red Panda / Known By Birds" (Çizgi Roman)
Dinamik, dramatik, grafik roman hissi. Daha modern, daha güçlü sosyal medya etkisi.

**Temel stil dizisi:**
```
comic book illustration style, detailed ink linework, graphic novel art,
dramatic cinematic lighting, warm interior glow vs cold exterior contrast,
highly detailed background, sharp foreground soft background, 2D illustration,
dark moody atmosphere, vibrant but controlled color palette
```

### STİL B — Doğal Tarih Kitabı (BeastTales Klasik)
Ansiklopedik, güvenilir, belgesel hissi. Daha yüksek CPM, daha akademik kitle.

**Temel stil dizisi:**
```
natural history book illustration, detailed ink engraving, editorial illustration,
National Geographic historical art, cross-hatching technique, aged parchment tones,
dramatic chiaroscuro lighting, cinematic composition, muted earth tones
```

---

## SAHNE ŞABLONLARI (Genel — Konu Bağımsız)

Her sahne için aşağıdaki şablonlardan birini seç:

### ŞABLON 1 — HAYVAN YAKINI (Soğuk Açılış)
```
[HAYVAN] extreme close-up, eyes wide open intense gaze, 
[STİL A veya B],
[ATMOSFER] — dramatic storm / heavy rain / burning fire glow / plague fog,
dark dramatic background, single dramatic light source,
cinematic composition, 16:9 --ar 16:9 --style raw --v 6
```

### ŞABLON 2 — HAYVAN + MEDENIYET (Ana Sahne)
```
[HAYVAN] in the foreground, [MEDENİYET UNSURU: ruined city / burning harbor / 
desert fortress / frozen palace / jungle temple] in background,
[STİL A veya B],
[ATMOSFER],
dramatic scale contrast — small animal, vast civilization,
cinematic wide shot, 16:9 --ar 16:9 --style raw --v 6
```

### ŞABLON 3 — KALABALIK SAHNE (Nedensellik Zinciri)
```
[HAYVAN] swarm / herd / colony moving through [ORTAM],
[MEDENİYET UNSURU] visible but overwhelmed,
[STİL A veya B],
bird's eye view / dramatic overhead angle,
sense of unstoppable scale and movement,
16:9 --ar 16:9 --style raw --v 6
```

### ŞABLON 4 — İNSAN + HAYVAN KARŞILAŞMASI
```
[TARİHİ KARAKTER: soldier / emperor / farmer / merchant] facing [HAYVAN],
[STİL A veya B],
[ATMOSFER],
tension and confrontation, dramatic low angle,
16:9 --ar 16:9 --style raw --v 6
```

### ŞABLON 5 — HARİTA / YAYILMA (B-Roll)
```
illustrated map style, [HAYVAN] movement paths shown as arrows across [MEDENİYET BÖLGESİ],
parchment texture, ink illustration, cartographic style,
dramatic color — red for danger zones, gold for trade routes,
16:9 --ar 16:9 --style raw --v 6
```

---

## IMAGEN 4 PROMPT ŞABLONLARI

Imagen 4 için flag kullanılmaz — doğal dil yeterli:

### Imagen4 — Hayvan Yakını
```
A dramatic close-up of [HAYVAN], eyes intense and piercing, 
illustrated in [comic book ink linework / natural history engraving] style,
[ATMOSFER: heavy rain falling around it / fire glow from behind / 
snow drifting past / fog surrounding],
dark moody atmosphere, cinematic lighting,
highly detailed, 16:9 aspect ratio, sharp focus on animal face
```

### Imagen4 — Epik Geniş Sahne
```
A [HAYVAN] in the foreground, [MEDENİYET: Roman city / Egyptian pyramid field / 
Viking harbor / Mongol steppe / Ottoman palace] visible in the background,
[comic book graphic novel illustration / natural history book illustration] style,
dramatic [storm / fire / plague / drought] atmosphere,
warm vs cold lighting contrast, epic scale, cinematic wide angle, 16:9 ratio
```

### Imagen4 — Nedensellik Sahne
```
Hundreds of [HAYVAN] moving through [ORTAM: city streets / grain fields / 
harbor docks / mountain pass / desert caravan route],
illustration style like a graphic novel or historical documentary art,
dramatic overhead bird's eye view, sense of inevitable unstoppable force,
dark atmosphere, [MEDENİYET] structures crumbling or overwhelmed, 16:9 ratio
```

---

## RENK AKSANI REHBERİ

| Medeniyet / Tema | Accent Rengi |
|------------------|-------------|
| Roma | `deep crimson red` |
| Mısır | `gold ochre` |
| Moğol | `electric blue` |
| Osmanlı | `deep turquoise` |
| Viking/Norse | `steel grey blue` |
| Orta Asya | `warm amber` |
| Veba/Hastalık | `sickly yellow green` |
| Savaş/Çöküş | `blood orange` |
| Doğa/Ekoloji | `deep forest green` |

---

## ÇALIŞTIRMA ADIMLARI

### 1. SENARYO OKUMA
Senaryoyu oku. 12–15 görsel an belirle:
- 1 → Soğuk Açılış (en dramatik)
- 2 → Dünyanın Öncesi
- 3 → Hayvanın Girişi
- 4 → Nedensellik Zinciri
- 2 → Dönüm Noktası
- 1 → Karşı Anlatı Ortaya Çıkışı
- 1 → Miras / Günümüz
- 2 → B-Roll (harita + yakın detay)

### 2. PROMPT OLUŞTURMA
Her görsel an için:
- Şablonu seç (1–5)
- Stili seç (A veya B)
- Atmosferi seç
- Renk aksanını ekle
- Midjourney VE Imagen4 versiyonu yaz

### 3. KAYDET
Şuraya kaydet: `wiki/beasttales/visuals/[konu-adı]-prompts.md`

---

## ÇIKTI FORMATI

```markdown
# [Konu] — Video Görselleri
**Stil:** [A: Çizgi Roman / B: Doğal Tarih]
**Renk Aksanı:** [renk]
**Toplam Sahne:** [N]

---

## SAHNE 01 — SOĞUK AÇILIŞ
**Senaryo anı:** "[senaryodan 1-2 satır alıntı]"
**Şablon:** [1–5]

**Midjourney Prompt:**
[prompt]

**Imagen4 Prompt:**
[prompt]

---
[her sahne için tekrar]
```
