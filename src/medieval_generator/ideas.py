"""Video idea generation utilities."""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class IdeaConfig:
    """Configuration for generating themed video ideas."""

    theme: str
    focus_keywords: Sequence[str]
    tonal_guidelines: Sequence[str]
    sensory_hooks: Sequence[str]
    historical_lenses: Sequence[str]


class VideoIdeaGenerator:
    """Creates long-running idea streams for immersive history scripts."""

    def __init__(self, config: IdeaConfig, *, seed: int | None = None) -> None:
        self._config = config
        self._random = random.Random(seed)

    def _cycle_from(self, values: Sequence[str]) -> Iterable[str]:
        shuffled = list(values)
        self._random.shuffle(shuffled)
        return itertools.cycle(shuffled)

    def generate(self, count: int) -> List[str]:
        """Return ``count`` richly described video concepts."""

        if count <= 0:
            raise ValueError("count must be positive")

        base_titles = self._cycle_from(
            [
                "How {theme} Survivors Endured Nights of Relentless Frost",
                "What Kept {theme} Communities Alive After Sundown",
                "Inside the Night Watch of {theme} Guardians",
                "Secrets of Midnight Rituals Among {theme} Settlements",
                "Why {theme} Storytellers Whispered Through the Cold",
                "Unexpected Comforts that Saved {theme} Travelers",
                "What {theme} Children Remembered About Winter Darkness",
            ]
        )
        narrative_hooks = self._cycle_from(self._config.tonal_guidelines)
        sensory = self._cycle_from(self._config.sensory_hooks)
        historical = self._cycle_from(self._config.historical_lenses)

        ideas: List[str] = []
        for idx in range(count):
            template = next(base_titles)
            hook = next(narrative_hooks)
            sense = next(sensory)
            lens = next(historical)
            keyword = self._random.choice(self._config.focus_keywords)

            idea = template.format(theme=self._config.theme)
            idea = (
                f"{idea}: {hook} with {sense}, explored through {lens} and the forgotten stories "
                f"of {keyword} keepers."
            )
            ideas.append(idea)

        return ideas

    @staticmethod
    def default_config(theme: str) -> IdeaConfig:
        """Create a configuration tuned for long-form medieval ambience."""

        lowered = theme.lower()
        focus_pool = [
            f"{lowered} healers",
            f"{lowered} scouts",
            f"{lowered} storytellers",
            f"{lowered} elders",
            f"{lowered} apprentices",
            f"{lowered} artisans",
            f"{lowered} watchmen",
            f"{lowered} wanderers",
        ]
        tonal_guidelines = [
            "a hushed, second-person narrative that feels both intimate and urgent",
            "immersive sensory threads that stitch together cold, courage, and community",
            "slow-burning tension balanced with moments of fragile warmth",
            "a meditation on endurance that still flirts with whispered superstition",
            "human-scale observations that make history feel lived-in and immediate",
        ]
        sensory_hooks = [
            "frost-silvered breath and aching limbs",
            "smoke-heavy cloaks and heartbeat drums",
            "shivering torchlight and damp straw underfoot",
            "crackling ice on water buckets and shared blankets",
            "embers glowing like watchful eyes over resting families",
        ]
        historical_lenses = [
            "chronicles preserved by monastic scribes",
            "oral histories passed from elder to child",
            "merchant letters detailing supply shortages",
            "battlefield reports smudged with soot and wax",
            "folk remedies recorded beside winter planting notes",
        ]
        return IdeaConfig(
            theme=theme,
            focus_keywords=focus_pool,
            tonal_guidelines=tonal_guidelines,
            sensory_hooks=sensory_hooks,
            historical_lenses=historical_lenses,
        )
