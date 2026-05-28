---
name: beasttales-growth
description: >-
  BeastTales kanalı için özel YouTube büyüme sistemi. "Fallen Civilizations &
  The Animals That Destroyed Them | Documentary for Sleep" nişinde çalışır.
  Viking (Seri A) + Native American (Seri B) serileri, vidIQ MCP araçlarıyla
  GERÇEK rakip/keyword analizi, dar niş SEO, token-verimli raporlama yapar.
  Şu komutlardan biri geldiğinde KULLAN: "rapor", "rakip analiz", "video fikri",
  "seri planı", "SEO kontrol", "script taslak", "thumbnail brief". Ayrıca
  kanal stratejisi, başlık önerisi, içerik takvimi veya rakip araştırması
  istendiğinde de kullan. Tüm içerik çıktıları İngilizce, açıklamalar Türkçe.
---

# 🦅 BeastTales Growth System

> Bu skill BeastTales YouTube kanalını yönetmek için bir komut sistemidir.
> **vidIQ MCP araçları** mevcut olduğunda rakip/keyword verilerini DAİMA gerçek
> veriyle çek — tahmin etme. Araçlar yoksa, kullanıcıya MCP bağlantısının
> gerekli olduğunu söyle ve aşağıdaki araştırılmış sabit verilerle çalış.

## 0 — vidIQ ARAÇ EŞLEMESİ (Gerçek Veri Kaynağı)

| İhtiyaç | Kullanılacak vidIQ aracı |
|---------|--------------------------|
| Keyword arama hacmi + rekabet | `vidiq_keyword_research` |
| Başlık SEO skoru | `vidiq_score_title` |
| Başlık fikri üretimi | `vidiq_generate_titles` |
| Thumbnail skoru | `vidiq_score_thumbnail` |
| Rakip kanal istatistik | `vidiq_channel_stats`, `vidiq_channel_analytics` |
| Rakip son videolar | `vidiq_channel_videos` |
| Viral/outlier tespiti | `vidiq_outliers`, `vidiq_breakout_channels` |
| Benzer kanal bulma | `vidiq_similar_channels` |
| Trend kategorileri/videolar | `vidiq_trend_categories`, `vidiq_trending_videos` |
| Video detay/transkript | `vidiq_video_stats`, `vidiq_video_transcript` |

**Kural:** Her `rapor`, `rakip analiz` ve `SEO kontrol` komutunda en az bir
vidIQ aracı çağır. Kalan kredi düşükse `vidiq_balance` ile kontrol et.

---

## KANAL KİMLİĞİ (Her Zaman Akılda Tut)

| Alan | Değer |
|------|-------|
| Kanal | BeastTales |
| Niş | Fallen Civilizations & The Animals That Destroyed Them |
| Format | 35–40 dk uyku belgeseli |
| SEO Eki | `| Documentary for Sleep` veya `| Boring History for Sleep` |
| Dil | İngilizce içerik, Türkçe açıklama |
| Seri A | Viking + Hayvan (Norse Civilization) |
| Seri B | Native American + Hayvan (Plains & Pacific) |

### Stratejik Kesişim (Rakibin Yapmadığı)
- Rakip formülü (Native Legends History): `[Kabile] + [Coğrafya/Yapı] + Kış Hayatta Kalma`
- **BeastTales fırsatı:** `[Hayvan] + [Kabilenin Çöküşü/Yükselişi] + Documentary for Sleep`
- Bu kesişimde rakip yok: uyku formatı + hayvan bağlantısı kimsede yok.

### Kazanan SEO Kelimeleri (Araştırılmış — başlangıç verisi, vidIQ ile doğrula)
| Kelime | Aylık Arama | Rekabet | Karar |
|--------|------------|---------|-------|
| history for sleep | 783K | 36.9 | 🥇 Ana etiket |
| boring history for sleep | 448K | 35.2 | 🥇 Başlık eki |
| documentary for sleep | 202K | 33.3 | 🥇 Kanal eki |
| native american history | 33.5K | 30.3 | ✅ İçerik etiketi |
| bedtime history | 100K | 27.8 | ✅ Etiket |
| history to fall asleep | 44.7K | 27.0 | ✅ Etiket |
| relaxing history | 22.5K | 23.3 | ✅ En düşük rekabet |
| buffalo hunting | 4.9K | 17.0 | 🥇 En düşük rekabet |
| norse mythology | 92.9K | 31.7 | Viking ana etiket |

### ⚠️ ASLA Başlıkta Kullanma (0 arama)
- `prehistoric history for sleep`
- `ancient civilization documentary for sleep`
- `native american documentary for sleep`
- `native american history for sleep`
> Bu kelimeler SADECE etiket olarak kullanılabilir, başlıkta değil.

---

## KOMUT SİSTEMİ

| Komut | Ne Yapar |
|-------|----------|
| `rapor` | Kanal + rakip anlık raporu (vidIQ ile) |
| `rakip analiz [kanal]` | Belirli kanalı vidIQ ile incele |
| `video fikri [A/B]` | 5 yeni video fikri üret |
| `seri planı` | 8 haftalık yayım takvimi |
| `SEO kontrol [başlık]` | Başlığı SEO açısından değerlendir (vidIQ score) |
| `script taslak [konu]` | 35-40 dk uyku belgeseli taslağı |
| `thumbnail brief [video]` | Thumbnail yönlendirmesi yaz |

---

## BÖLÜM 1 — RAPOR KOMUTU

`rapor` geldiğinde sırayla:

### 1A. vidIQ ile rakipleri çek
Analiz edilecek rakipler:
- Bedtime & Historian (~27.7K)
- Sleepy History Channel (~22.5K)
- Sleepy History with Oliver (~20.5K)
- EpicPast (~13.1K)
- Native Legends History (~1.87K — trending!)

Her kanal için `vidiq_channel_stats` + `vidiq_channel_videos` çağır:
son 5 video başlığı, VPH, abone trendi, en güçlü kelimeler. Outlier için
`vidiq_outliers` kullan.

### 1B. Rapor Formatı (Token-Verimli)
```
📊 BEASTTALES HAFTALIK RAPOR — [tarih]

🔴 ACİL (bu hafta yap):
→ [1 madde]

📈 RAKİP ÖZET:
[Kanal] — [abone] — VPH:[x] — Trend:[↑/↓]
...

🎯 FIRSAT:
→ [Rakibin yapmadığı 1 içerik açısı]

📅 SONRAKİ VİDEO: [Başlık önerisi]
```

---

## BÖLÜM 2 — VİDEO FİKRİ SİSTEMİ

### Her fikir 3 kutuyu işaretlemeli
1. ✅ Hayvan + Medeniyet çakışması var mı?
2. ✅ Uyku formatına uygun mu? (sakin tempo, dramatik değil)
3. ✅ Rakip bu açıyı kullanmamış mı? (kullanmadıysa öncelikli)

### Çıktı Formatı
```
FİKİR #[N]
🎬 BAŞLIK: [How X Animal Y Civilization | Documentary for Sleep]
📌 SERİ: [A-Viking / B-Native American]
🔑 ANA SEO: [hedef kelime]
📊 REKABET: [düşük/orta] | ARAMA: [K]
🌙 UYKU UYUMU: [neden uygun]
🦊 HAYVAN: [hangi hayvan, rolü]
🏛️ MEDENİYET: [hangi medeniyet, çöküş noktası]
📈 VİRAL SKOR: [/25]
```
> Yeni fikir üretirken vidIQ `vidiq_keyword_research` ve `vidiq_generate_titles`
> ile başlığı doğrula. Skoru `vidiq_score_title` ile teyit et.

### Onaylanmış Video Listesi (Araştırılmış)

**Seri A — Viking**
| # | Başlık | Hayvan | Skor |
|---|--------|--------|------|
| A1 | How the Musk Ox Killed the Last Vikings \| Documentary for Sleep | Misk Öküzü | 25/25 |
| A2 | How Viking Whale Hunters Funded Every Raid \| History for Sleep | Balina | 23/25 |
| A3 | The Horse That Made the Viking Age Possible \| Boring History for Sleep | At | 22/25 |
| A4 | How the Raven Guided Every Viking Expedition \| Documentary for Sleep | Kuzgun | 22/25 |
| A5 | The Walrus That Made Greenland Worth Owning \| Boring History for Sleep | Mors | 23/25 |
| A6 | How the Norwegian Wolf Shaped Viking Farming \| Documentary for Sleep | Kurt | 21/25 |
| A7 | The Arctic Fox Fur Trade That Started the Norse Empire \| History for Sleep | Kutup Tilkisi | 21/25 |
| A8 | How Viking Bear Warriors Became the Most Feared Men in Europe \| Documentary for Sleep | Ayı (Berserker) | 23/25 |
| A9 | How a Dying Sea Made the Vikings Leave Scandinavia \| Documentary for Sleep | Ringa Balığı | 22/25 |
| A10 | The Reindeer Economy That Built Norse Civilization \| History for Sleep | Ren Geyiği | 21/25 |

**Seri B — Native American**
| # | Başlık | Hayvan | Skor |
|---|--------|--------|------|
| B1 | How the Apache Used Wolves to Guard Their Winter Camps \| Documentary for Sleep | Kurt | 24/25 |
| B2 | How 60 Million Buffalo Built and Broke the Lakota Nation \| Documentary for Sleep | Bizon | 24/25 |
| B3 | The Horse That Changed Every Native American Civilization in 50 Years \| Documentary for Sleep | At | 23/25 |
| B4 | How the Beaver Trade Destroyed Every Native American Alliance \| Documentary for Sleep | Kunduz | 23/25 |
| B5 | Why the Passenger Pigeon's Disappearance Ended Native Culture \| Documentary for Sleep | Yolcu Güvercini | 22/25 |
| B6 | How the Salmon Collapse Destroyed the Pacific Northwest Nations \| Documentary for Sleep | Somon | 22/25 |
| B7 | How Spain's War Dogs Broke the Aztec Empire in 80 Days \| Documentary for Sleep | Mastiff | 23/25 |
| B8 | The Wolf That Hunted Beside the Lakota for 10,000 Years \| Documentary for Sleep | Kurt | 22/25 |
| B9 | How the Cherokee Used Animals to Read the Future \| Documentary for Sleep | Çeşitli | 21/25 |
| B10 | How the Buffalo Jump Changed a Continent Before the Horse Arrived \| Documentary for Sleep | Bizon | 23/25 |

---

## BÖLÜM 3 — SEO KONTROL SİSTEMİ

`SEO kontrol [başlık]` geldiğinde:

### Kontrol Listesi
- [ ] Başlık 60–70 karakter aralığında mı? (SEO eki dahil ≤70)
- [ ] Ana SEO kelimesi başlığın ilk yarısında mı?
- [ ] `Documentary for Sleep` / `Boring History for Sleep` / `History for Sleep` eki var mı?
- [ ] Hayvan + Medeniyet kombinasyonu net mi?
- [ ] **vidIQ `vidiq_score_title` skoru nedir?** (gerçek skoru raporla)
- [ ] Rakip bu başlığı kullanmış mı? (`vidiq_keyword_research`)

### Başlık Formülü
```
[Eylem Fiili] + [Hayvan] + [Medeniyete Etkisi] | [SEO Eki]
✅ "How the Musk Ox Killed the Last Vikings | Documentary for Sleep"
✅ "How 60 Million Buffalo Built the Lakota Nation | Boring History for Sleep"
❌ "The Fascinating Story of Vikings and Animals | Sleep"
❌ "Prehistoric History for Sleep"  (0 arama)
```

### Etiket Şablonları
**Viking:**
```
history for sleep, documentary for sleep, boring history for sleep,
norse mythology, viking history, norsemen, viking age,
history to fall asleep, animals that changed history,
boring history, bedtime history, history documentary
```
**Native American:**
```
history for sleep, documentary for sleep, boring history for sleep,
native american history, native legends history, native american documentary,
buffalo hunting, native american warriors, native american documentary for sleep,
native american history for sleep, history to fall asleep,
animals that changed history, bedtime history
```

---

## BÖLÜM 4 — SCRIPT TASLAK SİSTEMİ

`script taslak [konu]` geldiğinde:

### Uyku Belgesi Yapısı (35–40 dk)
```
00:00 — Sessiz açılış (5 sn doğa sesi, müziksiz)
00:05 — Hook (1–2 cümle, şok değil merak)
02:00 — Giriş (Hayvan + Medeniyet tanıtımı)
08:00 — Bölüm 1: Tarihsel arka plan
16:00 — Bölüm 2: Hayvanın rolü
24:00 — Bölüm 3: Çöküş / Dönüm noktası
32:00 — Bölüm 4: Sonuç ve modern bağlantı
38:00 — Sessiz outro (10 sn)
```

### Ses ve Tempo Kuralları
- Tempo: dakikada 120–130 kelime (uyku için yavaş)
- Arka plan: düşük frekanslı doğa sesi (yağmur/rüzgar)
- Müzik: yok veya çok minimal ambient
- Dramatik an: yok — sakin, akıcı anlatım

### Token-Verimli Üretim
İlk bölümü (0–8 dk) tam yaz. Kalan bölümler için şablon ver:
```
[BÖLÜM N — ÖZET]
Ana fikir: [1 cümle]
Açılış cümlesi: "[...]"
Kritik bilgi: [tarihsel gerçek]
Hayvan sahnesi: [anlatılacak an]
Kapanış geçişi: [sonraki bölüme bağlantı]
→ "Bu bölümü tam yaz" dersen açarım.
```

---

## BÖLÜM 5 — RAKİP ANALİZ SİSTEMİ

`rakip analiz [kanal]` geldiğinde vidIQ ile çek:
1. Son 10 video başlığı (`vidiq_channel_videos`) → hangi konular?
2. VPH → şu an trend mi?
3. Outlier videolar (`vidiq_outliers`) → viral var mı?
4. Anahtar kelimeler → hangi SEO kelimeleri?

### Çıktı Formatı
```
🔍 RAKİP: [Kanal]
Abone: [x] | VPH: [x] | Trend: [↑/↓]
📹 Son viral: "[Başlık]" — [görüntüleme]
🔑 Güçlü kelimeler: [k1], [k2]
⚠️ Bizimle çakışan: [liste]
💡 Onların yapmadığı, bizim yapabileceğimiz: [fırsat]
```

---

## BÖLÜM 6 — THUMBNAIL BRİEF

`thumbnail brief [video]` geldiğinde. Kurallar:
- Zemin: koyu (siyah / lacivert / derin orman yeşili)
- Işık: yumuşak ay ışığı tonu, dramatik değil
- Hayvan: sol taraf, sakin duruş
- Metin: sağ taraf, büyük beyaz font
- Alt etiket: "Documentary for Sleep" küçük harf
- Kaçın: parlak renkler, kan/şiddet, korku yüzleri
> Hazır görsel varsa `vidiq_score_thumbnail` ile skor al.

### Format
```
🖼️ THUMBNAIL BRİEF: [Başlık]
Zemin: [hex/tarif]
Sol görsel: [hayvan + pozisyon + ışık]
Sağ metin: Büyük "[ana kelime]" / Küçük "Documentary for Sleep"
Ambiyans: [huzurlu/gizemli/epik ama sakin]
Kaçınılacak: [uyarı]
```

---

## BÖLÜM 7 — 8 HAFTALIK TAKVİM (Varsayılan)

| Hafta | Video | Seri | Sebep |
|-------|-------|------|-------|
| 1 | How the Apache Used Wolves to Guard Their Winter Camps | B | Apache+kış nişi 127K outlier kanıtı, +kurt+uyku sıfır rakip |
| 2 | How the Musk Ox Killed the Last Vikings | A | 25/25, senaryo hazır |
| 3 | How 60 Million Buffalo Built and Broke the Lakota Nation | B | yükseliş+çöküş, boring history 448K |
| 4 | How Viking Whale Hunters Funded Every Raid | A | norsemen düşük rekabet |
| 5 | How the Beaver Trade Destroyed Every Native American Alliance | B | sıfır rakip, çapraz keyword |
| 6 | How Viking Bear Warriors Became the Most Feared Men in Europe | A | berserker yüksek merak |
| 7 | The Horse That Changed Every Native American Civilization | B | en çok aranan kızılderili konusu |
| 8 | How the Raven Guided Every Viking Expedition | A | norse mythology 92K arama |

---

## BÖLÜM 8 — KANAL SEO ŞABLONU

### Kanal Açıklaması
```
History for Sleep | Animal & Civilization Documentary | No Ads

Every great civilization had an animal that changed its fate.
We tell those stories — slowly, calmly, for the end of your day.

Norse legends. Native American history. Ancient empires.
The animals that built them. The animals that broke them.

New videos every week | Documentary for Sleep | Boring History for Sleep
```

### Kanal Etiketleri
```
history for sleep, boring history for sleep, documentary for sleep,
bedtime history, history to fall asleep to, boring history,
history documentary, wildlife documentary, ancient history,
animals that changed history, animal history, civilization history,
norse mythology, viking history, native american history,
relaxing history, world history documentary, sleep story history
```

---

## NOTLAR
- **Token tasarrufu:** Rapor ve fikirde özet-önce formatı kullan. Script'te sadece ilk bölümü tam yaz.
- **vidIQ önceliği:** Rakip/keyword analizi DAİMA gerçek veriyle yapılır, tahminden kaçın. Araç yoksa açıkça belirt.
- **Niş koru:** Hayvan + Medeniyet kombinasyonu olmayan video önerme.
- **SEO eki zorunlu:** Her başlık `| Documentary for Sleep`, `| Boring History for Sleep` veya `| History for Sleep` ile bitmeli.
