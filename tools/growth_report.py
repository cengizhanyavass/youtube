#!/usr/bin/env python3
"""Tek komut, tek rapor: kanal analizi + rakipler + nis + capraz dil viral tarama.

Kullanım:
  python tools/growth_report.py https://www.youtube.com/@KANALIN
  python tools/growth_report.py https://www.youtube.com/@KANALIN --seeds "tiny house,off grid"

Sonuç out/rapor.txt dosyasına yazılır. Bu dosya bilinçli olarak kısadır
(~1-2 KB); tamamını Claude'a yapıştırabilirsin.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from pathlib import Path

from channel_analyze import analyze, report, tokens
from common import ytdlp_json, entries, run
from yt_fetch import norm_channel_url

HERE = Path(__file__).resolve().parent


def section(title: str, body: str) -> str:
    return f"\n{'=' * 60}\n{title}\n{'=' * 60}\n{body.strip()}\n"


def run_tool(name: str, *cli_args: str) -> str:
    cmd = [sys.executable, str(HERE / name), *cli_args]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return (p.stdout or "").strip() or (p.stderr or "").strip()[:400]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url")
    ap.add_argument("--limit", type=int, default=80, help="analiz edilecek video sayisi")
    ap.add_argument("--seeds", help="virgulle ayrilmis konu tohumlari (bos ise otomatik)")
    ap.add_argument("--langs", default="en,es,pt,de,ru,hi,id,fr")
    ap.add_argument("--max-subs", type=int, default=100_000)
    ap.add_argument("--out", default="out/rapor.txt")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    url = norm_channel_url(args.url)
    extra = ["--refresh"] if args.refresh else []

    print("1/4 kanal analizi...")
    data = ytdlp_json(url, flat=True, limit=args.limit, refresh=args.refresh)
    vids = entries(data)
    if not vids:
        raise RuntimeError("kanaldan video alinamadi")
    name = data.get("channel") or data.get("title") or args.url
    subs = data.get("channel_follower_count")
    a = analyze(vids)
    head = f"KANAL: {name}   abone: {subs if subs is not None else '?'}"
    out = section("KANAL ANALIZI", head + "\n" + report(a))

    # konu tohumları: en iyi videoların başlıklarındaki sık kelimeler
    if args.seeds:
        seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    else:
        c = Counter(w for s in a["en_iyi"] for w in set(tokens(s["title"])))
        seeds = [w for w, _ in c.most_common(3)]
    out += section("SECILEN KONU TOHUMLARI", ", ".join(seeds) or "(bulunamadi)")

    print("2/4 rakip taramasi...")
    out += section("RAKIPLER", run_tool("competitors.py", "--from-channel", args.url,
                                        "--per", "20", "--top", "12", *extra))

    print("3/4 nis taramasi...")
    out += section("NIS SKORLARI", run_tool("niche_finder.py", *seeds,
                                            "--per", "12", "--top", "15", *extra))

    print("4/4 capraz dil viral tarama...")
    out += section("BASKA DILLERDE PATLAMIS / AZ ABONELI",
                   run_tool("viral_scout.py", *seeds, "--langs", args.langs,
                            "--per", "18", "--max-subs", str(args.max_subs),
                            "--top", "20", *extra))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(out)
    print(f"\nhazir: {args.out} ({len(out)} karakter). Tamamini Claude'a yapistir.")


if __name__ == "__main__":
    run(main)
