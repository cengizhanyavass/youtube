#!/usr/bin/env bash
# Gerekli python paketlerini kurar. ffmpeg sistemde yoksa imageio-ffmpeg
# kendi static binary'sini indirir, ayrica ffmpeg kurmana gerek yok.
set -e
python3 -m pip install -r "$(dirname "$0")/requirements.txt"
echo "hazir. simdi: python3 kenburns_edit.py --plan"
