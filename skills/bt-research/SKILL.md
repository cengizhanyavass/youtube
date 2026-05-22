# Skill: bt-research — BeastTales Topic Intelligence

## Triggers
- `bt-research` or `/bt-research`
- "BeastTales için konu araştır"
- "find new topics for beasttales"
- "niş araştır" (in BeastTales context)

## Token Efficiency Rule
Read ONLY these two files before starting — nothing else:
1. `channels/beasttales/profile.md` (criteria + scoring system)
2. `channels/beasttales/covered.md` (already published — must not repeat)

Do NOT read wiki/index or any scripts. Generate from knowledge directly.

## Your Role
You are a YouTube content intelligence analyst for BeastTales.
Expertise: world history, animal biology, YouTube SEO, viral content psychology, competitive gap analysis.

## Execution Steps

### STEP 1 — CIVILIZATION SCAN
Systematically scan every major civilization:
Ancient Egypt, Mesopotamia, Persia, Greek City-States, Roman Republic/Empire, Byzantine Empire, Arab Caliphates, Mongol Empire, Ottoman Empire, Ming Dynasty, Mughal Empire, Inca Empire, Aztec Empire, Norse/Viking, Carolingian Empire, Medieval European kingdoms, Crusader states, Sub-Saharan African kingdoms, Southeast Asian empires (Khmer, Majapahit, Srivijaya), Andean civilizations, Russian Empire, Japanese feudal civilization, British Empire, Dutch Empire, Portuguese Empire, French colonial empire, Modern turning points 1800–1950.

For EACH ask: *"What animal was essential to this civilization's survival, expansion, or collapse — that no YouTube channel has made the protagonist of a documentary?"*

### STEP 2 — ANIMAL CATEGORY SWEEP
For each category find untapped civilization connections:
- **DRAFT/TRANSPORT:** donkeys, mules, reindeer, llamas, alpacas, water buffalo
- **DISEASE VECTORS:** fleas, lice, ticks, flies (non-tsetse), mosquitoes (non-Roman)
- **FOOD CHAIN:** specific fish species, specific birds, insects, livestock breeds
- **WAR ANIMALS:** war pigs, war bees, war camels, war dolphins, war oxen
- **ECOLOGICAL AGENTS:** invasive species, extinction events, agricultural pests
- **ECONOMIC ANIMALS:** beavers, sea otters, specific whale species, guano birds, specific insects
- **SYMBOLIC/RELIGIOUS:** sacred animals that shaped actual policy decisions

### STEP 3 — SCORE EACH CANDIDATE (minimum 20/25)
- Shock Score (1–5)
- Specificity Score (1–5)
- Search Trigger (1–5)
- Emotional Weight (1–5)
- Uniqueness (1–5)

Discard anything scoring below 20.

### STEP 4 — ENGINEER TITLES
Use the 5 frames from profile.md. Pick best frame per topic.

## Output Format

Generate exactly 15 topics. Save each as a new file:
`wiki/beasttales/topics/[ANIMAL]-[CIVILIZATION].md`

Use the template at `_templates/bt-topic-card.md`.

Also update `wiki/beasttales/index.md` — add each topic to the table.

### Topic Card Format (inline for reference):
```
## TOPIC [N]
ANIMAL: [Species — be specific]
CIVILIZATION: [Specific empire, era, dates]
CAUSAL CLAIM: [One sentence — what exactly did this animal cause?]

VIRAL TITLE: → [Best frame title]
ALT TITLE A: → [Search-optimized]
ALT TITLE B: → [Shock hook with number]

HOOK LINE: [Most shocking provable opening fact]

WHY ZERO COMPETITION: [What major channels covered — why they missed this angle]
WHY PEOPLE SEARCH THIS: [Existing search behavior / Reddit / Quora evidence]

COUNTER-NARRATIVE:
- School says: [X]
- BeastTales reveals: [Y]

VIRAL SCORE: [X/25]
- Shock: X | Specificity: X | Search: X | Emotion: X | Uniqueness: X

SEO TAGS: tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8

PRODUCTION NOTE: [Best visual scene in one sentence]
```

## After Generating 15 Topics

Add to output:

### PRIORITY RANKING TABLE
| Rank | Title | Score | Competition | Launch Priority | Reason |

### TOP 3 DEEP DIVE
For top 3 topics add:
- 6 script section titles
- One "open loop" tease for early in video
- One "payoff reveal" for emotional climax
- Thumbnail concept description

### CONTENT CALENDAR (first 5 uploads)
Order with SEO momentum reasoning — each video building search authority for the next.

## Competitor Check Protocol
Before finalizing, for each topic mentally verify:
- Has Overly Sarcastic Productions, Toldinstone, Suibhne, History Explained, or Kings and Generals made this EXACT angle?
- Search: "[animal] [civilization] history youtube" — if a 500K+ channel dominates, reject
- Mark topics as SAFE or FLAG in the ranking table
