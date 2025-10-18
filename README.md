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

## Quickstart

1. Install the package locally:
   ```bash
   pip install .
   ```
2. Verify the command-line entry point:
   ```bash
   medieval-generator --help
   ```
3. Run a preview generation (about 5% of the requested script length) to check tone and structure:
   ```bash
   medieval-generator "Frontier Winter Watch" \
     "How Frontier Winter Watches Kept the Night at Bay" \
     --preview \
     --ideas-count 15 \
     --image-prompts 20 \
     --output preview.json
   ```
4. Launch the full-length run once the preview looks right:
   ```bash
   medieval-generator "Frontier Winter Watch" \
     "How Frontier Winter Watches Kept the Night at Bay" \
     --script-words 35000 \
     --ideas-count 25 \
     --image-prompts 28 \
     --output payload.json
   ```

The generated JSON contains the video ideas, each script section with its word count, the total script length, image
prompts, and the final thumbnail prompt. See [`docs/USAGE_TR.md`](docs/USAGE_TR.md) for a detailed Turkish walk-through
that covers the same workflow step by step.
