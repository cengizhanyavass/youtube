# YouTube Creator Second Brain — Claude + Obsidian Vault

Bu vault BeastTales kanalı için tam üretim otomasyonudur.
**Obsidian'da doğrudan aç** — tüm bilgiler burada birikir.

---

## 🧠 İKİNCİ BEYİN: Her Oturumda Okuma Sırası

```
1. wiki/beasttales/hot.md          ← ÖNCE BU (aktif bağlam, ~30 satır)
2. channels/beasttales/covered.md  ← Tekrar etme (yayınlananlar)
3. İlgili skill dosyası            ← Göreve göre
```

**Asla** tüm wiki'yi yükleme. Sadece ihtiyaç duyulan 2-3 dosya.

---

## 🎬 BeastTales Kanal Beyin

### Referans Dosyalar (sadece gerektiğinde oku)
```
channels/beasttales/profile.md       ← Kanal DNA: ses tonu, stil, kriterler
channels/beasttales/covered.md       ← Yayınlanan konular — ASLA TEKRAR ETME
channels/beasttales/competitors.md   ← Rakip kanal takibi
channels/beasttales/seo-veri.md      ← VidIQ keyword verileri (Mayıs 2026)
channels/beasttales/trend-raporu.md  ← VidIQ trend analizi
channels/beasttales/gorsel-stil.md   ← Görsel şablonlar (Midjourney + Imagen4)
```

---

## ⚡ Komutlar

| Komut | Ne Yapar | Okur | Yazar |
|-------|---------|------|-------|
| `/bt-research` | 15 benzersiz konu bulur, puanlar | profile + covered | wiki/topics/ + index |
| `/bt-script [konu]` | 13dk senaryo yazar | profile + topic card | wiki/scripts/ |
| `/bt-visuals [konu]` | **45 Imagen4 sahnesi** üretir | topic card | wiki/visuals/ |
| `/bt-thumbnail [konu]` | 3 thumbnail konsepti | profile + topic card | wiki/thumbnails/ |
| `/bt-produce [konu]` | Senaryo + 45 görsel + thumbnail | topic card | hepsi |

### Türkçe Tetikleyiciler (aynı sonucu verir)
```
"araştır"       → /bt-research
"senaryo yaz"   → /bt-script
"görseller üret"→ /bt-visuals  
"thumbnail"     → /bt-thumbnail
"üret"          → /bt-produce
```

---

## 📁 Wiki Yapısı

```
wiki/beasttales/
├── hot.md              ← ÖNCE OKU — aktif bağlam
├── index.md            ← Konu bankası tablosu
├── pipeline.md         ← Üretim takibi
├── topics/             ← Bireysel konu kartları
├── scripts/            ← Tam senaryolar
├── visuals/            ← 45 Imagen4 prompt seti
└── thumbnails/         ← Thumbnail konseptleri
```

---

## 🔄 Tam Üretim İş Akışı

```
1. /bt-research
   → 15 yeni konu kartı → wiki/beasttales/topics/
   → Öncelik tablosu → hangi konu önce çekilecek

2. /bt-produce [konu-adı]
   → Senaryo (1900 kelime, 8 bölüm) → wiki/scripts/
   → 45 Imagen4 sahnesi → wiki/visuals/
   → 3 thumbnail konsepti → wiki/thumbnails/

3. Yükleme sonrası:
   → covered.md güncelle (el ile ekle)
   → hot.md güncelle
   → pipeline.md işaretle

4. Tekrar /bt-research (asla önceki konuları önermez)
```

---

## 🎨 Görsel Sistem

### İki Stil:
- **STİL A — Çizgi Roman** (Red Panda / Known By Birds): thumbnail + açılış sahneleri
- **STİL B — Doğal Tarih**: B-roll, harita, anatomi sahneleri

### 45 Sahne Dağılımı:
```
Soğuk Açılış:      S01–S04   (4 sahne)
Dünyanın Öncesi:   S05–S09   (5 sahne)
Hayvanı Tanıyalım: S10–S14   (5 sahne)
Nedensellik:       S15–S26  (12 sahne)
Dönüm Noktası:     S27–S32   (6 sahne)
Karşı Anlatı:      S33–S36   (4 sahne)
Miras:             S37–S40   (4 sahne)
B-Roll:            B01–B05   (5 sahne)
TOPLAM: 45 sahne
```

### Token Verimliliği:
Her skill SADECE topic card okur (~40 satır).
Tüm şablonlar skill içinde gömülü — ek dosya okuma yok.

---

## 🔍 SEO Stratejisi (VidIQ Verisi)

**Ana Hedef Kelime:** `animals that changed history`
- Rekabet: 30.7 (ÇOK DÜŞÜK)
- Aylık arama: 5,025
- Her videoda kullan → kanal otoritesi birikir

**Başlık Formülü:**
```
"The [ANIMAL] That [DESTROYED/BUILT/CHANGED] [CIVILIZATION]"
```

**Tag Katmanları (her videoda):**
```
Katman 1: animals that changed history, history of animals
Katman 2: animal documentary, wildlife documentary
Katman 3: [spesifik medeniyet], ancient history
```

---

## 🛠️ Araçlar

```
tools/claude-youtube/    ← Kanal denetimi, SEO, analitik (14 komut)
tools/shortgpt/          ← YouTube Shorts otomasyonu
tools/money-printer/     ← Shorts üretici (yerel AI, ücretsiz)
tools/money-printer-v2/  ← Tam otomasyon + zamanlama
tools/faceless-video/    ← Yüzsüz video üretimi
tools/advertools/        ← YouTube SEO analizi
tools/viral-shorts/      ← Viral Shorts jeneratörü
tools/youtube-mcp/       ← YouTube API'si (40 araç)
```

---

## 📚 Genel Wiki (BeastTales dışı içerikler)

```
.raw/           ← Kaynak belgeler (değiştirme)
wiki/           ← Claude üretimi bilgi bankası
_templates/     ← Obsidian şablonları
```

Kaynak yükle: `.raw/` klasörüne koy → "ingest [dosya adı]" de

Soru sor: "query: [soru]"
Wiki sağlığı: "lint the wiki"
Oturumu kaydet: "/save"
