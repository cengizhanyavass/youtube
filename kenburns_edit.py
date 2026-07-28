#!/usr/bin/env python3
"""
Seslendirme (1.wav ... 11.wav) + gorseller -> tek video.

Her ses dosyasi bir bolum. Bolumun suresi kadar gorsel ekranda kalir,
gorsele odak noktasina dogru yavas bir zoom (Ken Burns) uygulanir ve
bolumler arasi yumusak gecis (crossfade) yapilir.

Kullanim:
    python3 kenburns_edit.py                 # assets/audio + assets/images -> out/final.mp4
    python3 kenburns_edit.py --plan          # sadece plani goster, render etme
    python3 kenburns_edit.py --preview       # hizli dusuk cozunurluklu on izleme
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import wave
from dataclasses import dataclass, field
from pathlib import Path

AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


# --------------------------------------------------------------------------- #
# yardimcilar
# --------------------------------------------------------------------------- #
def ffmpeg_bin() -> str:
    """Sistemde ffmpeg yoksa imageio-ffmpeg'in getirdigi static binary'yi kullan."""
    env = os.environ.get("FFMPEG_BIN")
    if env:
        return env
    from shutil import which

    found = which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg bulunamadi. `pip install imageio-ffmpeg` calistir.")


def natural_key(p: Path):
    """1.wav, 2.wav, ..., 10.wav, 11.wav dogru siralansin diye."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def media_duration(path: Path) -> float:
    if path.suffix.lower() == ".wav":
        try:
            with wave.open(str(path), "rb") as w:
                return w.getnframes() / float(w.getframerate())
        except wave.Error:
            pass
    out = subprocess.run(
        [ffmpeg_bin(), "-hide_banner", "-i", str(path)],
        capture_output=True,
        text=True,
    ).stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", out)
    if not m:
        sys.exit(f"Sure okunamadi: {path}")
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


# --------------------------------------------------------------------------- #
# odak noktasi tespiti
# --------------------------------------------------------------------------- #
def _box_blur(a, r: int):
    import numpy as np

    if r < 1:
        return a
    k = 2 * r + 1
    pad = np.pad(a, r, mode="edge")
    c = np.cumsum(np.cumsum(pad, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    h, w = a.shape
    return (c[k:k + h, k:k + w] - c[0:h, k:k + w] - c[k:k + h, 0:w] + c[0:h, 0:w]) / (k * k)


def detect_focus(path: Path) -> tuple[float, float]:
    """Goruntunun en 'dolu' (detayli/kontrastli) bolgesini normalize koordinat olarak dondurur.

    Yuz/nesne tespiti yok; detay yogunlugu pratikte ilgi cekici bolgeyle ortusur
    (yuzler, yazi, ana obje). Sonuc [0.22, 0.78] araligina kisilir ki kadraj
    kenara yapisip hareket tuhaflasmasin.
    """
    import numpy as np
    from PIL import Image

    with Image.open(path) as im:
        im = im.convert("L")
        im.thumbnail((256, 256), Image.LANCZOS)
        g = np.asarray(im, dtype=np.float32) / 255.0

    gx = np.zeros_like(g)
    gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
    gy[1:-1, :] = g[2:, :] - g[:-2, :]
    energy = np.hypot(gx, gy)

    h, w = energy.shape
    energy = _box_blur(energy, max(3, min(h, w) // 12))

    # hafif merkez agirligi: esit detayda merkeze yakin olan kazansin
    yy, xx = np.mgrid[0:h, 0:w]
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    dist = np.hypot((yy - cy) / h, (xx - cx) / w)
    energy *= 1.0 - 0.35 * (dist / (dist.max() or 1.0))

    iy, ix = np.unravel_index(int(np.argmax(energy)), energy.shape)
    fx = (ix + 0.5) / w
    fy = (iy + 0.5) / h
    clamp = lambda v: max(0.22, min(0.78, v))
    return round(clamp(fx), 4), round(clamp(fy), 4)


def cover_crop_focus(path: Path, fx: float, fy: float, aspect: float) -> tuple[float, float]:
    """Goruntu cerceveyi doldurmak icin ortadan kirpildiginda odak koordinatlarini duzelt."""
    from PIL import Image

    with Image.open(path) as im:
        w, h = im.size
    src = w / h
    if abs(src - aspect) < 1e-6:
        return fx, fy
    if src > aspect:  # kenarlardan kirpilir
        keep = aspect / src
        off = (1 - keep) / 2
        fx = (fx - off) / keep
    else:  # ust/alttan kirpilir
        keep = src / aspect
        off = (1 - keep) / 2
        fy = (fy - off) / keep
    clamp = lambda v: max(0.0, min(1.0, v))
    return round(clamp(fx), 4), round(clamp(fy), 4)


# --------------------------------------------------------------------------- #
# plan
# --------------------------------------------------------------------------- #
@dataclass
class Shot:
    image: Path
    duration: float
    focus: tuple[float, float]
    move: str            # "in" | "out"
    zoom: float
    segment: int
    audio: str = ""


@dataclass
class Plan:
    shots: list[Shot] = field(default_factory=list)
    audios: list[Path] = field(default_factory=list)


def allocate(durs, n_img, min_shot) -> list[int]:
    """Her bolume kac gorsel dusecegini belirler.

    Once herkese bir tane, kalan gorseller "cekim basina en uzun sure duseni
    once doyur" mantigiyla dagitilir; boylece uzun bolumler daha fazla gorsel
    alir ve tempo her yerde benzer olur. min_shot altina inen bolunme yapilmaz.
    """
    n_seg = len(durs)
    cap = [max(1, int(d // min_shot)) for d in durs]
    count = [1] * n_seg
    for _ in range(max(0, min(n_img, sum(cap)) - n_seg)):
        best = max(
            (i for i in range(n_seg) if count[i] < cap[i]),
            key=lambda i: durs[i] / count[i],
            default=None,
        )
        if best is None:
            break
        count[best] += 1
    return count


def build_plan(audios, images, cfg, zoom, min_shot) -> Plan:
    plan = Plan(audios=list(audios))
    if not images:
        sys.exit("Gorsel bulunamadi.")

    durs = [media_duration(a) for a in audios]
    n_seg, n_img = len(audios), len(images)

    if n_img <= n_seg:
        counts = [1] * n_seg
    else:
        counts = allocate(durs, n_img, min_shot)
        used = sum(counts)
        if used < n_img:
            print(f"uyari: {n_img - used} gorsel kullanilmadi — her cekim en az "
                  f"{min_shot:g}sn tutuluyor. Hepsini kullanmak icin --min-shot degerini dusur.",
                  file=sys.stderr)

    # gorselleri sirayla bolumlere dagit (az gorsel varsa bastan doner)
    per_seg, k = [], 0
    for c in counts:
        per_seg.append([images[(k + j) % n_img] for j in range(c)])
        k += c

    idx = 0
    for seg, (audio, bucket, dur) in enumerate(zip(audios, per_seg, durs)):
        share = dur / len(bucket)
        for img in bucket:
            o = cfg.get(img.name, {})
            fx, fy = o["focus"] if "focus" in o else detect_focus(img)
            plan.shots.append(
                Shot(
                    image=img,
                    duration=round(share, 3),
                    focus=(float(fx), float(fy)),
                    move=o.get("move", "in" if idx % 2 == 0 else "out"),
                    zoom=float(o.get("zoom", zoom)),
                    segment=seg + 1,
                    audio=audio.name,
                )
            )
            idx += 1
    return plan


# --------------------------------------------------------------------------- #
# ffmpeg filtre grafigi
# --------------------------------------------------------------------------- #
def zoompan_expr(shot: Shot, frames: int, fx: float, fy: float):
    """Odak noktasina dogru yumusak (ease-in-out) zoom + kaydirma."""
    p = f"(on/{max(frames - 1, 1)})"
    e = f"({p}*{p}*(3-2*{p}))"          # smoothstep: baslangic/bitis yumusak
    z0, z1 = (1.0, shot.zoom) if shot.move == "in" else (shot.zoom, 1.0)
    zexpr = f"{z0}+({z1 - z0})*{e}"

    # kadraj merkezi: "in" -> ortadan odaga, "out" -> odaktan ortaya
    if shot.move == "in":
        cx = f"(0.5+({fx - 0.5})*{e})"
        cy = f"(0.5+({fy - 0.5})*{e})"
    else:
        cx = f"({fx}+({0.5 - fx})*{e})"
        cy = f"({fy}+({0.5 - fy})*{e})"

    xexpr = f"max(0,min(iw-iw/zoom,{cx}*iw-iw/zoom/2))"
    yexpr = f"max(0,min(ih-ih/zoom,{cy}*ih-ih/zoom/2))"
    return zexpr, xexpr, yexpr


def build_command(plan: Plan, out: Path, width, height, fps, xdur, transition,
                  crf, preset, audio_bitrate) -> list[str]:
    n = len(plan.shots)
    aspect = width / height
    # zoompan'in adim adim kayma titremesini azaltmak icin 2x kaynakta calis
    w2, h2 = width * 2, height * 2

    cmd = [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error", "-stats"]

    lens = []
    for i, s in enumerate(plan.shots):
        # son cekim disinda her cekim gecis suresi kadar uzun tutulur ki
        # crossfade'ler toplam sureyi kisaltmasin (ses ile senkron kalsin)
        L = s.duration + (xdur if i < n - 1 else 0.0)
        lens.append(L)
        cmd += ["-loop", "1", "-framerate", str(fps), "-t", f"{L:.3f}", "-i", str(s.image)]
    for a in plan.audios:
        cmd += ["-i", str(a)]

    fc = []
    for i, (s, L) in enumerate(zip(plan.shots, lens)):
        frames = max(2, int(round(L * fps)))
        fx, fy = cover_crop_focus(s.image, s.focus[0], s.focus[1], aspect)
        z, x, y = zoompan_expr(s, frames, fx, fy)
        fc.append(
            f"[{i}:v]scale={w2}:{h2}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={w2}:{h2},setsar=1,"
            f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={width}x{height}:fps={fps},"
            f"trim=duration={L:.3f},setpts=PTS-STARTPTS,"
            f"fps={fps},settb=AVTB,format=yuv420p[v{i}]"
        )

    if n == 1:
        fc.append("[v0]copy[vout]")
    else:
        prev, acc = "[v0]", 0.0
        for i in range(1, n):
            acc += plan.shots[i - 1].duration          # bir sonraki cekimin baslama ani
            label = "[vout]" if i == n - 1 else f"[x{i}]"
            fc.append(
                f"{prev}[v{i}]xfade=transition={transition}:"
                f"duration={xdur}:offset={acc:.3f}{label}"
            )
            prev = label

    a0 = n
    alist = "".join(f"[{a0 + j}:a]" for j in range(len(plan.audios)))
    fc.append(
        f"{alist}concat=n={len(plan.audios)}:v=0:a=1[acat];"
        f"[acat]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]"
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    cmd += [
        "-filter_complex", ";".join(fc),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
        "-pix_fmt", "yuv420p", "-r", str(fps),
        "-c:a", "aac", "-b:a", audio_bitrate,
        "-movflags", "+faststart",
        "-shortest",
        str(out),
    ]
    return cmd


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Seslendirme + gorsellerden Ken Burns'lu video")
    ap.add_argument("--audio-dir", default="assets/audio")
    ap.add_argument("--image-dir", default="assets/images")
    ap.add_argument("--out", default="out/final.mp4")
    ap.add_argument("--config", default="edit.json", help="gorsel bazli odak/zoom override")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--zoom", type=float, default=1.14, help="maksimum zoom orani")
    ap.add_argument("--transition-duration", type=float, default=1.0)
    ap.add_argument("--transition", default="fade", help="ffmpeg xfade gecisi")
    ap.add_argument("--min-shot", type=float, default=4.0,
                    help="bir gorselin ekranda kalacagi minimum sure")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--audio-bitrate", default="192k")
    ap.add_argument("--preview", action="store_true", help="hizli, dusuk kaliteli on izleme")
    ap.add_argument("--plan", action="store_true", help="sadece plani yazdir")
    args = ap.parse_args()

    if args.preview:
        args.width, args.height = 960, 540
        args.crf, args.preset = 28, "veryfast"
        if args.out == "out/final.mp4":
            args.out = "out/preview.mp4"

    adir, idir = Path(args.audio_dir), Path(args.image_dir)
    audios = sorted((p for p in adir.glob("*") if p.suffix.lower() in AUDIO_EXT), key=natural_key)
    images = sorted((p for p in idir.glob("*") if p.suffix.lower() in IMAGE_EXT), key=natural_key)
    if not audios:
        sys.exit(f"{adir} icinde ses dosyasi yok (1.wav ... 11.wav bekleniyor).")
    if not images:
        sys.exit(f"{idir} icinde gorsel yok.")

    cfg_path = Path(args.config)
    cfg = json.loads(cfg_path.read_text()).get("images", {}) if cfg_path.exists() else {}

    plan = build_plan(audios, images, cfg, args.zoom, args.min_shot)
    total = sum(s.duration for s in plan.shots)

    print(f"{len(audios)} ses / {len(images)} gorsel / {len(plan.shots)} cekim  "
          f"toplam {int(total // 60)}:{total % 60:05.2f}")
    for i, s in enumerate(plan.shots, 1):
        print(f"  {i:>3}. {s.audio:<10} {s.image.name:<28} {s.duration:>7.2f}s  "
              f"{s.move:<3} zoom->{s.zoom:.2f}  odak=({s.focus[0]:.2f},{s.focus[1]:.2f})")

    if args.plan:
        return

    cmd = build_command(plan, Path(args.out), args.width, args.height, args.fps,
                        args.transition_duration, args.transition, args.crf,
                        args.preset, args.audio_bitrate)
    print("\nrender basliyor...", file=sys.stderr)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("\nffmpeg komutu:\n" + " ".join(shlex.quote(c) for c in cmd), file=sys.stderr)
        sys.exit(r.returncode)
    print(f"\nhazir: {args.out}")


if __name__ == "__main__":
    main()
