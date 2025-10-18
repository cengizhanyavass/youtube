"""Self-contained medieval content generator that outputs a JSON payload.

This module replicates the package pipeline in a single file so it can be
downloaded and executed without installing the full project. Run it like:

    python standalone_generator.py "Frontier Winter Watch" \
        "How Frontier Winter Watches Kept the Night at Bay" \
        --preview --ideas-count 15 --image-prompts 20 --output preview.json

The resulting JSON can be inspected with tools such as ``python -m json.tool``.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence


# ---------------------------------------------------------------------------
# Idea generation
# ---------------------------------------------------------------------------


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
        for _ in range(count):
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


# ---------------------------------------------------------------------------
# Script generation
# ---------------------------------------------------------------------------


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


@dataclass
class Section:
    """Represents a generated script section."""

    title: str
    body: str

    def word_count(self) -> int:
        return _word_count(self.body)


class ScriptGenerator:
    """Generate immersive, historically flavored narrative scripts."""

    def __init__(
        self,
        theme: str,
        *,
        target_word_count: int = 32000,
        seed: int | None = None,
        section_target_words: int = 1200,
    ) -> None:
        if target_word_count < 1000:
            raise ValueError("target_word_count must be at least 1000 words")
        if section_target_words < 400:
            raise ValueError("section_target_words must be at least 400 words")
        self._theme = theme
        self._target_words = target_word_count
        self._section_target = section_target_words
        self._random = random.Random(seed)
        self._section_titles = self._build_section_titles()
        self._paragraph_templates = self._build_paragraph_templates()
        self._transition_templates = self._build_transition_templates()
        self._closing_templates = self._build_closing_templates()

    def _build_section_titles(self) -> Iterable[str]:
        titles = [
            "Waking to the Chill in {theme} Hearths",
            "The Shared Warmth of {theme} Sleepers",
            "Guarding the Perimeter of {theme} Encampments",
            "Quiet Labors Before Dawn in {theme} Settlements",
            "How {theme} Storytellers Passed the Night",
            "Rituals of Comfort Among {theme} Families",
            "Watchfires and Whispered Fears of {theme} Wanderers",
            "Ingenuity that Kept {theme} Travelers Alive",
            "The Communal Heartbeat of {theme} Nights",
            "When {theme} Dreamers Met the Cold",
        ]
        shuffled = titles * 4
        self._random.shuffle(shuffled)
        return itertools.cycle([title.format(theme=self._theme) for title in shuffled])

    def _build_paragraph_templates(self) -> Sequence[Sequence[str]]:
        """Return layered paragraph templates containing sentence frames."""

        descriptive = [
            "You lie within a {shelter}, every sense alive to the {adjective} {air} swirling around you.",
            "The {structure} groans softly, and you feel the {texture} {floor} against your palms as you brace yourself.",
            "Breath mingles with {scent} and the quiet rustle of {companion_sound}, a reminder that survival is collective.",
            "Beyond the {barrier}, the night claws with {weather}, yet inside you cling to {comfort_item} like a vow.",
            "Frost traces the rafters in {pattern} lines, glittering whenever the fire exhales a weary glow.",
            "Your heartbeat answers the muted rhythm of {distant_noise}, each pulse keeping pace with the darkness outside.",
        ]

        historical = [
            "A mainstream historical fact whispers that {historical_fact}—and tonight it feels undeniably true.",
            "Chroniclers noted how {historical_event}, and you sense that legacy in the way the camp holds its breath.",
            "Scholars still argue whether {debated_topic}, yet you rest in the uncomfortable space between their theories.",
            "You recall records of {archival_memory}, copied by hands numb with cold, insisting that vigilance was everything.",
            "Merchant ledgers scribbled about {logistical_issue}, each line an echo of the scarcity pressing at your stomach.",
        ]

        sensory = [
            "The smell of {scent} lingers on your sleeves, mingling with the itch of {fabric} against your skin.",
            "Each inhale tastes of {taste_detail}, while your fingers chase warmth through {layered_clothing}.",
            "You listen to {companion_sound}, your mind weaving comfort out of familiar cadence.",
            "Your toes curl against {floor}, instinctively searching for pockets of heat.",
            "Even in half-sleep you catalogue {tiny_detail}, because small observations promise a measure of control.",
        ]

        reflection = [
            "You wonder who first decided that {quirky_tidbit} might stave off the cold, and whether they slept easier for trying.",
            "Part of you wishes for solitude, but another part clings to the knowledge that {community_truth}.",
            "You weigh the ache of {bodily_discomfort} against the fragile reassurance of {shared_experience}.",
            "Imagination paints {mythic_fear} beyond the palisade, and still you fight to keep your breathing steady.",
            "The memory of {legacy_memory} gives you courage, a whispered promise that the night has been survived before.",
        ]

        action = [
            "Someone shifts beside you, tucking {comfort_item} closer while another hand reaches to bank the embers.",
            "You add kindling to the brazier, coaxing sparks into a flame that paints {structure} walls with hope.",
            "A lookout murmurs the hour, boots crunching over {floor_covering} as they pace the entrance.",
            "You pass a {warm_drink} around the circle, steam curling in the dim light like a protective charm.",
            "The group rearranges {makeshift_bedding}, layering it higher in defiance of the creeping chill.",
        ]

        return [descriptive, historical, sensory, reflection, action]

    def _build_transition_templates(self) -> Sequence[str]:
        return [
            "Hours stretch in a loop of vigilance and uneasy dreams, yet the rhythm becomes its own form of sanctuary.",
            "Outside, the winter keeps rewriting the same threat, but inside you trade stories to redraw the night.",
            "The cold does not bargain, so you and yours learn to bargain with one another instead.",
            "Between each watch rotation, quiet jokes and hushed prayers stitch the darkness together.",
            "Whenever exhaustion edges in, someone hums a tune carried from {ancestral_place}, anchoring everyone.",
        ]

    def _build_closing_templates(self) -> Sequence[str]:
        return [
            "Dawn may be distant, but resolve is nearer—you feel it in the shared breath around you.",
            "The embers survive another stirring, and so do you, tucked into the collective determination of the camp.",
            "Eventually the night will loosen its grip, and until then you hold the line with patience and ritual.",
            "When morning finally arrives, it will find you awake, alert, and carrying the stories of those who held the watch.",
            "Even as you drift toward sleep, you vow to remember every lesson the darkness offered tonight.",
        ]

    def generate(self) -> List[Section]:
        sections: List[Section] = []
        total_words = 0
        section_index = 1

        while total_words < self._target_words:
            title = next(self._section_titles)
            section_body = self._build_section_body(section_index)
            section_words = _word_count(section_body)
            sections.append(Section(title=title, body=section_body))
            total_words += section_words
            section_index += 1

        return sections

    def _build_section_body(self, index: int) -> str:
        paragraphs: List[str] = []
        current_words = 0
        target = self._section_target + self._random.randint(-120, 180)
        template_cycle = itertools.cycle(self._paragraph_templates)

        while current_words < target:
            template_group = next(template_cycle)
            paragraph = self._assemble_paragraph(template_group)
            paragraphs.append(paragraph)
            current_words += _word_count(paragraph)

            if current_words < target:
                transition = self._random.choice(self._transition_templates)
                transition_filled = transition.format(
                    ancestral_place=self._random.choice(self._ancestral_places())
                )
                paragraphs.append(transition_filled)
                current_words += _word_count(transition_filled)

        closing = self._random.choice(self._closing_templates)
        paragraphs.append(closing)
        return "\n\n".join(paragraphs)

    def _assemble_paragraph(self, template_group: Sequence[str]) -> str:
        sentences: List[str] = []
        for template in template_group:
            sentences.append(template.format(**self._fill_values()))
        return " ".join(sentences)

    def _fill_values(self) -> dict[str, str]:
        return {
            "shelter": self._random.choice(self._shelters()),
            "adjective": self._random.choice(
                ["brittle", "biting", "restless", "trembling", "watchful", "ghostly"]
            ),
            "air": self._random.choice(["air", "wind", "silence", "darkness"]),
            "structure": self._random.choice(self._structures()),
            "texture": self._random.choice(["packed", "splintered", "woven", "muddy", "frozen"]),
            "floor": self._random.choice(self._floors()),
            "scent": self._random.choice(self._scents()),
            "companion_sound": self._random.choice(self._companion_sounds()),
            "barrier": self._random.choice(["door", "hide curtain", "canvas", "palisade", "tent flap"]),
            "weather": self._random.choice(
                [
                    "needles of snow",
                    "unforgiving wind",
                    "hail tapping like drumbeats",
                    "frozen rain",
                    "wolves howling into the pines",
                ]
            ),
            "comfort_item": self._random.choice(self._comfort_items()),
            "pattern": self._random.choice(["spiderweb", "constellation", "runic", "feathered"]),
            "distant_noise": self._random.choice(self._distant_noises()),
            "historical_fact": self._random.choice(self._historical_facts()),
            "historical_event": self._random.choice(self._historical_events()),
            "debated_topic": self._random.choice(self._debated_topics()),
            "archival_memory": self._random.choice(self._archival_memories()),
            "logistical_issue": self._random.choice(self._logistical_issues()),
            "fabric": self._random.choice(self._fabrics()),
            "taste_detail": self._random.choice(self._taste_details()),
            "layered_clothing": self._random.choice(self._layered_clothing()),
            "tiny_detail": self._random.choice(self._tiny_details()),
            "quirky_tidbit": self._random.choice(self._quirky_tidbits()),
            "community_truth": self._random.choice(self._community_truths()),
            "bodily_discomfort": self._random.choice(self._bodily_discomforts()),
            "shared_experience": self._random.choice(self._shared_experiences()),
            "mythic_fear": self._random.choice(self._mythic_fears()),
            "legacy_memory": self._random.choice(self._legacy_memories()),
            "floor_covering": self._random.choice(self._floor_coverings()),
            "warm_drink": self._random.choice(self._warm_drinks()),
            "makeshift_bedding": self._random.choice(self._makeshift_bedding()),
        }

    # The following helper methods provide thematically tuned vocabularies.

    def _shelters(self) -> Sequence[str]:
        return [
            f"{self._theme} watch-post",
            "canvas pavilion",
            "snow-packed lean-to",
            "timber longhouse",
            "sunken earth lodge",
            "stone keep alcove",
        ]

    def _structures(self) -> Sequence[str]:
        return [
            "timber frame",
            "low tent",
            "makeshift palisade",
            "log wall",
            "wagon frame",
            "stone corridor",
        ]

    def _floors(self) -> Sequence[str]:
        return [
            "packed earth",
            "frozen moss",
            "woven mats",
            "trampled straw",
            "ice-rimmed planks",
        ]

    def _scents(self) -> Sequence[str]:
        return [
            "woodsmoke",
            "tallow",
            "wet wool",
            "iron and leather",
            "smoldering pine",
            "stew thick with herbs",
        ]

    def _companion_sounds(self) -> Sequence[str]:
        return [
            "sleep-roughened breathing",
            "whispers about distant patrols",
            "a child murmuring half-dreams",
            "armor settling against shields",
            "a lullaby hummed through chattering teeth",
            "sparks snapping in the coals",
        ]

    def _comfort_items(self) -> Sequence[str]:
        return [
            "a patchwork quilt",
            "a rabbit-fur lining",
            "a heavy cloak",
            "a shared pile of cloaks",
            "a wax-sealed lantern",
            "a braided talisman",
        ]

    def _distant_noises(self) -> Sequence[str]:
        return [
            "wolves pacing the tree line",
            "ice shifting on the river",
            "sentinels crunching through snow",
            "banners flicking against poles",
            "horses stamping frost from their hooves",
        ]

    def _historical_facts(self) -> Sequence[str]:
        return [
            "families often rationed warmth through shared watch rotations",
            "winter levies required soldiers to carry double rations of peat and pitch",
            "travelers slept in layers of untreated wool despite the itch",
            "guild records listed straw allocations beside bread and salt",
            "night watches paired veterans with apprentices to pass along survival lore",
        ]

    def _historical_events(self) -> Sequence[str]:
        return [
            "entire villages migrated to communal halls during blizzards",
            "armies built brushwood revetments to deflect the wind",
            "monasteries opened guest spaces for wandering families",
            "city guards rotated cloaks to keep them dry",
            "supply caravans stalled for weeks at frozen fords",
        ]

    def _debated_topics(self) -> Sequence[str]:
        return [
            "embers alone could warm an uninsulated hut",
            "soldiers carried portable braziers into their tents",
            "fur-lined hoods were common among peasants",
            "shared sleeping platforms prevented frostbite",
            "salted meats or root stews offered better night fuel",
        ]

    def _archival_memories(self) -> Sequence[str]:
        return [
            "a shepherd scribbling weather runes in the margins",
            "a knight praising his squire's patience with the coals",
            "a healer noting whose hands shook during the third watch",
            "a merchant mourning lost candles on a snowbound road",
            "an elder sketching sleeping positions beside herbal recipes",
        ]

    def _logistical_issues(self) -> Sequence[str]:
        return [
            "shortages of dry tinder",
            "frozen wells delaying breakfast",
            "the cost of imported furs",
            "ration cards torn by damp fingers",
            "the weight of ice on canvas roofs",
        ]

    def _fabrics(self) -> Sequence[str]:
        return [
            "felted wool",
            "linen patched with fur",
            "oilcloth",
            "doeskin",
            "roughspun cloaks",
            "quilted gambesons",
        ]

    def _taste_details(self) -> Sequence[str]:
        return [
            "smoky broth",
            "juniper-laced tea",
            "honeyed oat mash",
            "salted marrow",
            "roasted chestnuts",
            "mulled cider",
        ]

    def _layered_clothing(self) -> Sequence[str]:
        return [
            "layered tunics and hose",
            "fur-lined caps and scarves",
            "woolen wraps bound with leather cords",
            "patched cloaks over quilted armor",
            "mittens tucked beneath gauntlets",
        ]

    def _tiny_details(self) -> Sequence[str]:
        return [
            "ice crystals forming along the beam",
            "a forgotten prayer charm near the fire",
            "socks steaming gently beside the coals",
            "a child's carved toy resting atop a saddle",
            "spoon handles warmed beneath a cloak",
        ]

    def _quirky_tidbits(self) -> Sequence[str]:
        return [
            "rubbing goose fat on cheeks",
            "tucking heated stones into boots",
            "layering straw between tunic and cloak",
            "humming marching songs backward for luck",
            "sharing a single iron pot as a foot warmer",
        ]

    def _community_truths(self) -> Sequence[str]:
        return [
            "no one survives a winter night alone",
            "shared breath means shared strength",
            "warmth multiplies when stories are traded",
            "solidarity is the only true insulation",
            "every heartbeat counts double when kept in rhythm",
        ]

    def _bodily_discomforts(self) -> Sequence[str]:
        return [
            "numb fingers",
            "aching knees",
            "stiff shoulders",
            "cramps from crouching",
            "a chill that burrows between shoulder blades",
        ]

    def _shared_experiences(self) -> Sequence[str]:
        return [
            "collective watchfulness",
            "the weight of three blankets",
            "unspoken prayers to the same guardian",
            "passing cups of broth in the dark",
            "breathing in unison to chase away fear",
        ]

    def _mythic_fears(self) -> Sequence[str]:
        return [
            "white-cloaked spirits",
            "hungry wolves with ember eyes",
            "raiders moving like ghosts",
            "the old frost witch sung about in lullabies",
            "horned silhouettes stalking the treeline",
        ]

    def _legacy_memories(self) -> Sequence[str]:
        return [
            "your grandmother teaching you to stitch quilts",
            "your father mapping the constellations of icicles",
            "your mentor counting breaths between gusts",
            "stories of caravans that survived black ice",
            "lessons whispered during the longest siege",
        ]

    def _floor_coverings(self) -> Sequence[str]:
        return [
            "layered rushes",
            "pine boughs",
            "old tapestries",
            "discarded cloaks",
            "coiled ropes",
        ]

    def _warm_drinks(self) -> Sequence[str]:
        return [
            "herbed broth",
            "spiced ale",
            "birch bark tea",
            "roasted barley drink",
            "thick oat porridge",
        ]

    def _makeshift_bedding(self) -> Sequence[str]:
        return [
            "rolled cloaks",
            "layered shields",
            "straw pallets",
            "bundled sailcloth",
            "stacked furs",
        ]

    def _ancestral_places(self) -> Sequence[str]:
        return [
            "the frost-bitten coast",
            "pine-shadowed valleys",
            "salt marsh watch posts",
            "mountain passes",
            "canals frozen into glass",
        ]


# ---------------------------------------------------------------------------
# Prompt generation
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Pipeline and CLI
# ---------------------------------------------------------------------------


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
    """Run the full content generation pipeline and return the payload."""

    idea_generator = VideoIdeaGenerator(VideoIdeaGenerator.default_config(theme), seed=seed)
    ideas = idea_generator.generate(ideas_count)

    target_words = max(1000, int(script_words * 0.05)) if preview else script_words
    script_gen = ScriptGenerator(theme, target_word_count=target_words, seed=seed)
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

    thumbnail_gen = ThumbnailPromptGenerator(ThumbnailPromptConfig(theme=theme, title=title))
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
        description="Generate medieval-themed video ideas, scripts, and image prompts from a single file.",
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
        help="Generate a short preview script (5% of requested words) for quick inspection.",
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
