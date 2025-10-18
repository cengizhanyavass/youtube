"""Command line interface for the medieval content generator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from .ideas import VideoIdeaGenerator
from .prompts import (
    ImagePromptGenerator,
    ImagePromptSettings,
    ThumbnailPromptConfig,
    ThumbnailPromptGenerator,
    _extract_keywords,
)
from .script import ScriptGenerator


def generate_payload(
    theme: str,
    title: str,
    *,
    ideas_count: int = 20,
    script_words: int = 32000,
    image_prompts: int = 24,
    seed: int | None = None,
    preview: bool = False,
) -> Dict[str, Any]:
    """Run the full content generation pipeline and return the payload.

    This helper is shared by both the CLI and the desktop GUI so that each
    interface relies on a single implementation of the business logic.
    """

    idea_generator = VideoIdeaGenerator(
        VideoIdeaGenerator.default_config(theme), seed=seed
    )
    ideas = idea_generator.generate(ideas_count)

    target_words = max(1000, int(script_words * 0.05)) if preview else script_words
    script_gen = ScriptGenerator(
        theme,
        target_word_count=target_words,
        seed=seed,
    )
    sections = script_gen.generate()

    script_texts = [section.body for section in sections]

    image_settings = ImagePromptSettings()
    image_gen = ImagePromptGenerator(settings=image_settings)
    image_prompts_payload = image_gen.build_prompts(
        script_texts,
        ideas,
        theme=theme,
        total_prompts=image_prompts,
    )

    thumbnail_gen = ThumbnailPromptGenerator(
        ThumbnailPromptConfig(theme=theme, title=title)
    )
    keywords = _extract_keywords("\n".join(script_texts + ideas), limit=20)
    thumbnail_prompt = thumbnail_gen.build_prompt(keywords)

    payload: Dict[str, Any] = {
        "theme": theme,
        "title": title,
        "target_word_count": target_words,
        "ideas": ideas,
        "script": [
            {
                "title": section.title,
                "body": section.body,
                "word_count": section.word_count(),
            }
            for section in sections
        ],
        "total_script_words": sum(section.word_count() for section in sections),
        "image_prompts": image_prompts_payload,
        "thumbnail_prompt": thumbnail_prompt,
    }

    return payload


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate medieval-themed video ideas, scripts, and image prompts.",
    )
    parser.add_argument("theme", help="Primary theme focus, e.g. 'Medieval Frontier Families'.")
    parser.add_argument(
        "title",
        help="Title that anchors the generated script and thumbnail prompt.",
    )
    parser.add_argument(
        "--ideas-count",
        type=int,
        default=20,
        help="How many video ideas to produce (default: 20).",
    )
    parser.add_argument(
        "--script-words",
        type=int,
        default=32000,
        help="Target word count for the generated script (default: 32000).",
    )
    parser.add_argument(
        "--image-prompts",
        type=int,
        default=24,
        help="Number of scenic illustration prompts to create (default: 24).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducible output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional file path to write the generated payload as JSON.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate a short preview script (5%% of requested words) for quick inspection.",
    )
    return parser


def main(argv: List[str] | None = None) -> Dict[str, Any]:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    payload = generate_payload(
        args.theme,
        args.title,
        ideas_count=args.ideas_count,
        script_words=args.script_words,
        image_prompts=args.image_prompts,
        seed=args.seed,
        preview=args.preview,
    )

    if args.output:
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return payload


if __name__ == "__main__":
    main()
