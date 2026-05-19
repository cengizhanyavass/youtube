import os
import glob
from pathlib import Path
from moviepy.editor import (
    ImageClip, AudioFileClip,
    concatenate_videoclips, CompositeVideoClip
)
from PIL import Image
import numpy as np


SUPPORTED_IMAGES = (".jpg", ".jpeg", ".png", ".webp")
OUTPUT_FPS = 24
OUTPUT_CODEC = "libx264"
OUTPUT_AUDIO_CODEC = "aac"
TARGET_SIZE = (1920, 1080)


def load_sorted_images(folder: str) -> list[str]:
    paths = []
    for ext in SUPPORTED_IMAGES:
        paths += glob.glob(os.path.join(folder, f"*{ext}"))
        paths += glob.glob(os.path.join(folder, f"*{ext.upper()}"))
    paths = sorted(set(paths), key=lambda p: os.path.basename(p))
    if not paths:
        raise FileNotFoundError(f"Görsel bulunamadı: {folder}")
    return paths


def pad_image_to_size(img_path: str, target: tuple[int, int]) -> np.ndarray:
    img = Image.open(img_path).convert("RGB")
    img.thumbnail(target, Image.LANCZOS)
    background = Image.new("RGB", target, (0, 0, 0))
    offset = ((target[0] - img.width) // 2, (target[1] - img.height) // 2)
    background.paste(img, offset)
    return np.array(background)


def build_video(
    images_folder: str,
    audio_path: str,
    output_path: str,
    fade_duration: float = 0.4,
    progress_callback=None,
) -> str:
    image_paths = load_sorted_images(images_folder)
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    n = len(image_paths)
    duration_each = total_duration / n

    clips = []
    for i, img_path in enumerate(image_paths):
        if progress_callback:
            progress_callback(i, n, os.path.basename(img_path))

        frame = pad_image_to_size(img_path, TARGET_SIZE)
        clip = ImageClip(frame, duration=duration_each)

        if fade_duration > 0 and duration_each > fade_duration * 2:
            clip = clip.fadein(fade_duration).fadeout(fade_duration)

        clips.append(clip)

    if progress_callback:
        progress_callback(n, n, "Video birleştiriliyor...")

    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    video.write_videofile(
        output_path,
        fps=OUTPUT_FPS,
        codec=OUTPUT_CODEC,
        audio_codec=OUTPUT_AUDIO_CODEC,
        preset="fast",
        verbose=False,
        logger=None,
    )

    audio.close()
    video.close()
    return output_path
