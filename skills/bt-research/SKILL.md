# Skill: bt-research — BeastTales Konu Zekası

## Tetikleyiciler
- `/bt-research` veya `araştır`
- `yeni konular bul`
- `find new topics for beasttales`
- `/bt-research sütun:1` → sadece hayvan gizemi konuları
- `/bt-research sütun:2` → sadece tarihi hayvan konuları

## TOKEN KURALI — SADECE 2 DOSYA OKU
```
1. channels/beasttales/profile.md   (~120 satır)
2. channels/beasttales/covered.md   (~35 satır)
```
Toplam ~155 satır. Başka hiçbir dosya okuma.

---

## ADIM 1 — SÜTUN BELİRLE

Varsayılan: Her araştırmada 8 Sütun-1 + 7 Sütun-2 konu üret (15 toplam).

---

## ADIM 2A — SÜTUN 1: HAYVAN GİZEMİ TARAMASI

Her hayvan için sor: *"Bu hayvan hakkında en çok yanlış anlaşılan davranış nedir? Kimse bunu YouTube'da tam ve doğru anlattı mı?"*

### Hayvan Kategorileri:
**Yaygın Ama Yanlış Anlaşılanlar:**
Kuzgunlar, baykuşlar, timsahlar, ahtapotlar, yılanlar, yarasalar, köpekbalıkları, aslanlar, kurtlar, tilkiler, karıncalar, arılar, örümcekler, çipmuks, sincaplar, rakun, opossum

**Egzotik + Az Bilinen:**
Platipüs, fossa, quokka, axolotl, tardigrade, mantis karidesi, pistol shrimp, mimic ahtapot, kör mağara balığı, elektrikli yılanbalığı, bal porsuku, su ayısı (tardigrade)

**Okyanus:**
Ahtapot, mürekkep balığı, yusufçuk larva, deniz salyangozu, balina, yunus, fok, mors

**Böcekler:**
Ateşböceği, güvelerin göç güdüsü, mayıs sineği, termit

### Sütun 1 Konu Kalıpları:
```
"Bu hayvan [davranış] yapıyor — bilim az önce gerçek sebebi buldu"
"[Hayvan] [yer/zaman] ne yapıyor — kimse fark etmedi"
"[Hayvan] aslında [yaygın inanç] değil — [gerçek bilgi]"
"[Hayvan] sizi [algılıyor/izliyor/değerlendiriyor] — [nasıl?]"
"[Hayvan] ölmeden önce [davranış] — neden hiç görmediniz?"
```

---

## ADIM 2B — SÜTUN 2: TARİHİ HAYVAN TARAMASI

Medeniyet listesini tara (covered.md'dekileri atla):
Mısır, Mezopotamya, Pers, Yunan şehir devletleri, Roma, Bizans, Arap Halifelikleri, Moğol İmparatorluğu, Osmanlı, Ming, Mughal, İnka, Aztek, Viking, Orta Çağ Avrupası, Haçlı devletleri, Güneydoğu Asya (Khmer, Majapahit), Rus İmparatorluğu, Japon feodal, Hollanda, Portekiz, Fransız sömürge, 1800–1950 modern dönüm noktaları

Hayvan kategorileri:
- **Ulaşım:** Eşek, katır, ren geyiği, lama, alpaka, su mandası
- **Hastalık vektörü:** Pire, bit, kene (non-tsetse), sinek türleri
- **Besin zinciri:** Spesifik balık, kuş, böcek, büyükbaş türleri
- **Savaş hayvanı:** Savaş domuzu, savaş arısı, savaş devesi, savaş yunus
- **Ekolojik:** İstilacı türler, tarım zararlıları, yok olan türler
- **Ekonomik:** Kunduz, su samuru, balina türleri, guano kuşu
- **Dini/sembolik:** Politikayı şekillendiren kutsal hayvanlar

---

## ADIM 3 — PUANLAMA (min 20/25)

Her aday için:
- Şok skoru (1-5): Kaç kişi bunu yanlış biliyor?
- Spesifik skor (1-5): Davranış/iddia ne kadar somut ve kanıtlı?
- Arama tetikleyici (1-5): İnsanlar bunu YouTube'da arıyor mu?
- Duygusal ağırlık (1-5): Merak/şaşırma/korku/bağ kuruyor mu?
- Benzersizlik (1-5): Bu açı YouTube'da yapıldı mı?

20 altı = at, kayıt tutma.

---

## ADIM 4 — BAŞLIK MÜHENDISLIĞI

Profile.md'deki formüllerden birini seç:

**SÜTUN 1 için:**
- FORMÜL A: "Why [Animal] [Does Behavior] — You've Been Watching Them Wrong"
- FORMÜL B: "The [Animal] Is Hiding [N] Secrets Nobody Ever Told You"
- FORMÜL C: "What [Animal] Actually Does [When] That You've Never Noticed"
- FORMÜL D: "The Real Reason [Animal] [Does X] — Science Just Discovered It"
- FORMÜL E: "If You See [Animal] Do This, Here's What It Actually Means"

**SÜTUN 2 için:**
- FORMÜL F: "What Really [Killed/Built/Destroyed] [Famous Thing] — It Wasn't [Common Belief]"
- FORMÜL G: "The [Animal] Nobody Talks About That [Collapsed/Built] [Empire]"
- FORMÜL H: "How [Small/Weak Animal] Defeated [Powerful Empire]"
- FORMÜL I: "The [Animal] [Civilization] Trusted — That Destroyed Them"
- FORMÜL J: "The Real Reason [FAMOUS EVENT] Happened (It Wasn't [Common Belief])"

---

## ÇIKTI FORMATI — HER KONU

```markdown
## KONU [N] — [SÜTUN 1: Hayvan Gizemi / SÜTUN 2: Tarihi Hayvan]

**HAYVAN:** [Türü — spesifik]
**KONU:** [Sütun 1: davranış gizemi / Sütun 2: medeniyet + dönem]
**ANA İDDİA:** [Tek cümle — bu hayvan tam olarak ne yaptı/yapıyor?]

**VİRAL BAŞLIK:** → [En iyi formül başlığı]
**ALTERNATİF A:** → [SEO odaklı — insanların aradığı]
**ALTERNATİF B:** → [Rakam şoku versiyonu]

**HOOK SATIRI:** [Videonun ilk cümlesi — en şok edici kanıtlanmış gerçek]

**NEDEN SIFIR REKABETİ VAR:**
[Rakip kanallar ne kapsadı — neden bu açıyı kaçırdılar]

**NEDEN ARIYORLAR:**
[Mevcut arama davranışı kanıtı]

**KARŞI ANLATI:**
- Herkes şunu biliyor: [X]
- BeastTales şunu ortaya koyuyor: [Y]

**VİRAL SKOR:** [X/25] → Şok:X | Spesifik:X | Arama:X | Duygu:X | Benzersiz:X

**SEO TAGLERI:** tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8

**ÜRETİM NOTU:** [En görsel çarpıcı sahne — tek cümle]
```

---

## ARAŞTIRMA SONU ÇIKTISI

**15 konu sonrası ekle:**

### ÖNCELİK SIRALAMA TABLOSU
| Sıra | Başlık | Skor | Sütun | Rekabet | Öncelik | Neden |

### İLK 3 DERİN DALMA
Her biri için:
- 6 senaryo bölüm başlığı
- Erken eklenecek merak tuzağı (open loop)
- Duygusal doruk anı (payoff reveal)
- Thumbnail konsepti

### İÇERİK TAKVİMİ (5 video, SEO momentum sırası)
Her video neden o sırada — önceki videonun SEO otoritesini nasıl inşa ediyor?

---

## Konu Kartı Kaydet
Her konu için: `wiki/beasttales/topics/[hayvan-konu].md`
İndex güncelle: `wiki/beasttales/index.md`
