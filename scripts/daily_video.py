#!/usr/bin/env python3
"""Gunun konusundan bir travel guide videosu uretir.

Konu, topics/travel_topics.txt icinden tarihe gore secilir; ayni gun icinde
tekrar calistirmak ayni konuyu verir, ertesi gun sirada bir sonrakine gecer.
Boylece CI'da imlec dosyasi commit'lemeye gerek kalmiyor.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MPT_DIR = Path(os.environ.get("MPT_DIR", ROOT / ".mpt"))
TOPICS_FILE = ROOT / "topics" / "travel_topics.txt"
OUTPUT_DIR = ROOT / "output"

# Travel guide on ayarlari. Manzara icerigi genis ekranda izlenir, sahneler
# script sirasina eslenir ve Latin alfabesi icin Latin bir font secilir.
PRESET = [
    "--video-aspect", "16:9",
    "--video-concat-mode", "sequential",
    "--video-transition-mode", "fade-in",
    "--video-clip-duration", "5",
    "--match-materials-to-script",
    "--font-name", "BeVietnamPro-Bold.ttf",
    "--font-size", "48",
    "--subtitle-position", "bottom",
    "--stroke-width", "1.5",
    "--bgm-type", "random",
    "--bgm-volume", "0.15",
]

SCRIPT_PROMPT = (
    "Write it as a travel guide narration for a YouTube video. "
    "Name real neighbourhoods, viewpoints and dishes. Give the viewer one "
    "concrete tip per paragraph, such as the best time of day to arrive. "
    "Do not use hashtags, emoji or a call to subscribe."
)


def load_topics() -> list[str]:
    if not TOPICS_FILE.exists():
        sys.exit(f"Konu dosyasi yok: {TOPICS_FILE}")
    topics = [
        line.strip()
        for line in TOPICS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not topics:
        sys.exit(f"{TOPICS_FILE} bos")
    return topics


def topic_for_today(topics: list[str]) -> str:
    return topics[date.today().toordinal() % len(topics)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", help="konu listesini atlayip bu konuyu kullan")
    parser.add_argument("--script", help="hazir metin; LLM cagrisini atlar")
    parser.add_argument("--terms", help="virgulle ayrilmis Pexels arama kelimeleri")
    parser.add_argument("--voice", default="en-US-AndrewNeural-Male", help="Edge TTS sesi")
    parser.add_argument(
        "--paragraphs", type=int, default=5,
        help="LLM'in uretecegi paragraf sayisi; her paragraf yaklasik 20-30 saniye",
    )
    args = parser.parse_args()

    cli = MPT_DIR / "cli.py"
    python = MPT_DIR / ".venv" / "bin" / "python"
    if not cli.exists() or not python.exists():
        sys.exit("MoneyPrinterTurbo kurulu degil. Once ./scripts/setup.sh calistir.")

    topic = args.topic or topic_for_today(load_topics())
    print(f"==> Konu: {topic}")

    command = [
        str(python), str(cli),
        "--video-subject", topic,
        "--video-language", "en-US",
        "--voice-name", args.voice,
        "--paragraph-number", str(args.paragraphs),
        "--video-script-prompt", SCRIPT_PROMPT,
        *PRESET,
    ]
    if args.script:
        command += ["--video-script", args.script]
    if args.terms:
        command += ["--video-terms", args.terms]

    # cli.py, config.toml ile gorece yollari MPT klasorune gore cozuyor.
    env = {**os.environ, "PATH": f"{python.parent}{os.pathsep}{os.environ['PATH']}"}
    result = subprocess.run(command, cwd=MPT_DIR, env=env, capture_output=True, text=True)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        # cli.py hata ayrintilarini stdout'a yaziyor; sadece stderr'i gostermek
        # basarisiz calistirmalari sebepsiz birakirdi.
        sys.stderr.write(result.stdout)
        return result.returncode

    # cli.py son satirda JSON ozet basiyor; uretilen dosyayi oradan aliyoruz.
    last_line = result.stdout.strip().splitlines()[-1]
    videos = json.loads(last_line)["result"]["videos"]

    OUTPUT_DIR.mkdir(exist_ok=True)
    slug = "".join(c if c.isalnum() else "-" for c in topic.lower()).strip("-")[:60]
    for index, video in enumerate(videos, start=1):
        suffix = f"-{index}" if len(videos) > 1 else ""
        destination = OUTPUT_DIR / f"{date.today():%Y-%m-%d}-{slug}{suffix}.mp4"
        shutil.copy2(video, destination)
        print(f"==> Hazir: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
