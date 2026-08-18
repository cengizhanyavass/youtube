#!/usr/bin/env python3
"""2D stickman (çöp adam) animasyon motoru — saf Pillow + ffmpeg, ücretsiz.

Açı sistemi: her uzuv mutlak açıyla tanımlanır. 0 = aşağı, 90 = sağa,
180 = yukarı, -90 = sola. Ekran koordinatında y aşağı büyür.

Tek başına önizleme:
  python tools/stickman.py --action wave --seconds 3 --out out/wave.mp4
"""
from __future__ import annotations

import argparse
import math
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- pose modeli

BASE_POSE = {
    "lean": 0.0,      # gövde eğimi (derece, + sağa)
    "head": 0.0,      # kafa eğimi
    "sh_l": -8.0, "el_l": -8.0,    # sol omuz / dirsek
    "sh_r": 8.0, "el_r": 8.0,      # sağ omuz / dirsek
    "hip_l": -10.0, "kn_l": -6.0,
    "hip_r": 10.0, "kn_r": 6.0,
    "dx": 0.0, "dy": 0.0,          # tüm figürün kayması (piksel oranı, boy cinsinden)
    "squash": 1.0,                 # dikey ezilme (zıplama/çömelme)
}


def pose(**kw) -> dict:
    p = dict(BASE_POSE)
    p.update(kw)
    return p


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def blend(p1: dict, p2: dict, t: float) -> dict:
    return {k: lerp(p1[k], p2[k], t) for k in BASE_POSE}


def ease(t: float) -> float:
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ aksiyonlar
# Her aksiyon: faz t (0..1) -> poz. Süreye göre tekrar eden hareketler
# 'cycles' ile hızlandırılır.

def a_idle(t):
    b = math.sin(t * math.tau * 2)
    return pose(sh_l=-8 + b * 2, sh_r=8 - b * 2, dy=b * 0.006, head=b * 1.5)


def a_wave(t):
    w = math.sin(t * math.tau * 3)
    return pose(sh_r=140, el_r=150 + w * 22, sh_l=-10, head=-4, dy=math.sin(t * math.tau) * 0.004)


def a_talk(t):
    w = math.sin(t * math.tau * 2)
    return pose(sh_r=45 + w * 12, el_r=95 + w * 18, sh_l=-25, el_l=-70, head=w * 2.5)


def a_point_right(t):
    e = ease(min(1.0, t * 3))
    return pose(sh_r=lerp(8, 88, e), el_r=lerp(8, 92, e), sh_l=-12, lean=lerp(0, 4, e))


def a_point_left(t):
    p = a_point_right(t)
    return pose(sh_l=-p["sh_r"], el_l=-p["el_r"], sh_r=12, lean=-p["lean"])


def a_walk(t):
    s = math.sin(t * math.tau)
    c = math.cos(t * math.tau)
    return pose(
        hip_r=s * 28, kn_r=s * 28 + max(0, -c) * 26,
        hip_l=-s * 28, kn_l=-s * 28 + max(0, c) * 26,
        sh_r=-s * 26, el_r=-s * 26 - 12,
        sh_l=s * 26, el_l=s * 26 + 12,
        dy=abs(s) * -0.012, lean=2,
    )


def a_run(t):
    p = a_walk(t)
    return pose(**{**p, "lean": 10, "hip_r": p["hip_r"] * 1.5, "hip_l": p["hip_l"] * 1.5,
                   "el_r": -80, "el_l": 80, "dy": p["dy"] * 1.8})


def a_jump(t):
    h = math.sin(min(1.0, t) * math.pi)
    return pose(dy=-h * 0.32, squash=1 + h * 0.06,
                sh_r=lerp(8, 165, h), sh_l=lerp(-8, -165, h),
                el_r=lerp(8, 170, h), el_l=lerp(-8, -170, h),
                hip_r=lerp(6, 34, h), hip_l=lerp(-6, -34, h),
                kn_r=lerp(4, 70, h), kn_l=lerp(-4, -70, h))


def a_think(t):
    w = math.sin(t * math.tau) * 3
    return pose(sh_r=62, el_r=132 + w, sh_l=-18, el_l=-64, head=8 + w * 0.4, lean=-3)


def a_cheer(t):
    w = math.sin(t * math.tau * 2)
    return pose(sh_r=168, el_r=172, sh_l=-168, el_l=-172,
                dy=-abs(w) * 0.05, head=w * 3)


def a_fall(t):
    e = ease(min(1.0, t))
    return pose(lean=lerp(0, 82, e), dy=lerp(0, 0.28, e),
                sh_r=lerp(8, 120, e), sh_l=lerp(-8, -120, e),
                hip_r=lerp(6, 40, e), kn_r=lerp(4, 60, e),
                hip_l=lerp(-6, -20, e), kn_l=lerp(-4, -50, e))


def a_shrug(t):
    e = ease(min(1.0, t * 2))
    return pose(sh_r=70, el_r=118, sh_l=-70, el_l=-118, head=lerp(0, -5, e))


def a_sit(t):
    return pose(dy=0.16, hip_r=78, kn_r=8, hip_l=-72, kn_l=-6, sh_r=30, el_r=64,
                sh_l=-30, el_l=-64, lean=-4)


ACTIONS = {
    "idle": a_idle, "wave": a_wave, "talk": a_talk, "walk": a_walk, "run": a_run,
    "jump": a_jump, "think": a_think, "cheer": a_cheer, "fall": a_fall,
    "shrug": a_shrug, "sit": a_sit, "point_right": a_point_right,
    "point_left": a_point_left,
}


# ------------------------------------------------------------------- çizim

@dataclass
class Style:
    bg: str = "#0e1116"
    ink: str = "#f2f4f8"
    accent: str = "#ffcc33"
    ground: str = "#2a3040"
    thickness: int = 0          # 0 = boya göre otomatik
    bubble_bg: str = "#ffffff"
    bubble_ink: str = "#111111"


@dataclass
class Actor:
    x: float = 0.5              # ekran genişliğinin oranı
    y: float = 0.82             # ayak hizası (yükseklik oranı)
    height: float = 0.45        # figür boyu (yükseklik oranı)
    color: str | None = None
    flip: bool = False
    action: str = "idle"
    cycles: float = 1.0
    bubble: str | None = None
    label: str | None = None
    _t: float = field(default=0.0, repr=False)


def _seg(x, y, ang, ln):
    r = math.radians(ang)
    return x + math.sin(r) * ln, y + math.cos(r) * ln


def draw_actor(d: ImageDraw.ImageDraw, W: int, H: int, ac: Actor, p: dict, style: Style):
    color = ac.color or style.ink
    h = ac.height * H
    w = style.thickness or max(3, int(h * 0.028))
    flip = -1 if ac.flip else 1

    # oranlar (toplam boy 1.0): kafa .16, gövde .30, bacak .46
    head_r = h * 0.085
    torso = h * 0.30 * p["squash"]
    upper = h * 0.15
    fore = h * 0.14
    thigh = h * 0.23 * p["squash"]
    shin = h * 0.21 * p["squash"]

    foot_x = ac.x * W + p["dx"] * W
    foot_y = ac.y * H + p["dy"] * H
    pelvis_x, pelvis_y = foot_x, foot_y - (thigh + shin)

    lean = p["lean"] * flip
    neck_x, neck_y = _seg(pelvis_x, pelvis_y, 180 + lean, torso)

    def limb(x, y, a1, l1, a2, l2):
        jx, jy = _seg(x, y, a1 * flip + lean, l1)
        ex, ey = _seg(jx, jy, a2 * flip + lean, l2)
        d.line([x, y, jx, jy], fill=color, width=w)
        d.line([jx, jy, ex, ey], fill=color, width=w)
        d.ellipse([jx - w / 2, jy - w / 2, jx + w / 2, jy + w / 2], fill=color)
        return ex, ey

    # bacaklar, gövde, kollar
    limb(pelvis_x, pelvis_y, p["hip_l"], thigh, p["kn_l"], shin)
    limb(pelvis_x, pelvis_y, p["hip_r"], thigh, p["kn_r"], shin)
    d.line([pelvis_x, pelvis_y, neck_x, neck_y], fill=color, width=w)
    limb(neck_x, neck_y, p["sh_l"], upper, p["el_l"], fore)
    hand = limb(neck_x, neck_y, p["sh_r"], upper, p["el_r"], fore)

    # kafa
    hx, hy = _seg(neck_x, neck_y, 180 + lean + p["head"] * flip, head_r * 1.15)
    d.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r],
              outline=color, width=w, fill=style.bg)
    eye = max(2, int(head_r * 0.16))
    for sx in (-0.38, 0.34):
        ex = hx + head_r * sx * flip
        ey = hy - head_r * 0.18
        d.ellipse([ex - eye, ey - eye, ex + eye, ey + eye], fill=color)
    d.arc([hx - head_r * 0.5, hy + head_r * 0.02, hx + head_r * 0.5, hy + head_r * 0.6],
          start=20, end=160, fill=color, width=max(2, w // 2))
    return {"head": (hx, hy - head_r), "hand": hand, "neck": (neck_x, neck_y)}


def wrap(text: str, font, max_w: int, d: ImageDraw.ImageDraw) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def load_font(size: int):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                 "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                 "C:/Windows/Fonts/arialbd.ttf"):
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


def draw_bubble(d: ImageDraw.ImageDraw, W: int, H: int, anchor, text: str, style: Style):
    font = load_font(max(16, int(H * 0.032)))
    max_w = int(W * 0.34)
    lines = wrap(text, font, max_w, d)
    lh = int(font.size * 1.32)
    tw = int(max(d.textlength(l, font=font) for l in lines))
    pad = int(font.size * 0.6)
    bw, bh = tw + pad * 2, lh * len(lines) + pad * 2

    ax, ay = anchor
    x0 = min(max(int(ax - bw / 2), 10), W - bw - 10)
    y0 = max(int(ay - bh - H * 0.05), 10)
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=pad,
                        fill=style.bubble_bg, outline=style.bubble_ink, width=3)
    tail = [(ax - pad * 0.5, y0 + bh - 2), (ax + pad * 0.5, y0 + bh - 2),
            (ax, y0 + bh + pad * 1.1)]
    d.polygon(tail, fill=style.bubble_bg, outline=style.bubble_ink)
    for i, line in enumerate(lines):
        d.text((x0 + pad, y0 + pad + i * lh), line, font=font, fill=style.bubble_ink)


def render_frame(W: int, H: int, actors: list[Actor], phases: list[float],
                 style: Style, title: str | None = None,
                 subtitle: str | None = None) -> Image.Image:
    img = Image.new("RGB", (W, H), style.bg)
    d = ImageDraw.Draw(img)
    gy = int(H * 0.83)
    d.line([0, gy, W, gy], fill=style.ground, width=max(2, H // 400))

    for ac, ph in zip(actors, phases):
        fn = ACTIONS.get(ac.action, a_idle)
        pts = draw_actor(d, W, H, ac, fn(ph), style)
        if ac.bubble:
            draw_bubble(d, W, H, pts["head"], ac.bubble, style)
        if ac.label:
            f = load_font(max(14, int(H * 0.026)))
            tw = d.textlength(ac.label, font=f)
            d.text((ac.x * W - tw / 2, ac.y * H + H * 0.02), ac.label, font=f, fill=style.accent)

    if title:
        f = load_font(max(24, int(H * 0.07)))
        tw = d.textlength(title, font=f)
        d.text(((W - tw) / 2, H * 0.06), title, font=f, fill=style.accent)
    if subtitle:
        f = load_font(max(18, int(H * 0.042)))
        for i, line in enumerate(wrap(subtitle, f, int(W * 0.86), d)[-2:]):
            tw = d.textlength(line, font=f)
            y = H * 0.88 + i * f.size * 1.25
            d.text(((W - tw) / 2 + 2, y + 2), line, font=f, fill="#000000")
            d.text(((W - tw) / 2, y), line, font=f, fill=style.ink)
    return img


# ------------------------------------------------------------------ ffmpeg

class VideoWriter:
    """Kareleri ffmpeg'e rawvideo olarak akıtır (disk'e PNG yazmaz -> hızlı)."""

    def __init__(self, path: str, W: int, H: int, fps: int, ffmpeg: str = "ffmpeg"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        cmd = [ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
               "-pix_fmt", "yuv420p", path]
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        self.path = path

    def add(self, img: Image.Image):
        self.proc.stdin.write(img.tobytes())

    def close(self):
        self.proc.stdin.close()
        rc = self.proc.wait()
        if rc != 0:
            raise RuntimeError(f"ffmpeg hata kodu {rc}")
        return self.path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--action", default="wave", choices=sorted(ACTIONS))
    ap.add_argument("--seconds", type=float, default=3)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--bubble")
    ap.add_argument("--title")
    ap.add_argument("--cycles", type=float, default=0, help="0 = saniyede 1 dongu")
    ap.add_argument("--out", default="out/preview.mp4")
    args = ap.parse_args()

    style = Style()
    actor = Actor(action=args.action, bubble=args.bubble)
    cycles = args.cycles or args.seconds
    n = max(1, int(args.seconds * args.fps))
    vw = VideoWriter(args.out, args.width, args.height, args.fps)
    for i in range(n):
        ph = (i / args.fps) * (cycles / args.seconds) % 1.0
        vw.add(render_frame(args.width, args.height, [actor], [ph], style, title=args.title))
    print(vw.close())


if __name__ == "__main__":
    main()
