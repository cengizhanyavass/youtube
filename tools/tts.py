#!/usr/bin/env python3
"""Ücretsiz seslendirme: edge-tts (Microsoft Edge sesleri, API anahtarı yok).

Kullanım:
  python tools/tts.py "Merhaba dunya" --voice tr-TR-AhmetNeural --out out/a.mp3
  python tools/tts.py --list | head

Ağ yoksa sessiz (silent) bir parça üretir; video yine de tamamlanır.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
from pathlib import Path

DEFAULT_VOICE_TR = "tr-TR-AhmetNeural"
DEFAULT_VOICE_EN = "en-US-AndrewNeural"


def audio_duration(path: str) -> float:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", path], capture_output=True, text=True, check=True).stdout
        return float(json.loads(out)["format"]["duration"])
    except (subprocess.CalledProcessError, KeyError, ValueError, FileNotFoundError):
        return 0.0


def estimate_duration(text: str, wpm: int = 150) -> float:
    words = max(1, len(text.split()))
    return max(1.2, words / wpm * 60)


def silence(path: str, seconds: float) -> str:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{seconds:.3f}", path],
                   check=True)
    return path


def _trust_env_ca():
    """Kurumsal/proxy CA sertifikasını edge-tts'in SSL bağlamına ekler.

    edge-tts sadece certifi paketini kullanır; proxy arkasında bu yetmez.
    Doğrulama kapatılmaz, sadece ortamın verdiği CA eklenir.
    """
    import os
    import ssl

    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "NODE_EXTRA_CA_CERTS", "CURL_CA_BUNDLE"):
        path = os.environ.get(var)
        if path and Path(path).exists():
            try:
                from edge_tts import communicate

                communicate._SSL_CTX.load_verify_locations(cafile=path)
            except (ImportError, ssl.SSLError, OSError, AttributeError):
                pass
            return


def speak(text: str, out: str, voice: str = DEFAULT_VOICE_TR, rate: str = "+0%") -> tuple[str, bool]:
    """(dosya_yolu, gercek_ses_mi) döner. Ağ hatasında sessizliğe düşer."""
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    try:
        import edge_tts

        _trust_env_ca()

        async def run():
            c = edge_tts.Communicate(text, voice, rate=rate)
            await c.save(out)

        asyncio.run(run())
        if Path(out).exists() and Path(out).stat().st_size > 800:
            return out, True
    except Exception as e:  # ağ/servis hatası: sessizlik ile devam
        print(f"  [tts] ses uretilemedi ({type(e).__name__}), sessiz parca kullaniliyor")
    wav = str(Path(out).with_suffix(".wav"))
    return silence(wav, estimate_duration(text)), False


def list_voices(prefix: str = "") -> list[str]:
    import edge_tts

    async def run():
        return await edge_tts.list_voices()

    voices = asyncio.run(run())
    return sorted(v["ShortName"] for v in voices if v["ShortName"].startswith(prefix))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("text", nargs="?")
    ap.add_argument("--voice", default=DEFAULT_VOICE_TR)
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--out", default="out/tts.mp3")
    ap.add_argument("--list", metavar="PREFIX", nargs="?", const="", help="sesleri listele")
    args = ap.parse_args()

    if args.list is not None:
        print("\n".join(list_voices(args.list)))
        return
    if not args.text:
        ap.error("metin gerekli")
    path, real = speak(args.text, args.out, args.voice, args.rate)
    print(f"{path}  ({audio_duration(path):.2f}s, gercek_ses={real})")


if __name__ == "__main__":
    main()
