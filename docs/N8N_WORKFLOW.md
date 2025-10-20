# n8n İş Akışı: Medieval YouTube Otomasyonu

Bu belge, `docs/workflows/youtube_automation.json` dosyasında verilen n8n iş akışını kurup çalıştırmak için gerekli adımları açıklar. İş akışı, günlük olarak tetiklenerek tema belirleme, betik üretimi, görsel oluşturma ve Google Drive'a aktarım süreçlerini otomatik hale getirir. Seslendirme, video montajı ve YouTube yükleme adımları manuel olarak yürütülmek üzere bir görev listesi oluşturur.

## Hızlı Başlangıç (Özet)

1. n8n'i başlatın (masaüstü uygulaması, Docker ya da `n8n start`).
2. Sol menüden **Credentials** bölümüne girerek:
   - OpenAI anahtarınızı içeren bir **OpenAI** credential oluşturun.
   - Google Drive OAuth credential'ınızı ekleyin.
3. **Workflows → Import from File** ile `docs/workflows/youtube_automation.json` dosyasını içeri aktarın.
4. İş akışı açıldığında tüm nodelar için doğru credential'ları seçin ve gerekli klasör ID'lerini alanlara yazın.
5. Sağ üstten **Execute Workflow** butonuna basarak testi yapın. (İlk denemede hata alırsanız eksik credential veya klasör ID'lerini düzeltip yeniden çalıştırın.)

Detaylı kurulum için aşağıdaki adımları uygulayın.

## 1. Gereksinimler

- Python 3.9+ ve bu depo için `pip install .`
- OpenAI API anahtarı (`OPENAI_API_KEY`)
- (Opsiyonel) Anthropic veya farklı modeller için ek anahtarlar
- Google Cloud projesi ve OAuth istemcisi ile yapılandırılmış Google Drive API erişimi
- n8n v1.20+ (CLI veya Docker)
- (Opsiyonel) DALL·E görüntü üretimi için OpenAI erişimi

## 2. n8n Ortam Değişkenleri

İş akışında kullanılan klasör ID'lerini ve kimlik bilgisi referanslarını ortam değişkeni olarak tanımlayın. `~/.n8n/.env` dosyasına veya Docker çalıştırma parametrelerine şu değerleri ekleyin:

```bash
# Google Drive klasörleri
export N8N_GDRIVE_SCRIPTS_FOLDER="<Scripts klasör ID>"
export N8N_GDRIVE_IMAGES_FOLDER="<Images klasör ID>"
export N8N_GDRIVE_THUMBNAILS_FOLDER="<Thumbnails klasör ID>"
export N8N_GDRIVE_PROJECTS_FOLDER="<Projects klasör ID>"

# Google Drive OAuth kimlik bilgisi kaydının n8n içindeki ID değeri
export N8N_GOOGLE_DRIVE_CREDENTIAL_ID="<n8n credential id>"

# OpenAI anahtarı (n8n genel .env veya credentials kullanabilirsiniz)
export OPENAI_API_KEY="sk-..."
```

n8n'in Docker ile çalışması halinde komut örneği:

```bash
docker run -it --rm --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v /path/to/this/repo:/workspace/youtube \
  --env-file ~/.n8n/.env \
  n8nio/n8n
```

> `medieval-generator` komutunun n8n konteynerinde bulunması için `pip install /workspace/youtube` komutunu n8n kabuğunda çalıştırın.

## 3. Klasör Yapısı

Google Drive tarafında aşağıdaki klasörleri oluşturup ID'lerini alın ve ortam değişkenlerine atayın:

```
YouTube_Otomasyon/
├── Scripts/
├── Images/
├── Projects/
├── Thumbnails/
└── Final_Videos/
```

`Final_Videos` klasörü iş akışında sadece görev listesinde referans edilir; manuel yüklemeler içindir.

## 4. İş Akışını İçeri Aktarma

1. n8n arayüzünde **Workflows → Import from File** seçeneğini kullanın.
2. `docs/workflows/youtube_automation.json` dosyasını seçin.
3. İş akışı açıldığında aşağıdaki adımları doğrulayın:
   - **Topic Planner** ve görsel oluşturma düğümlerinde OpenAI kimlik bilgisi seçilmiş olmalı.
   - Google Drive düğümleri, oluşturduğunuz OAuth kimlik bilgisi kaydını kullanmalı.
   - `Generate Assets` düğümü n8n sunucusunda `medieval-generator` komutuna erişebilmeli.

## 5. İş Akışı Aşamaları

1. **Daily Trigger**: Her gün 09:00'da çalışır (zon: `Europe/Istanbul`).
2. **Topic Planner**: OpenAI Chat API'siyle tema, başlık ve çıktı parametrelerini JSON olarak belirler.
3. **Generate Assets**: `medieval-generator` CLI komutunu çalıştırarak fikirler, betik bölümleri, görsel istemleri ve küçük resim istemi üretir.
4. **Upload Script**: JSON çıktısını Google Drive `Scripts/` klasörüne yükler.
5. **Create Checklist**: Manuel yapılacak işleri içeren Markdown dosyasını `Projects/` klasörüne kaydeder.
6. **Prepare Image Prompts → Render Scene → Upload Scene**: Görsel istemlerini tek tek DALL·E (gpt-image-1) üzerinden oluşturur ve `Images/` klasörüne yükler.
7. **Prepare Thumbnail Prompt → Render Thumbnail → Upload Thumbnail**: Thumbnail görselini üretip `Thumbnails/` klasörüne aktarır.

Her çalıştırmada dosya isimleri otomatik olarak video başlığından türetilen slug ile oluşturulur.

## 6. Manuel Süreç

İş akışı sonunda Google Drive'a yüklenen `*-checklist.md` dosyası, seslendirme, kurgu ve final video yükleme adımlarının hatırlatıcısıdır. Seslendirme dosyalarını ve tamamlanan videoyu elle `Projects/` ve `Final_Videos/` klasörlerine yerleştirin. YouTube yüklemesini manuel olarak tamamlayın.

## 7. Test ve İzleme

- İş akışını elle çalıştırmadan önce `Topic Planner` ve `Generate Assets` düğümlerini ayrı ayrı test edin.
- Görsel düğümleri OpenAI kota kullanımına tabidir; hata durumunda `Split Image Batches` düğümündeki batch boyutunu artırarak yeniden çalıştırabilirsiniz.
- Hata alan çalıştırmalar n8n'in **Executions** sekmesinden yeniden denenebilir.

## 8. Güvenlik Notları

- API anahtarlarını yalnızca n8n credential sistemi veya ortam değişkenleri üzerinden girin; düğüm parametrelerine düz metin olarak yazmayın.
- Google Drive kimlik bilgisi OAuth istemcisinin yalnızca gereken kapsamlarla sınırlı olduğundan emin olun (`https://www.googleapis.com/auth/drive.file`).

Bu yapılandırma ile günlük olarak yeni ortaçağ temalı YouTube proje paketleri oluşturabilir, görselleri hazırlar ve manuel prodüksiyon adımlarını hızlandırabilirsiniz.
