#!/usr/bin/env python3
"""Kanal analizi: performans dağılımı, outlier videolar, başlık kalıpları, ritim.

Kullanım:
  python tools/channel_analyze.py https://www.youtube.com/@kanal --limit 80
  python tools/channel_analyze.py https://www.youtube.com/@kanal --json rapor.json

Çıktı bilinçli olarak kısadır: Claude'a yapıştırınca ~300-600 token tutar.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
from collections import Counter

from common import ytdlp_json, entries, table, human, die, run
from yt_fetch import norm_channel_url

STOP = set("""a an the and or of to in for on with your you my me is are was be how what why
when who this that it its at from as by we our i̇ ve ile bir bu ne nasil nasıl icin için the""".split())


def tokens(title: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9çğıöşüÇĞİÖŞÜ']{3,}", (title or "").lower())
    return [w for w in words if w not in STOP]


def analyze(vids: list[dict]) -> dict:
    views = [v.get("view_count") or 0 for v in vids]
    real = [v for v in views if v > 0]
    med = st.median(real) if real else 0

    scored = []
    for v in vids:
        vc = v.get("view_count") or 0
        scored.append({
            "title": v.get("title") or "",
            "views": vc,
            "ratio": round(vc / med, 2) if med else 0,
            "dur": v.get("duration") or 0,
            "url": v.get("url") or f"https://youtu.be/{v.get('id')}",
        })
    scored.sort(key=lambda x: x["views"], reverse=True)

    # başlık kelimeleri: outlier videolarda ne sık geçiyor?
    top = [s for s in scored if s["ratio"] >= 1.5] or scored[: max(3, len(scored) // 5)]
    bottom = scored[-max(3, len(scored) // 5):]
    top_words = Counter(w for s in top for w in set(tokens(s["title"])))
    bot_words = Counter(w for s in bottom for w in set(tokens(s["title"])))
    edge = [(w, c, bot_words.get(w, 0)) for w, c in top_words.most_common(40)
            if c >= 2 and c > bot_words.get(w, 0)]

    durs = [s["dur"] for s in scored if s["dur"]]
    return {
        "video_sayisi": len(vids),
        "medyan_izlenme": int(med),
        "ortalama_izlenme": int(st.mean(real)) if real else 0,
        "en_iyi": scored[:8],
        "en_kotu": scored[-5:],
        "outlier_sayisi": sum(1 for s in scored if s["ratio"] >= 2),
        "medyan_sure_dk": round(st.median(durs) / 60, 1) if durs else None,
        "kazandiran_kelimeler": edge[:12],
        "baslik_uzunlugu_medyan": int(st.median([len(s["title"]) for s in scored])) if scored else 0,
    }


def report(a: dict) -> str:
    out = [
        f"video: {a['video_sayisi']}  medyan izlenme: {human(a['medyan_izlenme'])}  "
        f"ortalama: {human(a['ortalama_izlenme'])}  outlier(2x+): {a['outlier_sayisi']}",
        f"medyan sure: {a['medyan_sure_dk']} dk  medyan baslik uzunlugu: {a['baslik_uzunlugu_medyan']} karakter",
        "",
        "EN IYI VIDEOLAR",
        table([[human(s["views"]), f"{s['ratio']}x", s["title"][:52]] for s in a["en_iyi"]],
              ["izlenme", "medyana", "baslik"]),
        "",
        "EN ZAYIF VIDEOLAR",
        table([[human(s["views"]), f"{s['ratio']}x", s["title"][:52]] for s in a["en_kotu"]],
              ["izlenme", "medyana", "baslik"]),
    ]
    if a["kazandiran_kelimeler"]:
        out += ["", "KAZANDIRAN BASLIK KELIMELERI (ustte/altta gecis sayisi)",
                table([[w, t, b] for w, t, b in a["kazandiran_kelimeler"]],
                      ["kelime", "ust", "alt"])]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url")
    ap.add_argument("--limit", type=int, default=80)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--json", help="raporu JSON olarak bu dosyaya yaz")
    args = ap.parse_args()

    url = norm_channel_url(args.url)
    data = ytdlp_json(url, flat=True, limit=args.limit, refresh=args.refresh)
    vids = entries(data)
    if not vids:
        die("video bulunamadi")
    a = analyze(vids)
    print(f"KANAL: {data.get('channel') or data.get('title')}")
    print(report(a))
    if args.json:
        with open(args.json, "w") as f:
            json.dump(a, f, ensure_ascii=False, indent=1)
        print(f"\njson: {args.json}")


if __name__ == "__main__":
    run(main)
