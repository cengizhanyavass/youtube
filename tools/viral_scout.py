#!/usr/bin/env python3
"""Çapraz dil viral avcısı: az aboneli kanalda patlamış videoları bulur.

Mantık: bir video 3.000 aboneli kanalda 800.000 izlenme almışsa, o başarı
kanalın gücünden değil **konudan/paketlemeden** gelir. Bu videolar
kopyalanabilir; büyük kanalın 800K'sı kopyalanamaz.

Kullanım:
  python tools/viral_scout.py "tiny house" --langs en,es,pt,de,ru
  python tools/viral_scout.py --queries-file scripts/queries.json --max-subs 50000

Çıktı: viral oran (izlenme/abone) ile sıralı kısa tablo.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import ytdlp_json, entries, table, human, run

# Aynı konuyu farklı dillerde aramak için yaygın kalıplar.
LANG_HINTS = {
    "en": "", "es": "espanol", "pt": "portugues", "de": "deutsch", "fr": "francais",
    "ru": "russkiy", "hi": "hindi", "id": "indonesia", "tr": "turkce",
    "it": "italiano", "ar": "arabic", "ja": "japanese", "pl": "polski",
}

_subs_cache: dict[str, int] = {}


def channel_subs(channel_id: str | None, channel_url: str | None, refresh: bool) -> int:
    """Kanalın abone sayısı. Kanal başına tek istek, sonuç cache'lenir."""
    key = channel_id or channel_url or ""
    if not key:
        return 0
    if key in _subs_cache:
        return _subs_cache[key]
    url = channel_url or f"https://www.youtube.com/channel/{channel_id}"
    try:
        data = ytdlp_json(url + "/videos", flat=True, limit=1,
                          cache_key=f"subs::{key}", refresh=refresh)
        subs = int(data.get("channel_follower_count") or 0)
    except (RuntimeError, ValueError, TypeError):
        subs = 0
    _subs_cache[key] = subs
    return subs


def scan(queries: list[str], per: int, refresh: bool) -> list[dict]:
    seen, found = set(), []
    for q in queries:
        try:
            data = ytdlp_json(f"ytsearch{per}:{q}", flat=True, refresh=refresh)
        except RuntimeError as e:
            print(f"  atlandi ({q}): {e}")
            continue
        for v in entries(data):
            vid = v.get("id")
            if not vid or vid in seen:
                continue
            seen.add(vid)
            found.append({
                "id": vid,
                "title": v.get("title") or "",
                "views": v.get("view_count") or 0,
                "channel": v.get("channel") or v.get("uploader") or "?",
                "channel_id": v.get("channel_id"),
                "channel_url": v.get("channel_url") or v.get("uploader_url"),
                "dur": v.get("duration") or 0,
                "query": q,
            })
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("seeds", nargs="*", help="konu tohum kelimeleri")
    ap.add_argument("--queries-file", help='JSON: {"en": ["..."], "es": ["..."]}')
    ap.add_argument("--langs", default="en,es,pt,de,ru,hi,id,fr",
                    help="tohum kelimeye eklenecek dil ipuclari")
    ap.add_argument("--per", type=int, default=20, help="arama basina video")
    ap.add_argument("--min-views", type=int, default=100_000)
    ap.add_argument("--max-subs", type=int, default=100_000)
    ap.add_argument("--lookups", type=int, default=40, help="abone sorgusu ust siniri")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--json", help="sonucu JSON olarak yaz")
    args = ap.parse_args()

    queries: list[str] = []
    if args.queries_file:
        doc = json.loads(Path(args.queries_file).read_text())
        for lang, qs in doc.items():
            queries += list(qs)
    for seed in args.seeds:
        for lang in [l.strip() for l in args.langs.split(",") if l.strip()]:
            hint = LANG_HINTS.get(lang, lang)
            queries.append(f"{seed} {hint}".strip())
    if not queries:
        ap.error("tohum kelime ya da --queries-file gerekli")

    print(f"{len(queries)} arama taraniyor...")
    cands = [c for c in scan(queries, args.per, args.refresh) if c["views"] >= args.min_views]
    cands.sort(key=lambda c: -c["views"])
    print(f"{len(cands)} video esigi gecti, abone sayilari sorgulaniyor "
          f"(en fazla {args.lookups} kanal)...")

    hits = []
    for c in cands[: args.lookups]:
        subs = channel_subs(c["channel_id"], c["channel_url"], args.refresh)
        if not subs or subs > args.max_subs:
            continue
        c["subs"] = subs
        c["ratio"] = round(c["views"] / max(subs, 500), 1)
        hits.append(c)

    if not hits:
        print("kriterlere uyan video bulunamadi. --max-subs yukselt ya da "
              "--min-views dusur.")
        return

    hits.sort(key=lambda c: -c["ratio"])
    rows = [[f"{h['ratio']}x", human(h["views"]), human(h["subs"]),
             f"{h['dur'] // 60}dk", h["channel"][:18], h["title"][:44]]
            for h in hits[: args.top]]
    print(table(rows, ["oran", "izlenme", "abone", "sure", "kanal", "baslik"]))
    print("\nOkuma: oran 20x+ = konu kanali tasimis, format kopyalanabilir. "
          "Abonesi dusuk + izlenmesi yuksek olanlari kendi diline/nisine uyarla.")

    if args.json:
        Path(args.json).write_text(json.dumps(hits[: args.top], ensure_ascii=False, indent=1))
        print(f"json: {args.json}")


if __name__ == "__main__":
    run(main)
