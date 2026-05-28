# BeastTales — YouTube Otomasyon Sistemi

Bu repo, **BeastTales** kanalı için bir Claude Code skill'i içerir:
`.claude/skills/beasttales-growth/SKILL.md`

## Niş
**Fallen Civilizations & The Animals That Destroyed Them | Documentary for Sleep**
- Seri A: Viking + Hayvan
- Seri B: Native American + Hayvan
- Format: 35–40 dk uyku belgeseli, İngilizce içerik / Türkçe açıklama

## Nasıl Kullanılır
Claude Code oturumunda şu komutları yaz — skill otomatik tetiklenir:

| Komut | İşlev |
|-------|-------|
| `rapor` | Kanal + rakip haftalık raporu (vidIQ) |
| `rakip analiz [kanal]` | Bir rakibi vidIQ ile incele |
| `video fikri [A/B]` | 5 yeni video fikri |
| `seri planı` | 8 haftalık takvim |
| `SEO kontrol [başlık]` | Başlığı vidIQ ile skorla |
| `script taslak [konu]` | Uyku belgeseli taslağı |
| `thumbnail brief [video]` | Thumbnail yönlendirmesi |

## Gerçek Veri
Sistem, mevcut olduğunda **vidIQ MCP araçlarını** kullanır (keyword research,
outliers, channel analytics, score title/thumbnail, generate titles). Veriler
tahmin değil, çekilen gerçek değerlerdir.
