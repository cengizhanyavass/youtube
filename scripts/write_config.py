#!/usr/bin/env python3
"""config.example.toml'dan travel guide ayarlarina sahip bir config.toml uretir.

Anahtarlar ortam degiskenlerinden okunur, boylece hicbir sir repoya girmez.
Yorum satirlarini korumak icin dosya satir bazinda duzenlenir; TOML'i parse edip
yeniden yazmak ornek dosyadaki aciklamalarin tamamini silerdi.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

# Script uretimi icin desteklenen saglayicilar: ortam degiskeni -> config anahtari.
LLM_PROVIDERS = {
    "OPENAI_API_KEY": ("openai", "openai_api_key"),
    "ANTHROPIC_API_KEY": ("anthropic", "anthropic_api_key"),
    "GEMINI_API_KEY": ("gemini", "gemini_api_key"),
    "DEEPSEEK_API_KEY": ("deepseek", "deepseek_api_key"),
    "MOONSHOT_API_KEY": ("moonshot", "moonshot_api_key"),
}


def toml_string_list(values: list[str]) -> str:
    return "[" + ", ".join('"{}"'.format(v.replace('"', '\\"')) for v in values) + "]"


def set_key(lines: list[str], key: str, value: str) -> list[str]:
    """Yorum olmayan ilk `key = ...` atamasini degistirir."""
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*=")
    for i, line in enumerate(lines):
        if pattern.match(line):
            lines[i] = f"{key} = {value}\n"
            return lines
    raise KeyError(f"config.example.toml icinde '{key}' bulunamadi")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mpt-dir", required=True, type=Path)
    args = parser.parse_args()

    example = args.mpt_dir / "config.example.toml"
    target = args.mpt_dir / "config.toml"
    lines = example.read_text(encoding="utf-8").splitlines(keepends=True)

    pexels_keys = [k.strip() for k in os.environ.get("PEXELS_API_KEYS", "").split(",") if k.strip()]
    pixabay_keys = [k.strip() for k in os.environ.get("PIXABAY_API_KEYS", "").split(",") if k.strip()]
    if not pexels_keys and not pixabay_keys:
        raise SystemExit(
            "PEXELS_API_KEYS (veya PIXABAY_API_KEYS) tanimli degil. "
            "Ucretsiz anahtar: https://www.pexels.com/api/"
        )

    set_key(lines, "pexels_api_keys", toml_string_list(pexels_keys))
    set_key(lines, "pixabay_api_keys", toml_string_list(pixabay_keys))
    set_key(lines, "video_source", '"pexels"' if pexels_keys else '"pixabay"')
    # Edge altyazi hizalamasi TTS zamanlamalarini kullanir: Whisper'a gore hem
    # daha hizli hem de model indirmesi gerektirmiyor.
    set_key(lines, "subtitle_provider", '"edge"')

    for env_name, (provider, config_key) in LLM_PROVIDERS.items():
        api_key = os.environ.get(env_name, "").strip()
        if api_key:
            set_key(lines, "llm_provider", f'"{provider}"')
            set_key(lines, config_key, f'"{api_key}"')
            print(f"LLM saglayicisi: {provider}")
            break
    else:
        # LLM yoksa da sorun degil: daily_video.py --script ile calisabilir.
        print("LLM anahtari yok; script'i kendin vermelisin (--script).")

    target.write_text("".join(lines), encoding="utf-8")
    print(f"Yazildi: {target}")


if __name__ == "__main__":
    main()
