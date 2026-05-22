# Skill: bt-visuals — 40-45 Imagen4 Sahne Üretici

## Tetikleyiciler
- `/bt-visuals [konu]`
- `görseller üret [konu]`
- `sahne promptları [konu]`
- `imagen4 [konu]`

## TOKEN KURALI — SADECE 1 DOSYA OKU
```
wiki/beasttales/topics/[konu-adı].md
```
Başka hiçbir dosya okuma. Tüm şablonlar bu skill içinde gömülüdür.

---

## DEĞIŞKEN ÇIKARMA
Konu kartından şunları çıkar:

```
HAYVAN    = [animal field]
UYGAR     = [civilization field]
DÖNEM     = [era/date range]
RENK      = [renk aksanı rehberi'ne göre]
ATMOSFER1 = [soğuk açılış için]
ATMOSFER2 = [zirve sahne için]
```

---

## 45 SAHNE ÜRETİM ŞEMASİ

### BÖLÜM 1 — SOĞUK AÇILIŞ (4 prompt)

**S01 — Hayvan Gözü**
```
Extreme close-up of [HAYVAN] face, one eye filling the frame, intense direct gaze,
comic book illustration style, detailed ink linework, graphic novel art,
[ATMOSFER1: heavy rain falling / fire glow from behind / snow drifting / plague fog],
dramatic cinematic lighting, dark moody atmosphere,
single [RENK] color accent, sharp focus on eye,
16:9 aspect ratio
```

**S02 — Hayvan Tam Vücut**
```
Full body portrait of [HAYVAN] in dramatic stance,
comic book illustration style, detailed ink linework, graphic novel art,
[DÖNEM] [UYGAR] environment background, heavily detailed,
dramatic low angle shot looking up at animal,
dark storm sky above, [RENK] accent light,
16:9 aspect ratio
```

**S03 — Epik Geniş Sahne**
```
[HAYVAN] silhouette against a massive [UYGAR] city skyline — columns, towers, smoke,
natural history book illustration, ink engraving, editorial style,
[ATMOSFER1], epic scale — small animal, vast civilization behind,
dramatic wide establishing shot, [RENK] glow on horizon,
16:9 aspect ratio
```

**S04 — Dram Anı**
```
[HAYVAN] in motion — running, crawling, flying, spreading across frame,
comic book illustration style, motion blur ink lines, graphic novel art,
sense of unstoppable force and inevitability,
[UYGAR] structures visible and fragile in background,
dark dramatic atmosphere, [RENK] highlights,
16:9 aspect ratio
```

---

### BÖLÜM 2 — DÜNYANIN ÖNCESİ (5 prompt)

**S05 — İmparatorluk Zirve Anı**
```
[UYGAR] at its peak — grand palace, crowded market, triumphant army,
natural history book illustration, detailed ink engraving, cross-hatching,
golden hour warm light, prosperity and power,
wide panoramic view, aged parchment tones,
16:9 aspect ratio
```

**S06 — Halk Günlük Hayat**
```
Ordinary people of [UYGAR] — farmers, soldiers, merchants — going about daily life,
comic book illustration style, ink linework,
[DÖNEM] architecture and clothing detail, bustling activity,
warm afternoon light, sense of normalcy before catastrophe,
16:9 aspect ratio
```

**S07 — Güç Sembolü**
```
[UYGAR] ruler or general on throne or commanding position,
natural history book illustration, dramatic portrait composition,
robes, armor, symbols of [UYGAR] power in background,
candlelight or torch lighting, strong shadows, regal atmosphere,
16:9 aspect ratio
```

**S08 — Hayvan İlk Görünüş (gizli)**
```
[HAYVAN] barely visible in shadows — in grain storage, in forest edge, 
in harbor dock, in palace corner — unnoticed, small, overlooked,
comic book illustration, detailed ink, dark environment,
warm lit human activity in foreground ignoring the animal,
sense of dramatic irony — the audience sees what no one else does,
16:9 aspect ratio
```

**S09 — Harita Görünüşü**
```
Illustrated historical map of [UYGAR] territory and surrounding regions,
old parchment texture, ink illustration, cartographic art,
[DÖNEM] borders and cities labeled, trade routes as dotted lines,
[HAYVAN] range area marked in [RENK],
dramatic top-down map view, 16:9 aspect ratio
```

---

### BÖLÜM 3 — HAYVANI TANIYALIM (5 prompt)

**S10 — Hayvan Portresi**
```
Scientific portrait illustration of [HAYVAN] — full body, anatomically accurate,
natural history book illustration, detailed ink engraving,
white or parchment background, specimen plate style,
clear detail of key anatomical features, labels if appropriate,
16:9 aspect ratio
```

**S11 — Hayvan Habitatı**
```
[HAYVAN] in its natural environment — [habitat: desert / forest / steppe / river delta / 
mountain / coast], at home and thriving,
comic book illustration, ink linework,
lush detailed background, animal relaxed and confident,
warm natural lighting, 16:9 aspect ratio
```

**S12 — Hayvan Davranış Sahnesi**
```
[HAYVAN] demonstrating its key behavior — [foraging / hunting / breeding / 
migrating / burrowing / flying in swarm / reproducing rapidly],
natural history book illustration, action captured in ink,
detailed environment, scientific accuracy with dramatic composition,
16:9 aspect ratio
```

**S13 — Hayvan ve İnsan İlk Temas**
```
First contact moment — [UYGAR] human encountering [HAYVAN] for first time,
or [HAYVAN] entering [UYGAR] territory edge,
comic book illustration, dramatic framing,
both human and animal visible, tension or curiosity,
[ATMOSFER1] weather or environment, 16:9 aspect ratio
```

**S14 — Yakın Detay**
```
Extreme macro close-up of [HAYVAN] — key anatomical detail: 
[eye / teeth / claws / wings / proboscis / shell / fur texture],
natural history engraving style, ultra-detailed ink work,
dramatic close lighting, dark background,
scientific illustration meets dramatic art, 16:9 aspect ratio
```

---

### BÖLÜM 4 — NEDENSELLİK ZİNCİRİ (12 prompt)

**S15 — Zincir Başlangıcı**
```
Single [HAYVAN] beginning to interact with [UYGAR] infrastructure — 
grain store / harbor / farmland / palace / trade route,
comic book illustration, ink linework,
small scale — just one animal, one location, small event,
[ATMOSFER1], hint of things to come, 16:9 aspect ratio
```

**S16 — Çoğalma Başlıyor**
```
Multiple [HAYVAN] now visible — a small group spreading,
natural history book illustration, ink engraving,
[UYGAR] environment showing early damage or change,
time-lapse feel through composition, [RENK] accent,
16:9 aspect ratio
```

**S17 — İlk Hasar**
```
First visible damage to [UYGAR] caused by [HAYVAN] —
destroyed crops / contaminated water / diseased livestock / 
disrupted trade / dead soldiers,
comic book illustration, dramatic scene,
shocked or confused [UYGAR] humans in frame,
[RENK] highlighting the damage area, 16:9 aspect ratio
```

**S18 — Yayılma Haritası**
```
Map showing [HAYVAN] spread across [UYGAR] territory,
illustrated map style, ink and parchment,
[RENK] spreading zones showing progression over time,
arrows and dates, empire borders visible and shrinking,
16:9 aspect ratio
```

**S19 — Toplum Tepkisi**
```
[UYGAR] people reacting to the growing crisis — market panic,
emergency council meeting, soldiers confused, farmers desperate,
comic book illustration, crowd scene,
chaos and disorder building, [RENK] danger lighting,
16:9 aspect ratio
```

**S20 — Hayvan Sürüsü**
```
Massive swarm / herd / colony of [HAYVAN] — hundreds visible,
bird's eye view or dramatic wide angle,
overwhelming [UYGAR] infrastructure below,
natural history book illustration, epic scale,
unstoppable force aesthetic, [RENK] accent, 16:9 aspect ratio
```

**S21 — Ekonomik Çöküş**
```
[UYGAR] trade or economy breaking down — empty market stalls,
abandoned fields, ships not moving, treasury depleted,
comic book illustration, emptiness and loss,
contrast with the earlier prosperity scene,
grey tones with [RENK] accent showing remaining value,
16:9 aspect ratio
```

**S22 — Askeri Zayıflama**
```
[UYGAR] military weakened or disrupted by [HAYVAN] —
soldiers sick / supply lines cut / horses dead / cavalry gone,
natural history book illustration, military camp scene,
weakness and vulnerability visible, contrast with earlier power,
[ATMOSFER2] weather reinforcing doom, 16:9 aspect ratio
```

**S23 — Dış Tehdit Fırsatı**
```
Enemy civilization seeing [UYGAR] weakness — 
rival army gathering / enemy general looking at maps /
opportunistic attack beginning,
comic book illustration, enemy perspective,
[UYGAR] city visible as vulnerable target in background,
[RENK] danger lighting, 16:9 aspect ratio
```

**S24 — Kritik Savaş veya Olay**
```
The decisive battle or event where [HAYVAN]'s impact becomes undeniable —
[UYGAR] forces overwhelmed, the moment of no return,
natural history illustration, epic battle or crisis scene,
chaos and scale, [HAYVAN] visible as cause,
[ATMOSFER2] intensified, [RENK] accent dramatic, 16:9 aspect ratio
```

**S25 — Birikimli Tahribat**
```
Accumulated damage — [UYGAR] city or farmland showing years of [HAYVAN] impact,
before/after split composition or decay progression,
comic book illustration, melancholy tone,
nature reclaiming or enemy advancing, 16:9 aspect ratio
```

**S26 — Geri Dönüşsüz An**
```
The moment the [UYGAR] ruling class realizes they cannot recover,
emperor / general / high priest looking at the destruction,
natural history book illustration, intimate emotional portrait,
[UYGAR] power symbols now broken or burning behind,
[ATMOSFER2], despair and recognition, 16:9 aspect ratio
```

---

### BÖLÜM 5 — DÖNÜM NOKTASI (6 prompt)

**S27 — Çöküş Zirvesi**
```
The peak moment of collapse — [UYGAR] at its most vulnerable,
comic book illustration, most dramatic composition in the video,
[HAYVAN] visible or implied as the cause,
[ATMOSFER2] at maximum intensity,
[RENK] dominant, cinematic peak composition, 16:9 aspect ratio
```

**S28 — Halk Kaçışı**
```
Mass exodus — [UYGAR] civilians fleeing city or region,
natural history book illustration, crowd in motion,
abandoned homes and possessions, desperation visible,
[HAYVAN] impact visible in environment they're fleeing,
16:9 aspect ratio
```

**S29 — Son Savunma**
```
Final desperate [UYGAR] defense attempt — soldiers fighting,
leaders making last decisions, rituals or prayers performed,
comic book illustration, siege or final stand,
contrast between human determination and inevitable [HAYVAN] force,
16:9 aspect ratio
```

**S30 — Hayvana Yakın Plan**
```
[HAYVAN] close-up again — triumphant, indifferent, still spreading,
natural history book illustration, animal portrait,
chaos of [UYGAR] collapse behind it, animal unaware of its impact,
ironic calm of a creature that changed history without knowing,
16:9 aspect ratio
```

**S31 — Düşman Girişi**
```
Enemy or successor force entering the weakened [UYGAR] capital,
comic book illustration, invasion scene,
[UYGAR] symbols being replaced or destroyed,
[HAYVAN] impact visible in the landscape — disease, famine, empty streets,
16:9 aspect ratio
```

**S32 — Yıkım Sonrası**
```
Aftermath — [UYGAR] city or territory in ruins, silence,
natural history book illustration, desolate landscape,
[HAYVAN] still present in the ruins, small and inconspicuous,
grey palette with single [RENK] still burning ember or lingering life,
16:9 aspect ratio
```

---

### BÖLÜM 6 — KARŞI ANLATI (4 prompt)

**S33 — Tarih Kitabı Sahnesi**
```
Old history book open to a page about [UYGAR] — 
the WRONG explanation illustrated — generals, wars, economics, but no [HAYVAN],
illustrated in comic book style, book pages with ink drawings,
dramatic light on the book from above, suggesting incompleteness,
16:9 aspect ratio
```

**S34 — Gerçek Ortaya Çıkıyor**
```
Split composition — left side: old narrative (armies / leaders / politics),
right side: the real story ([HAYVAN] as cause),
comic book illustration style, dramatic reveal composition,
[RENK] lighting on the true side, grey on the false side,
16:9 aspect ratio
```

**S35 — Kanıt Anı**
```
Archaeological or historical evidence of [HAYVAN]'s impact —
bones / grain records / DNA traces / written accounts / environmental data,
natural history book illustration, artifact close-up,
scholar or archaeologist examining evidence,
[RENK] highlight on the key evidence, 16:9 aspect ratio
```

**S36 — Akademik Karşılaştırma**
```
Side-by-side: traditional historian explaining common narrative 
vs scientific evidence pointing to [HAYVAN],
comic book illustration, two-panel contrast,
confident academic on left, compelling animal evidence on right,
audience stands between them, choosing sides, 16:9 aspect ratio
```

---

### BÖLÜM 7 — MİRAS (4 prompt)

**S37 — Bugünkü İz**
```
Modern day [location where UYGAR once stood] — 
ruins or transformed landscape, [HAYVAN] species still present,
photo-realistic illustration or contemporary art style,
past superimposed as ghost image over present,
continuity of [HAYVAN]'s biological presence, 16:9 aspect ratio
```

**S38 — Günümüz Paralelliği**
```
Modern situation echoing the same [HAYVAN] + civilization dynamic today,
comic book illustration but contemporary setting,
news headlines / urban environment / modern agriculture,
warning or relevance for today, [RENK] accent, 16:9 aspect ratio
```

**S39 — Hayvanın Zafer Anı**
```
[HAYVAN] portrait — calm, eternal, unchanged since [DÖNEM],
natural history book illustration, timeless specimen quality,
empires rise and fall around it, but this creature persists,
white or minimal background, creature in full glory,
16:9 aspect ratio
```

**S40 — Son Yorum**
```
Philosophical final image — [HAYVAN] and [UYGAR] ruins together,
tiny animal, vast collapsed empire behind,
natural history book illustration, melancholy and wonder,
quote space at bottom, wide shot, full context,
[RENK] sunset or dawn light, 16:9 aspect ratio
```

---

### B-ROLL BÖLÜMÜ (5 prompt)

**B01 — Dönem Sanat Eseri**
```
[DÖNEM] [UYGAR] artwork or artifact — pottery, fresco, mosaic, sculpture —
depicting [HAYVAN] or the civilization's daily life,
illustrated in documentary style, museum lighting,
educational context, artifact close-up with environmental context,
16:9 aspect ratio
```

**B02 — Coğrafi Bağlam**
```
Physical geography of [UYGAR] homeland — rivers, mountains, coast, plains,
illustrated map with topographic detail,
[HAYVAN] habitat zones marked, trade routes and city locations,
natural colors with [RENK] accent on key areas, 16:9 aspect ratio
```

**B03 — Hayvan Anatomi Plakası**
```
Scientific anatomy illustration of [HAYVAN] — labeled organs,
key biological features explaining its civilizational impact,
Victorian natural history atlas style, detailed ink,
white background, educational diagram aesthetic, 16:9 aspect ratio
```

**B04 — Zaman Çizelgesi**
```
Visual timeline — [UYGAR] rise and fall annotated with [HAYVAN] events,
illustrated infographic style, ink and parchment,
key dates marked, [HAYVAN] impact zones highlighted in [RENK],
clear visual causation from [HAYVAN] introduction to [UYGAR] collapse,
16:9 aspect ratio
```

**B05 — Karşılaştırma**
```
Split map — [UYGAR] territory before [HAYVAN] impact vs after,
same region, different eras, same map style,
[RENK] showing loss or change, stark before/after contrast,
labeled borders, illustrated ink map style, 16:9 aspect ratio
```

---

## ÇIKTI FORMATI

Kaydet: `wiki/beasttales/visuals/[konu-adı]-prompts.md`

```markdown
# [HAYVAN] × [UYGAR] — 45 Imagen4 Sahnesi

**Değişkenler:**
- HAYVAN: [species]
- UYGAR: [civilization]  
- DÖNEM: [dates]
- RENK: [accent color]
- ATMOSFER1: [opening atmosphere]
- ATMOSFER2: [climax atmosphere]

---
## S01 — HAYVAN GÖZÜ
[prompt]

## S02 — HAYVAN TAM VÜCUT
[prompt]
...tüm 45 sahne...
```

**Toplam:** 40 ana sahne + 5 B-roll = **45 prompt**
