"""Ortak yardımcılar: cache, kompakt çıktı, yt-dlp sarmalayıcı.

Tasarım ilkesi: ham JSON diske yazılır, ekrana sadece kompakt özet basılır.
Böylece bir LLM'e (Claude) yapıştırılan çıktı küçük kalır -> az token.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)


def venv_bin(name: str) -> str:
    """venv içindeki çalıştırılabilir dosyayı bul, yoksa PATH'e düş."""
    cand = ROOT / ".venv" / "bin" / name
    return str(cand) if cand.exists() else name


def slug(text: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", text).strip("-").lower()
    return s[:maxlen] or "x"


def cache_path(key: str) -> Path:
    return CACHE / f"{slug(key, 90)}.json"


def load_cache(key: str):
    p = cache_path(key)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except json.JSONDecodeError:
            return None
    return None


def save_cache(key: str, data) -> Path:
    p = cache_path(key)
    p.write_text(json.dumps(data, ensure_ascii=False))
    return p


def ytdlp_json(url: str, flat: bool = False, limit: int | None = None,
               cache_key: str | None = None, refresh: bool = False):
    """yt-dlp ile metadata çeker. API anahtarı gerekmez, tamamen ücretsiz."""
    key = cache_key or f"{url}|flat={flat}|limit={limit}"
    if not refresh:
        cached = load_cache(key)
        if cached is not None:
            return cached

    cmd = [venv_bin("yt-dlp"), "--skip-download", "--ignore-errors", "--no-warnings", "-J"]
    if flat:
        cmd.append("--flat-playlist")
    if limit:
        cmd += ["--playlist-end", str(limit)]
    cmd.append(url)

    proc = subprocess.run(cmd, capture_output=True, text=True)
    raw = proc.stdout.strip()
    if not raw or raw == "null":
        err = (proc.stderr or "").strip().splitlines()
        tail = err[-1] if err else "bilinmeyen hata"
        raise RuntimeError(f"yt-dlp veri alamadi: {tail}")
    data = json.loads(raw)
    save_cache(key, data)
    return data


def entries(data) -> list[dict]:
    """Playlist/kanal cevabından video listesini düzleştirir."""
    out: list[dict] = []
    stack = [data]
    while stack:
        node = stack.pop()
        if not isinstance(node, dict):
            continue
        if node.get("_type") in (None, "video") and node.get("id") and "entries" not in node:
            out.append(node)
            continue
        for e in node.get("entries") or []:
            stack.append(e)
    return out


def table(rows: list[list], headers: list[str], maxw: int = 52) -> str:
    """Sabit genişlikli, dar bir tablo üretir (token dostu)."""
    data = [[str(c)[:maxw] for c in r] for r in rows]
    widths = [len(h) for h in headers]
    for r in data:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(c))
    line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * w for w in widths)
    body = "\n".join(" | ".join(c.ljust(widths[i]) for i, c in enumerate(r)) for r in data)
    return f"{line}\n{sep}\n{body}"


def human(n) -> str:
    try:
        n = float(n)
    except (TypeError, ValueError):
        return "-"
    for unit, div in (("M", 1e6), ("K", 1e3)):
        if abs(n) >= div:
            return f"{n / div:.1f}{unit}"
    return str(int(n))


def die(msg: str, code: int = 1):
    print(f"HATA: {msg}", file=sys.stderr)
    raise SystemExit(code)


def run(main_fn):
    """Ağ/veri hatalarını traceback yerine tek satır mesaja çevirir."""
    try:
        main_fn()
    except RuntimeError as e:
        die(str(e))
    except KeyboardInterrupt:
        die("iptal edildi", 130)


def env_flag(name: str, default: bool = False) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")
