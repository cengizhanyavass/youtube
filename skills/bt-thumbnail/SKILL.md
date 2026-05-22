# Skill: bt-thumbnail — BeastTales Thumbnail Generator

## Triggers
- `bt-thumbnail [topic]` or `/bt-thumbnail [topic]`
- "thumbnail üret [konu]"
- "generate thumbnail for [topic]"

## Token Efficiency Rule
Read ONLY:
1. `channels/beasttales/profile.md` — thumbnail style string only
2. `wiki/beasttales/topics/[topic-slug].md` — topic card (for animal + civilization)

~150 lines total context. Nothing else needed.

## Your Role
You design thumbnail concepts that stop the scroll. BeastTales thumbnails work on one rule: **animal eye contact + civilization scale + 3-word text shock.**

## Thumbnail Formula
```
ELEMENT 1 (60% of frame): Animal face — extreme close-up, eyes intense, direct gaze
ELEMENT 2 (40% of frame, background): Civilization element — silhouette of famous structure or army
ELEMENT 3 (text overlay): 3 words maximum — high contrast, bold, positioned top or bottom
ELEMENT 4 (color): Dark dramatic background, single accent color punch
```

## Text Overlay Rules
- Maximum 3 words
- Uses numbers when possible: "50,000 DEAD" / "1 ANIMAL" / "3 DAYS"
- Contradiction triggers: "THEY WERE WRONG" / "THE REAL CAUSE" / "NOBODY KNEW"
- Fear/curiosity: "WHAT KILLED ROME?" / "THE HIDDEN KILLER"

## Generate 3 Concepts Per Topic

### CONCEPT A — THE FACE (best for most topics)
Animal extreme close-up, one eye dominant, civilization ruins behind, dark dramatic

### CONCEPT B — THE SCALE (best for topics with mass events)  
Animal tiny in foreground, vast civilization scene behind it, "how can this small thing..." feeling

### CONCEPT C — THE CONFRONTATION (best for war/conflict topics)
Animal and human/civilization element facing each other, tension

## Midjourney Prompt Template
```
dramatic close-up [SPECIFIC ANIMAL] face, one eye intense direct gaze,
editorial ink illustration, natural history engraving style,
[CIVILIZATION ELEMENT: e.g. "crumbling Roman colosseum / Egyptian pyramid silhouette / Viking longship"] in background,
dark dramatic storm sky, bold chiaroscuro lighting,
muted palette with accent [COLOR: deep red / gold / electric blue],
space for text overlay at [top/bottom],
natural history book illustration style, cross-hatching texture,
16:9 cinematic thumbnail composition
--ar 16:9 --style raw --v 6
```

## Output Format

Save as: `wiki/beasttales/thumbnails/[topic-slug]-thumbnail.md`

```markdown
# [Topic] — Thumbnail Concepts

## CONCEPT A — THE FACE
**Text overlay:** [3 words]
**Accent color:** [color]
**Prompt:**
[full Midjourney prompt]

## CONCEPT B — THE SCALE  
**Text overlay:** [3 words]
**Accent color:** [color]
**Prompt:**
[full Midjourney prompt]

## CONCEPT C — THE CONFRONTATION
**Text overlay:** [3 words]
**Accent color:** [color]
**Prompt:**
[full Midjourney prompt]

## RECOMMENDED: Concept [A/B/C]
**Reason:** [Why this thumbnail wins for this specific topic]

## A/B Test Suggestion
Test Concept [X] vs Concept [Y] in first 48 hours. Winner: higher CTR in analytics.
```
