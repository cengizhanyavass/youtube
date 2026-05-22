# Command: /bt-produce

Full production pipeline for one BeastTales video.
Runs script + visuals + thumbnail in sequence.

## What Happens
1. Reads `channels/beasttales/profile.md`
2. Reads topic card: `wiki/beasttales/topics/[topic].md`
3. Writes full script → saves to `wiki/beasttales/scripts/`
4. Generates 12–15 Midjourney image prompts → saves to `wiki/beasttales/visuals/`
5. Generates 3 thumbnail concepts → saves to `wiki/beasttales/thumbnails/`
6. Outputs complete Production Brief (all in one place)

## Usage
```
/bt-produce beaver-russian-empire
/bt-produce [animal]-[civilization-slug]
```

## Token Efficiency
Only 3 files are read:
- `channels/beasttales/profile.md` (~80 lines)
- `channels/beasttales/covered.md` (~30 lines)
- `wiki/beasttales/topics/[topic].md` (~40 lines)

Total context loaded: ~150 lines. All generation is done from these 3 files + model knowledge.

## Complete Production Brief Output

After running, you receive:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEASTTALES PRODUCTION BRIEF: [TOPIC]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📹 TITLE: [Best viral title]
🏷️ TAGS: [8 tags]
📝 DESCRIPTION HOOK: [First 2 lines]

🎬 SCRIPT: → wiki/beasttales/scripts/[slug]-script.md
🖼️ VISUALS: → wiki/beasttales/visuals/[slug]-prompts.md  
🎨 THUMBNAIL: → wiki/beasttales/thumbnails/[slug]-thumbnail.md

⚡ HOOK LINE: [First sentence of video]
🔄 COUNTER-NARRATIVE: [One-line reveal]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Workflow Overview
```
/bt-research          ← Find 15 new topics
       ↓
/bt-produce [topic]   ← Full production for one topic
       ↓
Upload → Update covered.md
       ↓
/bt-research          ← Next batch (never repeats covered)
```
