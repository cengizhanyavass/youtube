#!/bin/bash

echo ""
echo "========================================"
echo "  BeastTales Video Maker - Kurulum"
echo "========================================"
echo ""

# Python kontrolü
if ! command -v python3 &>/dev/null; then
    echo "[HATA] Python3 bulunamadı!"
    echo "Lütfen önce Python kurun: https://www.python.org/downloads/"
    exit 1
fi

echo "[OK] Python bulundu: $(python3 --version)"
echo ""

cd "$(dirname "$0")"

echo "Kütüphaneler kuruluyor..."
python3 -m pip install --upgrade pip --quiet
pip3 install -r requirements.txt --quiet

echo ""
echo "[OK] Kurulum tamamlandı!"
echo ""
echo "Uygulama başlatılıyor..."
echo "Tarayıcınızda açılacak: http://localhost:8501"
echo ""

streamlit run app.py --server.maxUploadSize 2000
