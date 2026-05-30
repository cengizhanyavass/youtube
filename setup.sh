#!/bin/bash
# MoneyPrinterTurbo kurulum scripti

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MPT_DIR="$SCRIPT_DIR/MoneyPrinterTurbo"

echo "========================================"
echo "  YouTube Video Üretici Kurulum"
echo "========================================"

# Python kontrolü
if ! command -v python3 &>/dev/null; then
    echo "[!] Python3 bulunamadı. Lütfen Python 3.10+ kurun."
    exit 1
fi

echo "[1/4] Python bağımlılıkları kuruluyor..."
cd "$MPT_DIR"

if command -v uv &>/dev/null; then
    uv sync
else
    pip install -r requirements.txt -q
fi

echo "[2/4] ffmpeg kontrol ediliyor..."
if ! command -v ffmpeg &>/dev/null; then
    echo "[!] ffmpeg bulunamadı. Kuruluyor..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y ffmpeg -q
    elif command -v brew &>/dev/null; then
        brew install ffmpeg
    else
        echo "[!] ffmpeg'i manuel kurun: https://ffmpeg.org/download.html"
    fi
else
    echo "[✓] ffmpeg mevcut: $(ffmpeg -version 2>&1 | head -1)"
fi

echo "[3/4] ImageMagick kontrol ediliyor..."
if ! command -v magick &>/dev/null && ! command -v convert &>/dev/null; then
    echo "[!] ImageMagick bulunamadı. Kuruluyor..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y imagemagick -q
    elif command -v brew &>/dev/null; then
        brew install imagemagick
    else
        echo "[!] ImageMagick'i manuel kurun: https://imagemagick.org"
    fi
else
    echo "[✓] ImageMagick mevcut"
fi

echo "[4/4] Konfigürasyon kontrol ediliyor..."
if [ ! -f "$MPT_DIR/config.toml" ]; then
    cp "$MPT_DIR/config.example.toml" "$MPT_DIR/config.toml"
    echo "[!] config.toml oluşturuldu. Lütfen API anahtarlarını girin:"
    echo "    $MPT_DIR/config.toml"
fi

# storage klasörlerini oluştur
mkdir -p "$MPT_DIR/storage/cache_videos"
mkdir -p "$MPT_DIR/storage/tasks"

echo ""
echo "========================================"
echo "  Kurulum Tamamlandı!"
echo "========================================"
echo ""
echo "  Sonraki adımlar:"
echo ""
echo "  1) API anahtarlarını ayarla:"
echo "     nano $MPT_DIR/config.toml"
echo "     (pexels_api_keys, openai_api_key vb.)"
echo ""
echo "  2) Sunucuyu başlat:"
echo "     cd $MPT_DIR && python main.py"
echo ""
echo "  3) Video üret:"
echo "     python $SCRIPT_DIR/generate_video.py --konu 'Konun' --stil shorts"
echo ""
echo "  Yardım için:"
echo "     python $SCRIPT_DIR/generate_video.py --help"
echo "     python $SCRIPT_DIR/generate_video.py --stiller"
echo ""
