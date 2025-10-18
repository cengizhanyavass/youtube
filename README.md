# Medieval Narrative Generator

This project produces long-form, medieval-inspired YouTube automation assets. It creates:

- Viral-ready video idea statements anchored to a chosen theme.
- Narrative scripts in the immersive, second-person tone showcased in the reference material. The default length is
  32,000 words, and output can be previewed at 5% scale for quick iteration.
- Scenic illustration prompts (20–30 by default) suitable for tools such as MidJourney or Stable Diffusion, using the
  requested illuminated manuscript aesthetic.
- A single thumbnail prompt that follows the provided art direction for exaggerated, comedic medieval scenes.

## Installation

```bash
pip install .
```

## Usage

Generate a full payload directly to standard output:

```bash
medieval-generator "Frontier Winter Watch" "How Frontier Winter Watches Kept the Night at Bay"
```

To create a quick preview (about 5% of the requested script words) and save it to a file:

```bash
medieval-generator "Frontier Winter Watch" \
  "How Frontier Winter Watches Kept the Night at Bay" \
  --preview \
  --ideas-count 15 \
  --image-prompts 20 \
  --output output.json
```

The generated JSON contains the video ideas, each script section with its word count, the total script length, image
prompts, and the final thumbnail prompt.
