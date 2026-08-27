#!/usr/bin/env bash
# MoneyPrinterTurbo'yu kurar ve travel guide ayarlariyla yapilandirir.
# Kullanim: ./scripts/setup.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MPT_DIR="${MPT_DIR:-$ROOT/.mpt}"
MPT_REPO="https://github.com/harry0703/MoneyPrinterTurbo.git"

if [ -d "$MPT_DIR/.git" ]; then
  echo "==> MoneyPrinterTurbo guncelleniyor"
  git -C "$MPT_DIR" pull --ff-only
else
  echo "==> MoneyPrinterTurbo klonlaniyor"
  git clone --depth 1 "$MPT_REPO" "$MPT_DIR"
fi

echo "==> Python ortami hazirlaniyor"
python3 -m venv "$MPT_DIR/.venv"
"$MPT_DIR/.venv/bin/pip" install --quiet --upgrade pip
"$MPT_DIR/.venv/bin/pip" install --quiet -r "$MPT_DIR/requirements.txt" imageio-ffmpeg

# MoviePy ve MPT, PATH uzerinde bir ffmpeg bekliyor. imageio-ffmpeg ile gelen
# statik binary'yi venv/bin'e baglayarak sistem kurulumuna ihtiyaci kaldiriyoruz.
if ! command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG_BIN="$("$MPT_DIR/.venv/bin/python" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
  ln -sf "$FFMPEG_BIN" "$MPT_DIR/.venv/bin/ffmpeg"
  echo "==> ffmpeg baglandi: $FFMPEG_BIN"
fi

echo "==> config.toml yaziliyor"
"$MPT_DIR/.venv/bin/python" "$ROOT/scripts/write_config.py" --mpt-dir "$MPT_DIR"

echo
echo "Kurulum tamam. Video uretmek icin:"
echo "  ./scripts/daily_video.py"
