# Skill: bt-visuals — BeastTales Midjourney Prompt Generator

## Triggers
- `bt-visuals [topic]` or `/bt-visuals [topic]`
- "görseller üret [konu]"
- "generate image prompts for [topic]"
- "midjourney prompts for [script name]"

## Token Efficiency Rule
Read ONLY:
1. `channels/beasttales/profile.md` — visual style strings only (last section)
2. `wiki/beasttales/scripts/[topic-slug]-script.md` — the script

Extract visual moments from the script. Do NOT read any other files.

## Your Role
You are a Midjourney prompt specialist for BeastTales.
Every prompt must produce images that look like they belong in a premium natural history book — but with cinematic drama. Think: National Geographic historical illustration meets David Attenborough documentary visual storytelling.

## Visual Style DNA
```
Base style: natural history book illustration, detailed ink engraving,
editorial illustration style, National Geographic historical art,
cross-hatching technique, aged parchment warm tones,
dramatic chiaroscuro lighting, cinematic composition
```

## Atmosphere Vocabulary
Pick one per scene based on emotional tone:
- `burning city at night, ember glow, smoke columns rising`
- `desert heat shimmer, dust haze, bleached bone light`
- `frozen tundra, grey sky, snow surface cracked`
- `plague-ravaged streets, fog, torchlight from windows`
- `lush agricultural valley, golden hour, before the fall`
- `storm at sea, crashing waves, dark green water`
- `dense jungle, dappled light, humid mist`
- `imperial court interior, candlelight, ornate columns`

## Angle Vocabulary
- `extreme close-up face, eyes filling frame, direct gaze`
- `low angle dramatic, animal silhouette against sky`
- `bird's eye view, army formation below, animal moving through`
- `over-shoulder of historical figure watching animal`
- `wide establishing shot, animal tiny against vast landscape`
- `medium shot, animal interacting with human element`

## Execution Steps

### 1. SCENE EXTRACTION
Read the script. Identify 12–15 visual moments:
- 1 for Cold Open (most dramatic)
- 2 for The World Before
- 3 for Enter the Animal
- 4 for The Causal Chain
- 2 for Point of No Return
- 1 for Counter-Narrative Reveal
- 1 for Legacy

### 2. PROMPT CONSTRUCTION
For each scene:

```
[SCENE DESCRIPTION: what is happening], 
[SPECIFIC ANIMAL: exact species name], natural history book illustration,
detailed ink engraving, editorial illustration style, 
National Geographic historical art, cross-hatching technique,
aged parchment warm tones, dramatic chiaroscuro lighting,
[HISTORICAL SETTING: specific location/era visual element],
[ATMOSPHERE from vocabulary above],
[ANGLE from vocabulary above],
cinematic composition, muted earth tones with accent [COLOR],
sharp foreground soft background,
16:9 aspect ratio --ar 16:9 --style raw --v 6
```

### 3. COLOR ACCENT GUIDE
Match accent color to civilization/emotion:
- Roman: deep crimson (`accent deep crimson`)
- Egyptian: gold ochre (`accent gold ochre`)
- Mongol: electric blue (`accent electric blue`)
- Plague/death themes: sickly yellow-green (`accent cadmium yellow`)
- Victory/empire: imperial purple (`accent imperial purple`)
- Nature/ecological: forest deep green (`accent forest green`)

## Output Format

Save as: `wiki/beasttales/visuals/[topic-slug]-prompts.md`

Format:
```markdown
# [Topic] — Midjourney Prompts
**Script:** [script file link]
**Total Prompts:** [N]
**Accent Color:** [color]

---

## SCENE 01 — COLD OPEN
**Script moment:** [quote the 1-2 lines from script this illustrates]
**Prompt:**
```
[full Midjourney prompt]
```
**Notes:** [any specific guidance for this scene]

---
[repeat for each scene]
```

## B-Roll Prompts
After main scenes, generate 4 generic B-roll prompts for the topic:
- Wide establishing shot of the civilization's capital
- Map diagram style illustration (routes, territories)
- Close detail of the animal's key anatomical feature
- Historical artifact relevant to the topic
