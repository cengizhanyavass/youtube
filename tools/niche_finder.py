#!/usr/bin/env python3
"""Niş bulucu: verilen tohum kelimelerden alt nişleri tarar ve skorlar.

Kullanım:
  python tools/niche_finder.py "stickman" --modifiers-file scripts/modifiers.txt
  python tools/niche_finder.py "stickman" "stick figure" --per 15

Skor = talep (medyan izlenme) / rekabet (büyük kanal yoğunluğu).
Yüksek skor: az rakip, çok izlenme -> girilebilir niş.
"""
from __future__ import annotations

import argparse
import statistics as st
from pathlib import Path

from common import ytdlp_json, entries, table, human, run

DEFAULT_MODIFIERS = [
    "animation", "story", "fight", "explained", "for kids", "funny",
    "shorts", "tutorial", "compilation", "vs", "history", "meme",
]


def score_query(q: str, per: int, refresh: bool) -> dict | None:
    try:
        data = ytdlp_json(f"ytsearch{per}:{q}", flat=True, refresh=refresh)
    except RuntimeError:
        return None
    vids = entries(data)
    views = [v.get("view_count") or 0 for v in vids if v.get("view_count")]
    if len(views) < 3:
        return None
    med = st.median(views)
    big = sum(1 for v in views if v > 1_000_000)          # doygun rekabet göstergesi
    small_hits = sum(1 for v in views if 50_000 <= v <= 500_000)  # ulaşılabilir tavan
    competition = 1 + big / max(1, len(views)) * 10
    return {
        "query": q,
        "medyan": int(med),
        "buyuk": big,
        "ulasilabilir": small_hits,
        "skor": round(med / 1000 / competition, 1),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("seeds", nargs="+")
    ap.add_argument("--modifiers-file", help="her satırda bir modifier")
    ap.add_argument("--per", type=int, default=15)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    mods = DEFAULT_MODIFIERS
    if args.modifiers_file:
        mods = [l.strip() for l in Path(args.modifiers_file).read_text().splitlines() if l.strip()]

    results = []
    for seed in args.seeds:
        for m in [""] + mods:
            q = f"{seed} {m}".strip()
            r = score_query(q, args.per, args.refresh)
            if r:
                results.append(r)
    if not results:
        print("veri alinamadi (ag erisimi veya arama sonucu yok)")
        return

    results.sort(key=lambda r: -r["skor"])
    rows = [[r["skor"], human(r["medyan"]), r["buyuk"], r["ulasilabilir"], r["query"][:40]]
            for r in results[: args.top]]
    print(table(rows, ["skor", "medyan", "1M+", "50-500K", "arama"]))
    print("\nOkuma: skor yuksek + '1M+' dusuk + '50-500K' yuksek = kucuk kanalin girebilecegi nis.")


if __name__ == "__main__":
    run(main)
