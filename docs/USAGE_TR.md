# Medieval Narrative Generator Kullanım Rehberi

Bu rehber, proje çıktılarının nasıl üretileceğini ve günlük iş akışınıza nasıl entegre edileceğini Türkçe olarak adım adım açıklar.

## 1. Kurulum

1. Python 3.9 veya üzeri bir sürüm kullanın.
2. Depo klasöründe aşağıdaki komutu çalıştırın:
   ```bash
   pip install .
   ```
3. Kurulumdan sonra `medieval-generator --help` komutunun çalıştığını doğrulayın.

## 2. Temel Kullanım

Varsayılan komut, JSON formatında tam üretimi standart çıktıya yazar:

```bash
medieval-generator "Tema" "Video Başlığı"
```

- **Tema**: İçerik fikirlerini ve betiği yönlendirecek ana odak (ör. `Ortaçağ Kış Hayatta Kalma Taktikleri`).
- **Video Başlığı**: Hem anlatıyı hem de küçük resim istemini belirleyen başlık.

## 3. Önizleme (Hızlı Kontrol)

Tam 32.000 kelimelik metni beklemek istemiyorsanız `--preview` seçeneği yaklaşık %%5 oranında kısa bir betik üretir:

```bash
medieval-generator "Ortaçağ Kış Hayatta Kalma Taktikleri" \
  "How Medieval Villagers Slept Without Freezing" \
  --preview \
  --ideas-count 10 \
  --image-prompts 8 \
  --output preview.json
```

- `preview.json` dosyası, video fikirleri, kısa anlatım bölümleri ve görsel istemlerini içerir.
- İçerik tarzını hızlıca kontrol etmek veya uzun üretimden önce ses tonunu ayarlamak için idealdir.

## 4. Tam Üretim

32.000 kelime civarında bir betik için `--preview` kullanmayın. İsteğe göre kelime sayısını değiştirebilirsiniz:

```bash
medieval-generator "Frontier Winter Watch" \
  "How Frontier Families Survived The Coldest Nights" \
  --script-words 35000 \
  --ideas-count 25 \
  --image-prompts 28 \
  --output tam_cikti.json
```

### Çıktı İçeriği

- `ideas`: Viral potansiyeli yüksek video fikirleri listesi.
- `script`: Her biri başlık, gövde ve kelime sayısı ile birlikte uzun anlatım bölümleri.
- `image_prompts`: Belirtilen estetik yönergelere uygun 20-30 arası görsel istemi.
- `thumbnail_prompt`: YouTube küçük resmi için mizahi, çizgi stilinde ayrıntılı istem.

## 5. Çıktılarla Çalışma

1. **JSON'u metne dönüştürme**: Bölümleri tek dosyada birleştirmek için basit bir Python betiği kullanabilirsiniz:
   ```python
   import json
   data = json.load(open("tam_cikti.json", "r", encoding="utf-8"))
   with open("tam_metin.txt", "w", encoding="utf-8") as f:
       for section in data["script"]:
           f.write(section["title"] + "\n\n")
           f.write(section["body"] + "\n\n")
   ```
2. **Görsel üretimi**: `image_prompts` listesini MidJourney/Leonardo/Stable Diffusion gibi modellerde doğrudan kullanabilirsiniz.
3. **Küçük resim**: `thumbnail_prompt` çıktısı beyaz arka plan, abartılı ifadeler ve ortaçağ objeleri içeren çizgi stilini hedefler.

## 6. İleri Ayarlar

- `--seed`: Aynı girdilerle yeniden üretim yapmak için sabitlenebilir.
- `--ideas-count`: Daha fazla/az fikir üretmek için ayarlanabilir.
- `--image-prompts`: Video süresine göre görsel sayısını değiştirebilirsiniz.

## 7. Sorun Giderme

- Komut uzun sürüyorsa, önce `--preview` ile kontrol edin.
- Çıktı dosyası UTF-8 olarak kaydedilir; düzenlerken aynı kodlamayı kullanın.
- Kelime sayısı hedefi gereğinden uzun gelirse `--script-words` değerini düşürebilirsiniz.

Bu adımlar, aradığınız uzun, detaylı ve özgün ortaçağ temalı içerikleri hızlıca üretmenizi sağlar. Sorularınız varsa README'deki ek notlara göz atabilirsiniz.
