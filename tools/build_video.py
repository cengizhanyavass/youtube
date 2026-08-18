#!/usr/bin/env python3
"""JSON senaryo -> bitmiş stickman videosu (görüntü + seslendirme + altyazı).

Kullanım:
  python tools/build_video.py scripts/example.json --out out/video.mp4
  python tools/build_video.py scripts/example.json --no-tts --fast

Senaryo şeması: scripts/example.json dosyasına bak.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from stickman import ACTIONS, Actor, Style, VideoWriter, render_frame
from tts import audio_duration, estimate_duration, silence, speak

WORK = Path("out/_work")


def chunk_text(text: str, n: int = 7) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + n]) for i in range(0, len(words), n)] or [""]


def build_audio(segments: list[tuple[str, float]], out: str) -> str:
    """Her parçayı tam sahne süresine getirir ve birleştirir."""
    WORK.mkdir(parents=True, exist_ok=True)
    fixed = []
    for i, (path, dur) in enumerate(segments):
        dst = str(WORK / f"seg{i:03d}.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path,
                        "-af", "apad", "-t", f"{dur:.3f}", "-ar", "44100",
                        "-ac", "2", dst], check=True)
        fixed.append(dst)
    listfile = WORK / "concat.txt"
    listfile.write_text("\n".join(f"file '{Path(p).resolve()}'" for p in fixed))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listfile), "-c", "copy", out], check=True)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("script")
    ap.add_argument("--out", default="out/video.mp4")
    ap.add_argument("--no-tts", action="store_true", help="seslendirme yapma")
    ap.add_argument("--fast", action="store_true", help="640x360 @ 15fps taslak")
    args = ap.parse_args()

    doc = json.loads(Path(args.script).read_text())
    W = 640 if args.fast else doc.get("width", 1920)
    H = 360 if args.fast else doc.get("height", 1080)
    fps = 15 if args.fast else doc.get("fps", 30)
    voice = doc.get("voice", "tr-TR-AhmetNeural")
    style = Style(**doc.get("style", {}))
    scenes = doc["scenes"]
    WORK.mkdir(parents=True, exist_ok=True)

    # 1) sahne süreleri + ses parçaları
    plan = []
    for i, sc in enumerate(scenes):
        say = sc.get("say", "")
        seg, dur = None, float(sc.get("duration", 0) or 0)
        if say and not args.no_tts:
            path, real = speak(say, str(WORK / f"say{i:03d}.mp3"), voice, doc.get("rate", "+0%"))
            adur = audio_duration(path) or estimate_duration(say)
            dur = max(dur, adur + float(sc.get("pad", 0.5)))
            seg = path
        elif say:
            dur = max(dur, estimate_duration(say) + 0.4)
        dur = dur or 3.0
        if seg is None:
            seg = silence(str(WORK / f"sil{i:03d}.wav"), dur)
        plan.append((sc, dur, seg))
        print(f"sahne {i + 1}/{len(scenes)}: {dur:.1f}s  {sc.get('title') or say[:40]}")

    # 2) görüntü
    vw = VideoWriter(str(WORK / "video.mp4"), W, H, fps)
    for sc, dur, _ in plan:
        actors = [Actor(**a) for a in sc.get("actors", [{"action": "talk"}])]
        for a in actors:
            if a.action not in ACTIONS:
                raise SystemExit(f"bilinmeyen aksiyon: {a.action}. secenekler: {sorted(ACTIONS)}")
        subs = chunk_text(sc["say"]) if (sc.get("say") and sc.get("subtitle", True)) else None
        n = max(1, int(dur * fps))
        for f in range(n):
            t = f / n
            phases = [(t * dur * a.cycles) % 1.0 for a in actors]
            sub = subs[min(int(t * len(subs)), len(subs) - 1)] if subs else None
            vw.add(render_frame(W, H, actors, phases, style,
                                title=sc.get("title"), subtitle=sub))
    video = vw.close()

    # 3) ses + birleştirme
    audio = build_audio([(seg, dur) for _, dur, seg in plan], str(WORK / "audio.wav"))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", audio,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                    args.out], check=True)
    total = sum(d for _, d, _ in plan)
    print(f"\nhazir: {args.out}  ({total:.1f}s, {W}x{H}@{fps})")


if __name__ == "__main__":
    main()
