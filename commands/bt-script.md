# Command: /bt-script

Trigger this command to write a full BeastTales script for a topic.

## What Happens
1. Claude reads `channels/beasttales/profile.md` (voice + structure)
2. Claude reads `wiki/beasttales/topics/[topic].md` (topic card)
3. Writes 12–14 min script (~1,900 words) in BeastTales voice
4. Saves to `wiki/beasttales/scripts/[topic]-script.md`
5. Includes metadata: title, description, tags, thumbnail text

## Usage
```
/bt-script beaver-russian-empire
/bt-script llama-inca-empire
/bt-script [animal]-[civilization-slug]
```

## Output Location
`wiki/beasttales/scripts/[topic-slug]-script.md`

## After This Command
```
/bt-visuals [topic-slug]    ← generate all Midjourney prompts
/bt-thumbnail [topic-slug]  ← generate thumbnail concepts
```
Or run both at once:
```
/bt-produce [topic-slug]
```
