# YouTube Creator Second Brain — Claude + Obsidian Vault

This vault is a Claude Code plugin + Obsidian second brain for YouTube channel production.

**Primary Channel:** BeastTales (historical animal documentary)
**Plugin name:** `claude-obsidian` + BeastTales production system
**Vault path:** This directory (open in Obsidian directly)

---

## BeastTales Production System

### Channel Brain (read-only reference — always load before any BT task)
```
channels/beasttales/profile.md    ← Channel DNA, voice rules, visual style, criteria
channels/beasttales/covered.md    ← Published topics — NEVER repeat these
channels/beasttales/competitors.md ← Competitor tracking
```

### BeastTales Skills

| Command | What It Does | Files Read | Files Written |
|---------|-------------|------------|---------------|
| `/bt-research` | Find 15 new topics | profile + covered | wiki/beasttales/topics/ + index |
| `/bt-script [topic]` | Write full 13min script | profile + topic card | wiki/beasttales/scripts/ |
| `/bt-visuals [topic]` | Generate all Midjourney prompts | profile + script | wiki/beasttales/visuals/ |
| `/bt-thumbnail [topic]` | Generate 3 thumbnail concepts | profile + topic card | wiki/beasttales/thumbnails/ |
| `/bt-produce [topic]` | Full pipeline: script + visuals + thumbnail | profile + topic card | all 3 above |

### Token Efficiency Rule
Each BT skill reads a maximum of 3 files (~150 lines). Never load the full wiki for production tasks.

### Production Workflow
```
/bt-research              → get 15 scored topics
/bt-produce [topic-slug]  → full production package
Upload → update covered.md
/bt-research              → next batch (never repeats)
```

### BeastTales Wiki
```
wiki/beasttales/index.md      ← Topic bank (auto-updated by research)
wiki/beasttales/pipeline.md   ← Production tracker
wiki/beasttales/topics/       ← Individual topic cards
wiki/beasttales/scripts/      ← Full scripts
wiki/beasttales/visuals/      ← Midjourney prompt sets
wiki/beasttales/thumbnails/   ← Thumbnail concepts
```

### Tools Available
```
tools/claude-youtube/   ← Claude Code YouTube growth skill (channel audit, SEO, analytics)
tools/shortgpt/         ← AI framework for YouTube Shorts automation
tools/money-printer/    ← YouTube Shorts auto-generator (local AI, free)
tools/money-printer-v2/ ← Full YouTube automation suite with scheduling
```

---

## What This Vault Is For

This vault demonstrates the LLM Wiki pattern — a persistent, compounding knowledge base for Claude + Obsidian. Drop any source, ask any question, and the wiki grows richer with every session.

## Vault Structure

```
.raw/           source documents — immutable, Claude reads but never modifies
wiki/           Claude-generated knowledge base
_templates/     Obsidian Templater templates
_attachments/   images and PDFs referenced by wiki pages
```

## How to Use

Drop a source file into `.raw/`, then tell Claude: "ingest [filename]".

Ask any question. Claude reads the index first, then drills into relevant pages.

Run `/wiki` to scaffold a new vault or check setup status.

Run "lint the wiki" every 10-15 ingests to catch orphans and gaps.

## Cross-Project Access

To reference this wiki from another Claude Code project, add to that project's CLAUDE.md:

```markdown
## Wiki Knowledge Base
Path: /path/to/this/vault

When you need context not already in this project:
1. Read wiki/hot.md first (recent context, ~500 words)
2. If not enough, read wiki/index.md
3. If you need domain specifics, read wiki/<domain>/_index.md
4. Only then read individual wiki pages

Do NOT read the wiki for general coding questions or things already in this project.
```

## Plugin Skills

| Skill | Trigger |
|-------|---------|
| `/wiki` | Setup, scaffold, route to sub-skills |
| `ingest [source]` | Single or batch source ingestion |
| `query: [question]` | Answer from wiki content |
| `lint the wiki` | Health check |
| `/save` | File the current conversation as a structured wiki note |
| `/autoresearch [topic]` | Autonomous research loop: search, fetch, synthesize, file |
| `/canvas` | Visual layer: add images, PDFs, notes to Obsidian canvas |

## MCP (Optional)

If you configured the MCP server, Claude can read and write vault notes directly.
See `skills/wiki/references/mcp-setup.md` for setup instructions.
