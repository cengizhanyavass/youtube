#!/usr/bin/env bash
# Tek komutluk kurulum: ffmpeg + python bagimliliklari.
# Kullanim:  bash setup.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "== ffmpeg kontrol =="
if ! command -v ffmpeg >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update -qq && sudo apt-get install -y ffmpeg
  elif command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  elif command -v winget >/dev/null 2>&1; then
    winget install --id Gyan.FFmpeg -e
  else
    echo "ffmpeg'i elle kur: https://ffmpeg.org/download.html" >&2
    exit 1
  fi
fi
ffmpeg -version | head -1

echo "== python ortami =="
python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

echo "== dogrulama =="
.venv/bin/python tools/stickman.py --action wave --seconds 1 --out out/_check.mp4 >/dev/null
echo "kurulum tamam. ornek: .venv/bin/python tools/build_video.py scripts/example.json --fast"
