# Travel Guide Video Uretimi

[MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (MIT) uzerine
kurulu, gunde bir travel guide videosu ureten otomasyon. Script LLM ile yazilir,
seslendirme Edge TTS ile ucretsiz yapilir, goruntuler Pexels'ten cekilir ve
FFmpeg ile birlestirilir.

## Kurulum

```bash
export PEXELS_API_KEYS="senin-anahtarin"      # ucretsiz: pexels.com/api
export OPENAI_API_KEY="senin-anahtarin"       # ya da ANTHROPIC / GEMINI / DEEPSEEK / MOONSHOT
./scripts/setup.sh
```

`setup.sh` MoneyPrinterTurbo'yu `.mpt/` altina klonlar, kendi sanal ortamini
kurar ve `config.toml` dosyasini bu anahtarlarla yazar. Sistemde `ffmpeg` yoksa
`imageio-ffmpeg` ile gelen statik binary'yi kullanir.

## Video uretme

```bash
./scripts/daily_video.py                        # gunun konusu
./scripts/daily_video.py --topic "Two Days in Seville"
./scripts/daily_video.py --topic "Lisbon" --script "$(cat metin.txt)"
```

Cikti `output/2026-08-27-konu-adi.mp4` seklinde kaydedilir.

LLM anahtarin yoksa `--script` ile metni kendin verebilirsin; o zaman sadece
Pexels anahtari gerekir.

## Gunluk otomasyon

`.github/workflows/daily-video.yml` her gun 06:00 UTC'de (TR saatiyle 09:00)
calisir ve videoyu Actions artifact'i olarak yukler. Repo ayarlarindan sunlari
secret olarak ekle:

| Secret | Zorunlu | Ne ise yarar |
| --- | --- | --- |
| `PEXELS_API_KEYS` | evet | Stok goruntu (`PIXABAY_API_KEYS` de kabul edilir) |
| `OPENAI_API_KEY` | script icin | Script uretimi |
| `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` / `DEEPSEEK_API_KEY` / `MOONSHOT_API_KEY` | alternatif | Ilk bulunan kullanilir |

Actions sekmesinden **Run workflow** ile elle de tetikleyebilir, o calistirmaya
ozel konu ve ses verebilirsin.

## Konu listesi

`topics/travel_topics.txt` icindeki satirlardan gunun konusu tarihe gore
sirayla secilir. Satir eklemek yeterli; imlec dosyasi tutulmuyor, bu yuzden ayni
gun iceginde tekrar calistirmak ayni videoyu uretir.

## Ayarlar

Kadraj, gecisler, font ve muzik seviyesi `scripts/daily_video.py` icindeki
`PRESET` listesinde. Ses icin Edge TTS isimleri kullanilir, ornegin
`en-GB-RyanNeural-Male` veya `en-US-AriaNeural-Female`.

## Maliyet

Pexels, Edge TTS ve FFmpeg ucretsiz. GitHub Actions public repo'da ucretsiz.
Geriye sadece script icin kullanilan LLM cagrilari kaliyor; gunde bir video
icin aylik birkac dolar.
