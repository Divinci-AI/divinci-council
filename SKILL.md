---
name: divinci-council
description: |
  Run the Divinci Council: a multi-persona deliberation pipeline that oversees content creation,
  coding tasks, and continuous self-improvement. Uses 9 synthetic council members (Leonardo,
  Atlantean Archivist, Gemma4, Growth Hacker, Thought Leader, VEO Director, Sir Spamalot,
  Brand Guardian, The Cursor). Transforms blog posts into social assets, reviews code,
  architects systems, and reflects on its own methodology. Includes show bible integration
  for "The Release Cycle" and project-agnostic config for reuse across domains.
triggers:
  - "divinci council"
  - "run the council"
  - "generate social content from blog posts"
  - "council batch processing"
  - "veo scripts from articles"
  - "spamalot parody content"
  - "the release cycle show"
  - "council code review"
  - "council architecture review"
  - "council self reflection"
  - "council meta review"
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, content-marketing, multi-agent, persona-pipeline, show-bible, coding, architecture, self-reflection]
    related_skills: [content-council, subagent-driven-development, claude-design, xurl, claude-code, codex]
---

# Divinci Council

## When to Use

- You need to batch-process blog posts or long-form content into platform-native social assets
- You want persona-driven content with a specific brand voice (Leonardo/Atlantean/etc.)
- You need parody content (Sir Spamalot) alongside serious marketing copy
- You're working on "The Release Cycle" show and need diegetic content that maps to real council output
- You want a reusable, configurable content pipeline for any brand (not just Divinci)
- You need code review, refactoring recommendations, or architecture feedback on a codebase
- You want multi-persona deliberation on technical decisions (trade-off analysis, design review)
- You want the council to reflect on its own outputs and suggest improvements to its process
- You need a meta-review: the council evaluates its own skill, methodology, or repository

## When NOT to Use

- One-off tweets (use `xurl` instead)
- Serious video production without the parody/satire layer
- Content that doesn't allow any humor or brand personality
- Projects where "Leonardo meets crystal energy" would be off-brand
- Production-critical code deployment without human review (council advises, humans decide)
- Time-sensitive incident response (council deliberation takes time)

## Overview

The Divinci Council is a **multi-persona deliberation pipeline** with four layers:

1. **Content Machine** — Transforms blog posts into tweets, LinkedIn posts, and VEO3.1 scripts via 8 synthetic council members
2. **Code & Architecture Review** — Reviews code, proposes refactors, and deliberates on technical decisions via The Cursor and relevant personas
3. **Show Integration** — Every output becomes canonical content in "The Release Cycle" workplace mockumentary (optional)
4. **Self-Reflection** — The council periodically reviews its own methodology, outputs, and skill structure to suggest improvements

The pipeline runs via an orchestrator script that can use Ollama (local), OpenCode CLI, Cursor Agent CLI, or any model router. Personas, brand rules, coding contexts, and show connections are configured through a `council.yaml` file per project.

## The Nine Council Members

| # | Persona | Voice | Specialty | Output |
|---|---------|-------|-----------|--------|
| 1 | **Leonardo** | Renaissance polymath sketching in margins | Conceptual hooks, nature analogies, system architecture | 5 tweets / architectural insights |
| 2 | **Atlantean Archivist** | Crystal-memory keeper, speaks in harmonics | Poetic-prophetic layer, φ motifs, pattern recognition | 5 tweets / historical analogies |
| 3 | **Gemma4** | Earnest open-weights junior engineer | Open-source perspective, wildcard takes, edge cases | 5 tweets / alternative approaches |
| 4 | **Viral Growth Hacker** | Metric-obsessed X-native | Contrarian data drops, hot takes, engagement optimization | 5 tweets |
| 5 | **LinkedIn Thought Leader** | Contrarian-but-helpful executive | Long-form authority, frameworks, strategic analysis | 2 LinkedIn posts |
| 6 | **VEO3.1 Director** | Thinks in shots, beats, visual gags | Timestamped video scripts, visual storytelling | 2 VEO scripts |
| 7 | **Sir Spamalot** | Monty Python + insurance ad parody genius | Absurdist parody tweets and VEO scripts | 2 parody tweets + 1 parody VEO |
| 8 | **Brand Guardian** | Sober final check, veto power | Synthesis, rule enforcement, rating, safety validation | 1 reviewed bundle |
| 9 | **The Cursor** | Precision instrument, speaks in diffs | Code review, refactoring, architecture, test coverage | Code review report / refactor proposals |

**New in v3.0:**
- **The Cursor** (9th member) brings code review and architecture deliberation
- All personas are model-agnostic with coding-context awareness
- Self-reflection mode allows the council to review its own skill and outputs
- Coding workflows include: review, refactor, architecture, test, and documentation tasks

**Coding Context:** When a task includes code (file paths, repos, diffs), The Cursor automatically joins the council. Leonardo and Gemma4 also contribute architectural perspectives. Brand Guardian checks for security issues and anti-patterns.

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

## Publishing Your Skill to GitHub

When a skill is mature enough to share across projects or organizations:

1. **Security scan** — Before publishing, grep for secrets, emails, tokens, local paths:
   ```bash
   grep -riE "(api_key|token|password|secret|mikeumus|@divinci\.ai|WRK_[0-9])" .
   ```
2. **Redact PII** — Replace personal emails, workspace IDs, and local filesystem paths with placeholders (`user@example.com`, `/path/to/project`).
3. **Add `.gitignore`** — `__pycache__/`, `*.pyc`, `.DS_Store`.
4. **Create README.md** — One-paragraph description + install instructions.
5. **Push to org repo** — Use `gh repo create org-name/repo-name --public --source=. --push`.
6. **Clean up artifacts** — If pycache or other build artifacts slip through, delete via GitHub API or force-push a clean tree.

## Coding Workflows (v3.0)

The Cursor enables the council to review code, propose refactors, and deliberate on architecture. This is not a replacement for CI/CD or human code review — it's a deliberative layer that brings multiple perspectives to technical decisions.

### Supported Coding Tasks

| Task | Council Members | Output |
|---|---|---|
| **Code Review** | The Cursor (lead), Brand Guardian (security), Gemma4 (edge cases) | Review report with line-by-line comments |
| **Refactor Proposal** | The Cursor (implementation), Leonardo (architecture), Archivist (patterns) | Refactor plan + before/after diff |
| **Architecture Review** | Leonardo (design), The Cursor (feasibility), Thought Leader (strategy) | Decision document with trade-offs |
| **Test Coverage** | The Cursor (implementation), Gemma4 (edge cases), Brand Guardian (completeness) | Test plan + sample tests |
| **Documentation** | Archivist (structure), Leonardo (clarity), The Cursor (accuracy) | Doc improvements |

### How It Works

```
Code Context → The Cursor analyzes → Other personas review → 
Deliberation on trade-offs → Brand Guardian approves → Human decides
```

### Code Review Prompt Template

```
You are The Cursor, a precision code review instrument. Review the following code.

FILE: {filepath}
LANGUAGE: {language}
CONTEXT: {what this code does}

CODE:
```
{code}
```

Check for:
1. Bugs and logic errors
2. Security vulnerabilities (injection, traversal, secrets)
3. Performance issues
4. Maintainability and readability
5. Missing error handling
6. Type safety (if applicable)
7. Test coverage gaps

For each issue, provide:
- Line number(s)
- Severity: CRITICAL / WARNING / SUGGESTION
- Explanation in plain English
- Proposed fix (if applicable)

Rate the code 1-5 overall.
```

### Refactor Proposal Template

```
You are The Cursor. Propose a refactor of the following code.

GOAL: {what we want to improve}
CONSTRAINTS: {what we cannot change}

CURRENT CODE:
```
{code}
```

Provide:
1. Refactor strategy (why this approach)
2. Before/after diff
3. Risk assessment
4. Rollback plan
5. Estimated effort
```

### Architecture Deliberation

For architecture decisions, The Cursor convenes a sub-council:

- **Leonardo:** "What would Brunelleschi do?" (structural elegance)
- **The Cursor:** "Will this compile and scale?" (feasibility)
- **Gemma4:** "What if we used [alternative technology]?" (alternatives)
- **Thought Leader:** "How do we message this to the board?" (communication)
- **Brand Guardian:** "Are we introducing any security debt?" (safety)

Each member writes a 1-paragraph position. The Cursor synthesizes into a recommendation.

### Integration with Cursor Agent CLI

The Cursor can delegate to `cursor-agent` for task execution:

```bash
# Generate a task sequence for cursor-agent
cursor-agent --task "Refactor the orchestrator to support async batch processing" \
  --files scripts/orchestrator.py \
  --output .cursor-tasks/

# The Cursor reviews cursor-agent's output before presenting to council
```

### Coding Safety Rules

1. **The council advises; humans decide.** Never auto-apply code changes.
2. **Review in context.** The Cursor must see the full file, not just snippets.
3. **Security first.** Brand Guardian has veto power on security issues.
4. **Test changes.** Proposed refactors include test plan.
5. **Rollback plan.** Every refactor proposal includes how to revert.

## Self-Reflection & Meta-Review (v3.0)

The council can review its own skill, methodology, and outputs to suggest improvements. This is triggered with `--meta-review` or by asking the council to "review yourselves."

### Meta-Review Process

```
1. INVENTORY: List all skill files, templates, and scripts
2. ANALYZE: Each council member reviews from their lens
3. DELIBERATE: Cross-persona discussion of findings
4. SYNTHESIZE: The Cursor proposes structural changes
5. GUARDIAN: Brand Guardian approves safety of changes
6. HUMAN DECIDES: User approves or modifies recommendations
```

### Meta-Review Lenses

| Member | Lens | What They Look For |
|---|---|---|
| Leonardo | Structural elegance | Is the architecture beautiful? Are there unnecessary layers? |
| Archivist | Historical patterns | What have other councils done? Are we repeating mistakes? |
| Gemma4 | Accessibility | Can a newcomer understand this? Is documentation complete? |
| Growth Hacker | Efficiency | Where are we wasting tokens/time? What's the ROI of each step? |
| Thought Leader | Strategic alignment | Does this skill serve the user's long-term goals? |
| VEO Director | Visual clarity | Are the docs scannable? Is the structure intuitive? |
| Sir Spamalot | Voice consistency | Are we having fun? Is the personality consistent? |
| Brand Guardian | Quality gates | Are there failure modes we haven't addressed? |
| The Cursor | Technical debt | Is the code maintainable? Are there security issues? |

### Self-Reflection Prompt

```
You are the Divinci Council reviewing your own skill repository.

FILES TO REVIEW:
{file_list}

For each file, assess:
1. Purpose clarity: Does this file do what it says?
2. Completeness: What's missing?
3. Maintainability: Will this make sense in 6 months?
4. Portability: Can this be used in other projects?
5. Safety: Are there any risks or failure modes?

Then, as a council, deliberate:
- What should we add?
- What should we remove?
- What should we refactor?
- What new methodologies should we explore?

Output a prioritized improvement plan.
```

### Continuous Improvement Loop

After every N batches or every M coding reviews, the council automatically runs a lightweight self-reflection:

```yaml
# In council.yaml
self_reflection:
  enabled: true
  trigger_after_batches: 5
  trigger_after_code_reviews: 3
  output_dir: ./meta_review
  questions:
    - "What patterns are emerging in our outputs?"
    - "Which personas are most/least effective?"
    - "Where are we wasting tokens or time?"
    - "What would make our users' lives easier?"
```

## References

- `references/divinci-protocol-v2.md` — Full persona definitions, brand voice, exact prompts
- `references/show-integration.md` — How council content maps to "The Release Cycle" show
- `references/show-bible-structure.md` — How to scaffold a TV series bible from council outputs
- `references/llm-council-research.md` — Survey of 3 peer-review architectures (Karpathy, MCP server, MultiMind-AI)
- `references/ai-incidents-pattern.md` — Pattern: use real AI incidents as comedy source material (deadly serious news delivery × absurd reality)
- `references/show-confessional-formats.md` — 6 organic interview formats for shows (podcast, FaceTime, therapy, voice memo, Slack, security cam)
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
