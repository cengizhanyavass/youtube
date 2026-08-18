#!/usr/bin/env python3
"""Rakip araştırması: anahtar kelimelerden rakip kanalları bulur ve karşılaştırır.

Kullanım:
  python tools/competitors.py "stickman animation" "stick figure story" --per 25
  python tools/competitors.py --from-channel https://www.youtube.com/@kanal

Skor mantığı: bir kanalın aramalarda kaç kez çıktığı x medyan izlenmesi.
Küçük ama yüksek izlenmeli kanallar = kopyalanabilir format.
"""
from __future__ import annotations

import argparse
import statistics as st
from collections import defaultdict

from common import ytdlp_json, entries, table, human, run
from yt_fetch import norm_channel_url
from channel_analyze import tokens


def collect(queries: list[str], per: int, refresh: bool) -> dict[str, list[dict]]:
    by_channel: dict[str, list[dict]] = defaultdict(list)
    for q in queries:
        data = ytdlp_json(f"ytsearch{per}:{q}", flat=True, refresh=refresh)
        for v in entries(data):
            ch = v.get("channel") or v.get("uploader") or "?"
            by_channel[ch].append(v)
    return by_channel


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("queries", nargs="*", help="arama terimleri")
    ap.add_argument("--from-channel", help="kanalın başlıklarından otomatik terim üret")
    ap.add_argument("--per", type=int, default=20, help="arama başına video")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    queries = list(args.queries)
    if args.from_channel:
        data = ytdlp_json(norm_channel_url(args.from_channel), flat=True, limit=40,
                          refresh=args.refresh)
        words = defaultdict(int)
        for v in entries(data):
            for w in set(tokens(v.get("title") or "")):
                words[w] += 1
        queries += [w for w, _ in sorted(words.items(), key=lambda kv: -kv[1])[:5]]
    if not queries:
        ap.error("en az bir arama terimi ver ya da --from-channel kullan")

    print(f"terimler: {', '.join(queries)}")
    by_channel = collect(queries, args.per, args.refresh)

    if not by_channel:
        print("sonuc yok (ag erisimi engelli olabilir ya da terimler cok dar)")
        return

    rows = []
    for ch, vids in by_channel.items():
        views = [v.get("view_count") or 0 for v in vids]
        med = int(st.median(views)) if views else 0
        best = max(vids, key=lambda v: v.get("view_count") or 0)
        rows.append([len(vids), human(med), human(best.get("view_count")), ch[:24],
                     (best.get("title") or "")[:44]])
    rows.sort(key=lambda r: (-r[0], r[1]))

    print(table(rows[: args.top],
                ["cikis", "medyan", "en_iyi", "kanal", "en_iyi_video"]))
    print("\nOkuma: 'cikis' cok + 'medyan' yuksek = nisin sahibi. "
          "'cikis' az + 'en_iyi' cok yuksek = tek videoyla patlamis format, kopyalanabilir.")


if __name__ == "__main__":
    run(main)
