---
name: divinci-council
description: |
  Run the Divinci Content Council: a multi-persona content generation pipeline that transforms
  blog posts into tweets, LinkedIn posts, and VEO3.1 video scripts using 8 synthetic council
  members (Leonardo, Atlantean Archivist, Gemma4, Growth Hacker, Thought Leader, VEO Director,
  Sir Spamalot, Brand Guardian). Includes show bible integration for "The Release Cycle" and
  project-agnostic config for reuse across brands.
triggers:
  - "divinci content council"
  - "run the council"
  - "generate social content from blog posts"
  - "council batch processing"
  - "veo scripts from articles"
  - "spamalot parody content"
  - "the release cycle show"
  - "content council skill"
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, content-marketing, multi-agent, persona-pipeline, show-bible]
    related_skills: [content-council, subagent-driven-development, claude-design, xurl]
---

# Divinci Council

## When to Use

- You need to batch-process blog posts or long-form content into platform-native social assets
- You want persona-driven content with a specific brand voice (Leonardo/Atlantean/etc.)
- You need parody content (Sir Spamalot) alongside serious marketing copy
- You're working on "The Release Cycle" show and need diegetic content that maps to real council output
- You want a reusable, configurable content pipeline for any brand (not just Divinci)

## When NOT to Use

- One-off tweets (use `xurl` instead)
- Serious video production without the parody/satire layer
- Content that doesn't allow any humor or brand personality
- Projects where "Leonardo meets crystal energy" would be off-brand

## Overview

The Divinci Council is a **multi-persona content generation pipeline** with two layers:

1. **Content Machine** — Transforms blog posts into tweets, LinkedIn posts, and VEO3.1 scripts via 8 synthetic council members
2. **Show Integration** — Every output becomes canonical content in "The Release Cycle" workplace mockumentary (optional)

The pipeline runs via an orchestrator script that can use Ollama (local), OpenCode CLI, or any model router. Personas, brand rules, and show connections are configured through a `council.yaml` file per project.

## The Eight Council Members

| # | Persona | Voice | Specialty | Output |
|---|---------|-------|-----------|--------|
| 1 | **Leonardo** | Renaissance polymath sketching in margins | Conceptual hooks, nature analogies | 5 tweets |
| 2 | **Atlantean Archivist** | Crystal-memory keeper, speaks in harmonics | Poetic-prophetic layer, φ motifs | 5 tweets |
| 3 | **Gemma4** | Earnest open-weights junior engineer | Open-source perspective, wildcard takes | 5 tweets |
| 4 | **Viral Growth Hacker** | Metric-obsessed X-native | Contrarian data drops, hot takes | 5 tweets |
| 5 | **LinkedIn Thought Leader** | Contrarian-but-helpful executive | Long-form authority, frameworks | 2 LinkedIn posts |
| 6 | **VEO3.1 Director** | Thinks in shots, beats, visual gags | Timestamped video scripts | 2 VEO scripts |
| 7 | **Sir Spamalot** | Monty Python + insurance ad parody genius | Absurdist parody tweets and VEO scripts | 2 parody tweets + 1 parody VEO |
| 8 | **Brand Guardian** | Sober final check, veto power | Synthesis, rule enforcement, rating | 1 reviewed bundle |

**New in v2.0:** All personas are model-agnostic. You route each to any backend via `council.yaml`.

## Quick Start

### 1. Create a project config

```bash
cp ~/.hermes/skills/creative/divinci-council/templates/council.yaml ./council.yaml
```

Edit `council.yaml`:

```yaml
project_name: "My Startup"
source_domain: "https://example.com/blog"

models:
  ollama_local:
    type: ollama
    url: http://localhost:11434/api/generate
    model: gemma4:latest
    timeout: 300
    options:
      temperature: 0.8
      num_predict: 4096
  opencode_cloud:
    type: opencode
    model: opencode/deepseek-v4-flash
  hermes_native:
    type: hermes

personas:
  leonardo: {model: ollama_local, temperature: 0.9}
  archivist: {model: hermes_native}
  gemma4: {model: ollama_local}
  growthhacker: {model: opencode_cloud}
  thoughtleader: {model: opencode_cloud}
  veodirector: {model: hermes_native}
  sirspamalot: {model: ollama_local, temperature: 1.0}
  brand_guardian: {model: hermes_native}

content_quota:
  tweets: 7
  linkedin_posts: 2
  veo_scripts: 3

brand:
  forbidden_words: ["revolutionary", "game-changing", "disruptive", "synergy"]
  required_motifs: ["golden spiral", "crystal lattice", "solar abundance"]
  phrases: ["Excellence, every time", "The Age of AI Management"]
  character_desc: "Young Leonardo da Vinci sketching robots at a cleanroom bench"
  visual_identity: "Dark theme with gold accents, phi = 1.618"
  target_audience: "Technical AI engineers"
  tone: "Craftsmanship, mastery, technical depth without hype"

show_integration:
  enabled: true
  show_title: "The Release Cycle"
  faction: "Content Council / Ad Cult"
  character_mapping:
    leonardo: "Trevor"
    archivist: "Trevor (channeling)"
    gemma4: "The Laptop"
    growthhacker: "Priya"
    thoughtleader: "Trevor"
    veodirector: "Dana (in visor mode)"
    sirspamalot: "Margaret"
    brand_guardian: "Jordan"

output:
  articles_dir: ./articles
  tweets_dir: ./tweets
  linkedin_dir: ./linkedin
  veo_dir: ./veo
  bundles_dir: ./output
```

### 2. Set up your source catalog

Create `catalog.json`:

```json
[
  {
    "batch_id": "001",
    "title": "How to Diagnose Custom LLM QA Failures in 7 Steps",
    "url": "https://divinci.ai/blog/how-to-diagnose-custom-llm-qa-failures-in-7-steps/",
    "category": "Product",
    "date": "May 29, 2026"
  }
]
```

### 3. Run the council

```bash
# Process all batches
python3 ~/.hermes/skills/creative/divinci-council/scripts/orchestrator.py

# Single batch
python3 ~/.hermes/skills/creative/divinci-council/scripts/orchestrator.py --batch 001

# Dry run
python3 ~/.hermes/skills/creative/divinci-council/scripts/orchestrator.py --dry-run

# With deliberation (peer review round)
python3 ~/.hermes/skills/creative/divinci-council/scripts/orchestrator.py --deliberate
```

### 4. Integrate with "The Release Cycle" (optional)

If `show_integration.enabled: true`, the orchestrator also generates `show_notes/` with:
- Character dialogue for Content Council meeting scenes
- Parody script table-read versions
- Whiteboard content (batch tracker snapshots)
- Diegetic social media posts (the actual tweets as if posted by characters)

See `references/show-integration.md` for full mapping.

## Content Quota (v2.0)

Per source article:

| Asset Type | Count | Personas |
|---|---|---|
| **Tweets** | 7+ | Leonardo (5), Archivist (5), Gemma4 (5), Growth Hacker (5), Sir Spamalot (2) |
| **LinkedIn posts** | 2 | Thought Leader (long + short) |
| **VEO scripts** | 3 | Director (2), Sir Spamalot parody (1) |
| **Parody variants** | 3+ | Sir Spamalot (tweets + VEO + any) |

## Parody & Comedy (Sir Spamalot)

**Not optional.** Sir Spamalot has consistently produced the highest-rated content (5.0/5 Brand Guardian scores) across 9 production batches.

### Proven Formats

| Format | Example | Notes |
|---|---|---|
| **State Farm parody** | "Like a good neighbor, Divinci is there... with your rollback" | Insurance ad optimism × 2:14 AM infrastructure |
| **Monty Python absurdist** | "And now for something completely different... RAG retrieval" | Technically accurate underneath |
| **Golden Girls sitcom** | "Thank you for being a friend... who configures eval pipelines" | Multi-generational appeal |
| **GEICO simplicity** | "So easy a caveman can do it — but cavemen don't use LLMs" | Self-aware limitation humor |

### Trademark Safety Rules
- No copyrighted logos
- No exact jingle melodies
- No brand names in final output
- Reference the *style* ("red-shirt/khakis energy") not the trademark
- Transformative use: the humor comes from the juxtaposition, not the brand itself

## Deliberation Layer (Peer Review)

Add `--deliberate` to enable a cross-persona review round before synthesis:

```
Source → Drafting → Peer Review → Revision → Brand Guardian → Bundle
```

### Reviewer Mapping

| Reviewer | Lens | Reviews |
|---|---|---|
| Brand Guardian | Brand rules, trademark safety | All (especially Sir Spamalot) |
| Growth Hacker | "What's missing? Will this fail?" | Thought Leader, Leonardo, Archivist |
| Leonardo | "Strip assumptions. Does this hold up?" | Growth Hacker, Gemma4, Director |

### Prompt Template for Reviewers

```
You are [PERSONA]. Review these drafts from other council members.

SOURCE ARTICLE: [title]
YOUR LENS: [critical lens]

DRAFTS TO REVIEW:
[outputs]

Critique on: accuracy, hook strength, brand alignment, factual correctness.
Quote exact lines you're critiquing. Rate each draft 1-5.
```

### Revision Round

Feed critiques back to original authors:

```
Here is feedback on your draft. Revise to address the strongest critiques
while keeping your voice. You may reject a critique if you defend why.
```

## Output Bundle Schema (v2.0)

```json
{
  "source_post": {
    "url": "...",
    "title": "...",
    "category": "...",
    "date": "...",
    "author": "...",
    "word_count": 1200
  },
  "council_run": {
    "run_id": "2026-06-01T12-00-00Z",
    "council_version": "2.0",
    "deliberation": false,
    "models_used": ["gemma4:latest", "hermes", "opencode/deepseek-v4-flash"],
    "members": ["Leonardo", "Atlantean Archivist", "Gemma4", "Viral Growth Hacker", "LinkedIn Thought Leader", "VEO3.1 Director", "Sir Spamalot", "Brand Guardian"]
  },
  "tweets": [
    {
      "variant": "primary",
      "type": "technical_hook",
      "persona": "Leonardo",
      "text": "...",
      "char_count": 243,
      "rating": 4.8,
      "council_note": "Brand Guardian: Approved. Strong analogy."
    }
  ],
  "linkedin_posts": [
    {
      "variant": "primary",
      "type": "long_form",
      "persona": "ThoughtLeader",
      "text": "...",
      "rating": 4.5
    }
  ],
  "veo_scripts": [
    {
      "variant": "primary",
      "title": "...",
      "persona": "VEODirector",
      "duration_sec": 14.5,
      "style": "atmospheric_tension",
      "script": "[00:00.0 - 00:02.5] VISUAL: ... BEAT: ...",
      "rating": 4.7
    },
    {
      "variant": "parody",
      "title": "...",
      "persona": "SirSpamalot",
      "duration_sec": 13.0,
      "style": "state_farm_parody",
      "parody_target": "State Farm insurance commercials",
      "script": "[00:00.0 - 00:03.0] VISUAL: Teal-blue office...",
      "rating": 5.0,
      "council_note": "Brand Guardian: Approved. Transformative use."
    }
  ],
  "brand_guardian_review": {
    "verdict": "APPROVED",
    "forbidden_words_found": 0,
    "motifs_present": ["golden spiral", "crystal lattice"],
    "best_tweet": "...",
    "best_linkedin": "...",
    "best_veo": "...",
    "review_text": "..."
  },
  "show_integration": {
    "scene_drafts": [
      {
        "scene_type": "content_council_meeting",
        "characters": ["Trevor", "Priya", "Jordan", "Margaret"],
        "dialogue": "...",
        "whiteboard_content": "..."
      }
    ],
    "diegetic_posts": {
      "tweets_published": ["..."],
      "linkedin_published": "..."
    }
  }
}
```

## Show Integration

"The Release Cycle" treats every council output as diegetic content. When enabled, the orchestrator generates additional `show_notes/` output:

### Scene Drafts
Fictionalized versions of the council meeting that produced this batch:
- Trevor (as Leonardo) sketching ad concepts in brown ink
- Priya presenting engagement spreadsheets
- Jordan brandishing the forbidden words list
- Margaret (as Sir Spamalot) in cape pitching parody
- Gemma4 (the laptop) formally "consulted"

### Diegetic Social Media
The actual approved content, as if posted by the characters:
- Trevor's Leonardo tweets from @DivinciAI account
- Priya's engagement-optimized hot takes
- The parody videos that "accidentally" went viral

### Content Council Meetings as Ritual
The show treats council sessions like séances or D&D campaigns:
- Name tags with persona names
- Gemma4 laptop positioned as an equal member
- Jordan's forbidden words list as sacred text
- Margaret's gradual slide into Sir Spamalot as mental health metaphor

See `references/show-integration.md` for:
- Full character mapping (show character ↔ council persona)
- Episode-by-episode content placement
- Meta-content map (how each output type appears on screen)
- Title sequence and visual identity notes

## Scaling Tips

1. **Parallel dispatch:** Run Independent Drafting via `delegate_task` with `tasks: [...]` for speed
2. **Local-first for bulk:** Use Ollama for unattended batch runs (zero API cost)
3. **Cloud for quality:** Route Brand Guardian and high-stakes personas through Hermes or opencode
4. **Hybrid for deliberation:** Generate drafts locally, run peer review and synthesis via cloud models
5. **Verify programmatically:** After every batch, run automated checks:
   - Character counts (tweets ≤ 280)
   - Forbidden word grep
   - Brand motif presence
   - URL status (200 OK)
6. **Track with BATCH_TRACKER.md:** See `references/batch-tracker-template.md`

## Model Routing

The orchestrator supports three backend types, configured in `council.yaml`:

### Ollama (local)
```yaml
type: ollama
url: http://localhost:11434/api/generate
model: gemma4:latest
```
Fast, zero cost, ideal for bulk runs. Best for: Leonardo, Archivist, Gemma4.

### Hermes (native)
```yaml
type: hermes
```
Uses the current Hermes session model. Best for: Brand Guardian (consistency checking), Archivist (creative reasoning), VEO Director (visual scripting).

### OpenCode CLI
```yaml
type: opencode
model: opencode/deepseek-v4-flash-free
```
Cloud inference via `opencode run`. Requires payment method for paid models. Free variant works. Best for: Growth Hacker (viral optimization), Thought Leader (structured reasoning).

**Note:** `opencode` v1.15.13 routes through `opencode.ai`. The free `deepseek-v4-flash-free` model works without payment. The paid variant requires billing setup.

## Directory Structure (per project)

```
my-council-project/
├── council.yaml              # Project config (copy from templates/)
├── catalog.json              # Source content catalog
├── brand-guide.md            # Brand voice (copy from templates/)
├── BATCH_TRACKER.md          # Living checklist
├── articles/                 # Scraped source articles
├── tweets/                   # Per-persona tweet drafts
├── linkedin/                 # Thought Leader posts
├── veo/                      # Video scripts
├── output/                   # Final JSON bundles
└── show_notes/              # Diegetic content for "The Release Cycle"
    ├── scenes/              # Meeting scene drafts
    ├── diegetic_posts/      # In-universe social media
    └── props/               # Whiteboard content, forbidden words list
```

## Common Pitfalls

1. **Stale URLs produce silent 404 bundles.** Always `curl -sI` URLs before adding to catalog. Check word count > 800 after scrape.

2. **Gemma4 hallucinates tool calls.** It may claim to execute scripts without actually doing so. Always verify with `ps aux` or file existence checks.

3. **Opencode requires billing for paid models.** Use `deepseek-v4-flash-free` for zero-cost runs. Paid models need payment method at `opencode.ai` workspace billing.

4. **Sir Spamalot can cross into trademark infringement.** Always run Brand Guardian review on parody content. Reference style, not trademarks.

5. **Deliberation adds 2-3x runtime.** On Ollama, peer review loops add ~1-2 min per persona. For bulk unattended runs, run deliberation only on priority batches.

6. **Ollama direct API > CLI wrappers.** Use `POST /api/generate` with JSON payload rather than `ollama run` for unattended scripts. No TTY needed, clean response parsing.

## Verification Checklist

- [ ] `council.yaml` has all 8 personas mapped to backends
- [ ] `catalog.json` URLs return 200 OK via `curl -sI`
- [ ] Ollama is running (`curl http://localhost:11434` returns 200)
- [ ] Target models are pulled (`ollama list` shows them)
- [ ] Brand guide specifies forbidden words, required motifs, target audience
- [ ] Show integration disabled unless intentionally producing diegetic content
- [ ] Output directories exist
- [ ] `--dry-run` passes without errors before full run
- [ ] First batch manually spot-checked for quality before unattended bulk run
- [ ] `BATCH_TRACKER.md` created and updated per batch

## References

- `references/divinci-protocol-v2.md` — Full persona definitions, brand voice, exact prompts
- `references/show-integration.md` — How council content maps to "The Release Cycle" show
- `references/show-bible-structure.md` — How to scaffold a TV series bible from council outputs
- `references/llm-council-research.md` — Survey of 3 peer-review architectures (Karpathy, MCP server, MultiMind-AI)
- `references/batch-tracker-template.md` — BATCH_TRACKER.md template
- `references/opencode-config-fix.md` — How to fix opencode CLI model routing (5-layer config fix)
- `templates/council.yaml` — Project configuration template
- `templates/brand-guide.md` — Brand voice template
- `scripts/orchestrator.py` — Core orchestrator (abstracted, model-agnostic)

## User Preferences

The user who created this pipeline prefers thorough, unhurried work on complex multi-step tasks. When asked to plan and execute:

1. **Plan first, execute iteratively.** Do not rush into generation. Lay out the structure, get alignment, then build.
2. **Document as you build.** Every significant output gets a file. Every decision gets a note.
3. **Package for reuse.** Scripts, configs, and templates should be portable to other projects without modification.
4. **Honor the persona voices.** The council members have specific, distinct voices. Do not flatten them into generic marketing copy.
5. **Parody is first-class content.** Sir Spamalot outputs are not optional extras — they are core deliverables that consistently outperform serious content.
6. **Show integration is canonical.** When working on "The Release Cycle," every piece of council output becomes diegetic content. Write it as if the characters will perform it.

## One-Shot Recipes

### Run Divinci's Full Pipeline

```bash
cd ~/Documents/server/scripts/content-council
python3 council_orchestrator_v3.py --deliberate
```

### Spin Up a New Brand Council

```bash
mkdir my-brand-council && cd my-brand-council
cp ~/.hermes/skills/creative/divinci-council/templates/council.yaml .
cp ~/.hermes/skills/creative/divinci-council/templates/brand-guide.md .
# Edit council.yaml and brand-guide.md
# Create catalog.json with your blog posts
python3 ~/.hermes/skills/creative/divinci-council/scripts/orchestrator.py --dry-run
```

### Generate Show Scene from a Bundle

```bash
python3 ~/.hermes/skills/creative/divinci-council/scripts/show_scene_generator.py \
  --bundle output/bundle-001.json \
  --scene-type council_meeting \
  --episode 3
```

### Run Council for "The Release Cycle" Episode

When writing an episode, extract the relevant batch and generate diegetic content:

```bash
python3 scripts/orchestrator.py --batch 003 --show-integration
# Produces:
# - output/bundle-003.json (real marketing content)
# - show_notes/scenes/ep03_council_meeting.md (diegetic scene)
# - show_notes/diegetic_posts/ep03_tweets.json (in-universe social)
```
