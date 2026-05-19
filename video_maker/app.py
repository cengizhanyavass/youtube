import os
import shutil
import tempfile
import time
from pathlib import Path

import streamlit as st

from core import build_video, load_sorted_images, SUPPORTED_IMAGES

st.set_page_config(
    page_title="BeastTales Video Maker",
    page_icon="🦉",
    layout="centered",
)

# ── Başlık ────────────────────────────────────────────────────────────────────
st.title("🦉 BeastTales Video Maker")
st.caption("Görsellerini + sesi yükle → otomatik YouTube videosu oluştur")
st.divider()

# ── Yardım kutusu ─────────────────────────────────────────────────────────────
with st.expander("📖 Nasıl kullanılır?", expanded=False):
    st.markdown(
        """
**Adım 1 — Görseller:**
- Ideogram / Leonardo'dan indirdiğin görsel dosyalarını seç
- Dosya adları sırayla olmalı: `001.jpg`, `002.jpg`, ... veya `a.jpg`, `b.jpg`
- Önerilen: **110–130 görsel** (12-14 dk video için)

**Adım 2 — Ses:**
- Minimax'tan indirdiğin MP3 dosyasını seç

**Adım 3 — Ayarlar:**
- Geçiş süresi: görseller arası yumuşak geçiş (önerilen 0.4 sn)

**Adım 4 — Video Oluştur butonuna bas**
- Uygulama sesi eşit bölüp her görsele dağıtır
- 1920×1080 (Full HD) MP4 çıkar
- Bitince indir düğmesi çıkar

---
**İpucu:** Görsel sayısı = ses dakikası × 9 formülünü kullan.
Örn: 13 dk video → ~117 görsel
"""
    )

# ── Görsel yükleme ─────────────────────────────────────────────────────────────
st.subheader("1️⃣  Görselleri Seç")
uploaded_images = st.file_uploader(
    "Görsel dosyalarını sürükle veya seç (JPG / PNG / WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
)

if uploaded_images:
    st.success(f"✅ {len(uploaded_images)} görsel yüklendi")
    with st.expander("Yüklenen görseller"):
        cols = st.columns(5)
        for i, f in enumerate(uploaded_images[:20]):
            cols[i % 5].image(f, use_column_width=True, caption=f.name)
        if len(uploaded_images) > 20:
            st.caption(f"... ve {len(uploaded_images) - 20} görsel daha")

st.divider()

# ── Ses yükleme ────────────────────────────────────────────────────────────────
st.subheader("2️⃣  Seslendirmeyi Seç")
uploaded_audio = st.file_uploader(
    "Minimax'tan indirdiğin MP3 dosyasını seç",
    type=["mp3", "wav", "m4a"],
)
if uploaded_audio:
    st.audio(uploaded_audio)
    st.success(f"✅ Ses yüklendi: {uploaded_audio.name}")

st.divider()

# ── Ayarlar ────────────────────────────────────────────────────────────────────
st.subheader("3️⃣  Ayarlar")
col1, col2 = st.columns(2)
with col1:
    fade = st.slider(
        "Geçiş süresi (saniye)",
        min_value=0.0,
        max_value=1.5,
        value=0.4,
        step=0.1,
        help="Görseller arası yumuşak geçiş süresi",
    )
with col2:
    output_name = st.text_input(
        "Çıktı dosya adı",
        value="beasttales_video",
        help="Uzantı ekleme, otomatik .mp4 eklenir",
    )

st.divider()

# ── Video oluştur ──────────────────────────────────────────────────────────────
st.subheader("4️⃣  Video Oluştur")

ready = uploaded_images and uploaded_audio
if not ready:
    st.info("⬆️ Görsel ve ses dosyalarını yükledikten sonra buton aktif olur")

if st.button(
    "🎬 Video Oluştur",
    disabled=not ready,
    use_container_width=True,
    type="primary",
):
    with tempfile.TemporaryDirectory() as tmp:
        img_dir = os.path.join(tmp, "images")
        os.makedirs(img_dir)

        # Görselleri kaydet
        for uf in sorted(uploaded_images, key=lambda x: x.name):
            dest = os.path.join(img_dir, uf.name)
            with open(dest, "wb") as f:
                f.write(uf.read())

        # Sesi kaydet
        audio_ext = Path(uploaded_audio.name).suffix
        audio_path = os.path.join(tmp, f"audio{audio_ext}")
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.read())

        output_path = os.path.join(tmp, f"{output_name}.mp4")

        # İlerleme göstergesi
        progress_bar = st.progress(0, text="Başlatılıyor...")
        status = st.empty()

        def update_progress(current, total, label):
            pct = int((current / total) * 100) if total else 0
            progress_bar.progress(pct, text=f"{pct}% — {label}")
            status.caption(f"İşleniyor: {label}")

        start = time.time()
        try:
            build_video(
                images_folder=img_dir,
                audio_path=audio_path,
                output_path=output_path,
                fade_duration=fade,
                progress_callback=update_progress,
            )
            elapsed = round(time.time() - start, 1)
            progress_bar.progress(100, text="✅ Tamamlandı!")
            status.empty()

            n_images = len(uploaded_images)
            st.success(
                f"🎉 Video hazır! "
                f"{n_images} görsel işlendi — {elapsed} saniyede tamamlandı"
            )

            with open(output_path, "rb") as vf:
                video_bytes = vf.read()

            st.download_button(
                label="⬇️  MP4 İndir",
                data=video_bytes,
                file_name=f"{output_name}.mp4",
                mime="video/mp4",
                use_container_width=True,
            )

            st.video(video_bytes)

        except Exception as e:
            progress_bar.empty()
            status.empty()
            st.error(f"❌ Hata oluştu: {e}")
            st.info(
                "Olası nedenler: bozuk görsel dosyası, "
                "desteklenmeyen ses formatı. "
                "Görsellerin JPG/PNG olduğunu kontrol et."
            )

st.divider()
st.caption(
    "BeastTales Video Maker — "
    "Görsel: Ideogram / Leonardo  •  "
    "Ses: Minimax  •  "
    "Video: Bu uygulama  •  "
    "Montaj son dokunuşlar: CapCut"
)
