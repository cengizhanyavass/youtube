# Command: /bt-research

Trigger this command to find 15 new video topics for BeastTales.

## What Happens
1. Claude reads `channels/beasttales/profile.md` and `channels/beasttales/covered.md`
2. Runs full civilization scan + animal category sweep
3. Scores every candidate (minimum 20/25)
4. Generates 15 topic cards → saves to `wiki/beasttales/topics/`
5. Updates `wiki/beasttales/index.md`
6. Produces Priority Ranking Table + Top 3 Deep Dive + Content Calendar

## Usage
```
/bt-research
```

Or with focus:
```
/bt-research focus: Southeast Asia
/bt-research focus: disease vectors
/bt-research focus: economic animals
```

## Output Location
- Individual topic cards: `wiki/beasttales/topics/[animal]-[civ].md`
- Research summary: `wiki/beasttales/index.md` (updated)

## After This Command
Pick the #1 topic from the ranking table, then run:
```
/bt-script [topic-name]
```
