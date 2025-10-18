"""Prompt generation utilities for images and thumbnails."""

from __future__ import annotations

import collections
import re
import itertools
from dataclasses import dataclass
from typing import Iterable, List, Sequence


STOP_WORDS = {
    "the",
    "a",
    "and",
    "of",
    "to",
    "in",
    "that",
    "it",
    "with",
    "for",
    "on",
    "as",
    "is",
    "its",
    "into",
    "at",
    "by",
    "from",
    "their",
    "you",
    "your",
    "they",
    "them",
    "this",
    "was",
    "were",
    "are",
    "be",
    "over",
    "under",
    "around",
    "against",
    "inside",
    "outside",
    "across",
    "within",
    "without",
    "while",
    "every",
    "another",
    "still",
}


def _extract_keywords(text: str, *, limit: int = 20) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]+", text.lower())
    freq: collections.Counter[str] = collections.Counter()
    for word in words:
        if word in STOP_WORDS or len(word) < 4:
            continue
        freq[word] += 1
    return [word for word, _ in freq.most_common(limit)]


@dataclass
class ImagePromptSettings:
    """Configuration for scenic prompt creation."""

    aspect_ratio: str = "16:9"
    style_suffix: str = (
        "medieval manuscript illustration, flat two-dimensional, parchment texture, natural pigments, "
        "clear outlines, storybook medieval art, decorative illuminated manuscript style, highly detailed, "
        "historically inspired artwork"
    )


class ImagePromptGenerator:
    """Generate richly detailed illustration prompts derived from script text."""

    def __init__(self, *, settings: ImagePromptSettings | None = None) -> None:
        self._settings = settings or ImagePromptSettings()

    def build_prompts(
        self,
        script_sections: Sequence[str],
        ideas: Sequence[str],
        *,
        theme: str,
        total_prompts: int = 24,
    ) -> List[str]:
        if total_prompts < 4:
            raise ValueError("total_prompts must be at least 4")
        if total_prompts > 40:
            raise ValueError("total_prompts must be 40 or fewer")

        combined_text = "\n".join(script_sections) + "\n" + "\n".join(ideas)
        keywords = _extract_keywords(combined_text, limit=60)
        if not keywords:
            keywords = ["winter", "camp", "watch", "families", "embers"]

        prompts: List[str] = []
        keyword_cycle = itertools.cycle(keywords)

        keyword_rewrites = {
            "cold": "biting cold",
            "night": "midnight silence",
            "watch": "the vigilant watch",
            "breath": "clouded breath",
            "quiet": "hushed whispers",
            "rhythm": "shared heartbeats",
            "winter": "winter endurance",
            "palisade": "fortified palisade",
            "frontier": "frontier resolve",
            "through": None,
            "between": None,
            "each": None,
            "like": None,
        }

        def next_keyword() -> str | None:
            for _ in range(len(keywords)):
                candidate = next(keyword_cycle)
                rewrite = keyword_rewrites.get(candidate, candidate)
                if rewrite:
                    return rewrite
            return None

        def keyword_clause() -> str:
            primary = next_keyword()
            secondary = next_keyword()
            selected = [phrase for phrase in (primary, secondary) if phrase]
            if not selected:
                return "highlighting winter endurance"
            if len(selected) == 1:
                return f"highlighting {selected[0]}"
            return f"highlighting {selected[0]} and {selected[1]}"

        focus_cycle = itertools.cycle(
            [
                f"{theme.lower()} night watch guardians",
                f"{theme.lower()} storytellers and listeners",
                f"{theme.lower()} scouts trading reports",
                f"{theme.lower()} healers preparing remedies",
                f"{theme.lower()} elders guiding apprentices",
            ]
        )
        object_cycle = itertools.cycle(
            [
                "an ember-rich brazier",
                "layered wool blankets",
                "a steaming cauldron of broth",
                "a spread of winter maps",
                "a cluster of handmade talismans",
            ]
        )
        atmosphere_cycle = itertools.cycle(
            [
                "frost-laced breath swirling like ghostly banners",
                "snowflakes catching torchlight in bright halos",
                "smoke curling beneath low canvas beams",
                "wind rattling shields stacked as windbreaks",
                "quiet hymns softening the restless dark",
            ]
        )
        structure_cycle = itertools.cycle(
            [
                "timber buttresses braced with rope",
                "canvas walls weighted by snow-packed crates",
                "shield walls leaned in a defensive crescent",
                "woven reed mats sealing the draft",
                "layered furs draped along the ridgepole",
            ]
        )
        environment_cycle = itertools.cycle(
            [
                "a snowbound palisade",
                "moonlit pine stands",
                "frozen riverbanks",
                "stone keep courtyards",
                "wind-scoured ridgelines",
            ]
        )
        defensive_cycle = itertools.cycle(
            [
                "raising a sentinel horn",
                "tightening fur-lined cloaks",
                "checking arrow bundles",
                "stacking firewood into a heat wall",
                "mapping rotating watch partners",
            ]
        )
        memory_cycle = itertools.cycle(
            [
                "scribbled night watch ledgers",
                "whispered lullabies from earlier winters",
                "etched tally marks of survived storms",
                "carefully wrapped heirloom charms",
                "shared myths about frost spirits",
            ]
        )
        light_cycle = itertools.cycle(
            [
                "lantern glow",
                "pine resin torches",
                "shielded candles",
                "low coals painted gold",
                "moonlight cutting through the canvas seam",
            ]
        )
        sustenance_cycle = itertools.cycle(
            [
                "juniper tea",
                "roasted chestnuts",
                "honey oat cakes",
                "thick barley stew",
                "mulled cider",
            ]
        )
        weather_cycle = itertools.cycle(
            [
                "encroaching blizzards",
                "ice-needle gusts",
                "sleet hammering the ridge",
                "snow squalls curling like specters",
                "midnight frost settling on armor",
            ]
        )

        templates = [
            "{focus} gathered around {obj}, {atmosphere}, {highlight}",
            "{focus} reinforcing {structure} beside {environment}, {highlight}",
            "{focus} sharing {sustenance} near {environment}, {highlight}",
            "{focus} preparing by {defensive}, {highlight} as {weather} looms",
            "{focus} recording {memory} under {light}, {highlight}",
        ]

        while len(prompts) < total_prompts:
            template = templates[len(prompts) % len(templates)]
            prompts.append(
                self._format_prompt(
                    template,
                    focus=next(focus_cycle),
                    obj=next(object_cycle),
                    atmosphere=next(atmosphere_cycle),
                    highlight=keyword_clause(),
                    structure=next(structure_cycle),
                    environment=next(environment_cycle),
                    sustenance=next(sustenance_cycle),
                    defensive=next(defensive_cycle),
                    weather=next(weather_cycle),
                    memory=next(memory_cycle),
                    light=next(light_cycle),
                )
            )

        return prompts

    def _format_prompt(self, template: str, **parts: str) -> str:
        base = template.format(**parts)
        return (
            f"{base}, –aspect ratio {self._settings.aspect_ratio}, "
            f"{self._settings.style_suffix}"
        )


@dataclass
class ThumbnailPromptConfig:
    """Configuration for the thumbnail prompt generator."""

    theme: str
    title: str


class ThumbnailPromptGenerator:
    """Produce a single AI prompt for a YouTube thumbnail."""

    def __init__(self, config: ThumbnailPromptConfig) -> None:
        self._config = config

    def build_prompt(self, keywords: Iterable[str]) -> str:
        focus_keywords = self._format_keywords(keywords)

        characters = " and ".join(
            [
                f"overwhelmed {self._config.theme.lower()} scout",
                f"determined {self._config.theme.lower()} elder",
            ]
        )
        props = ", ".join(
            [
                "frost-tipped shields",
                "steaming wooden bowls",
                "ruffled cloaks",
                "quirky talismans",
            ]
        )

        return (
            f"Cartoonish illustration, exaggerated expressions, comedic medieval vibe. "
            f"Depict {characters} reacting to {', '.join(focus_keywords)}. Include medieval props such as {props}. "
            f"Pure white background, flat muted earthy tones, no gradients, clear outlines, two to four characters, "
            f"big eyes, dramatic mouths. Title inspiration: '{self._config.title}'."
        )

    def _format_keywords(self, keywords: Iterable[str]) -> List[str]:
        rewrites = {
            "cold": "biting cold",
            "night": "midnight silence",
            "watch": "the vigilant watch",
            "breath": "clouded breath",
            "winter": "winter endurance",
            "quiet": "hushed whispers",
            "rhythm": "shared heartbeats",
            "each": None,
            "through": None,
            "like": None,
            "between": None,
        }

        formatted: List[str] = []
        for word in keywords:
            phrase = rewrites.get(word, word)
            if not phrase:
                continue
            if phrase not in formatted:
                formatted.append(phrase)
            if len(formatted) == 4:
                break

        if not formatted:
            formatted = [self._config.theme.lower(), "winter endurance", "lantern glow"]

        return formatted
