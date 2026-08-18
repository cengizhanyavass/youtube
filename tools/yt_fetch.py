#!/usr/bin/env python3
"""Kanal / video metadata çekici (yt-dlp tabanlı, API anahtarsız).

Kullanım:
  python tools/yt_fetch.py video https://youtu.be/SM2mo8XR-vQ
  python tools/yt_fetch.py channel https://www.youtube.com/@kanal --limit 60
  python tools/yt_fetch.py search "stickman animation" --limit 25

Ham veri data/cache/ içine yazılır; ekrana sadece özet basılır.
"""
from __future__ import annotations

import argparse
import json

from common import cache_path, ytdlp_json, entries, table, human, die, run


def norm_channel_url(url: str) -> str:
    url = url.rstrip("/")
    if url.endswith(("/videos", "/shorts", "/streams")):
        return url
    return url + "/videos"


def cmd_video(args):
    d = ytdlp_json(args.url, refresh=args.refresh)
    fields = ["title", "channel", "channel_id", "channel_url", "duration",
              "view_count", "like_count", "comment_count", "upload_date"]
    for f in fields:
        print(f"{f}: {d.get(f)}")
    tags = d.get("tags") or []
    print(f"tags({len(tags)}): {', '.join(tags[:15])}")
    print(f"cache: {cache_path(args.url + '|flat=False|limit=None')}")


def cmd_channel(args):
    url = norm_channel_url(args.url)
    data = ytdlp_json(url, flat=True, limit=args.limit, refresh=args.refresh)
    vids = entries(data)
    if not vids:
        die("kanaldan video alinamadi")
    rows = []
    for v in vids[: args.show]:
        rows.append([
            human(v.get("view_count")),
            f"{(v.get('duration') or 0) // 60}dk",
            (v.get("title") or "")[:60],
        ])
    print(f"kanal: {data.get('channel') or data.get('title')}  video: {len(vids)}")
    print(table(rows, ["izlenme", "sure", "baslik"]))
    print(f"cache: {cache_path(url + f'|flat=True|limit={args.limit}')}")


def cmd_search(args):
    url = f"ytsearch{args.limit}:{args.query}"
    data = ytdlp_json(url, flat=True, refresh=args.refresh)
    vids = entries(data)
    rows = [[human(v.get("view_count")), (v.get("channel") or "")[:22],
             (v.get("title") or "")[:52]] for v in vids]
    print(table(rows, ["izlenme", "kanal", "baslik"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true", help="cache'i yok say")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("video"); p.add_argument("url"); p.set_defaults(fn=cmd_video)
    p = sub.add_parser("channel"); p.add_argument("url")
    p.add_argument("--limit", type=int, default=60)
    p.add_argument("--show", type=int, default=20)
    p.set_defaults(fn=cmd_channel)
    p = sub.add_parser("search"); p.add_argument("query")
    p.add_argument("--limit", type=int, default=20); p.set_defaults(fn=cmd_search)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    run(main)
