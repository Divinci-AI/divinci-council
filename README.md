# Divinci Council

> *"Like a good council, Divinci is there... generating content at 2 AM while you sleep."* — Sir Spamalot

A multi-persona deliberation pipeline that transforms blog posts into platform-native content **and** reviews code architecture **and** generates comedic scripts about AI industry mishaps. Runs on local Ollama, cloud APIs, or your current Hermes session.

Think of it as a writers' room that happens to include a Renaissance inventor, an Atlantean archivist, a viral growth hacker, a LinkedIn thought leader, a VEO director, a Monty Python parodist, a brand guardian, and now — a code review cursor.

[SKILL.md](SKILL.md) · [v3.0 Release Notes](#v30-whats-new) · [The Show](#the-release-cycle-tv-series)

---

## Quick Start

```bash
# Clone into your Hermes skills directory
git clone https://github.com/Divinci-AI/divinci-council.git \
  ~/.hermes/skills/creative/divinci-council

# Or run standalone
cd divinci-council
cp templates/council.yaml ./council.yaml
cp templates/brand-guide.md ./brand-guide.md
# Edit council.yaml with your project settings
python3 scripts/orchestrator.py --batch 001
```

**Prerequisites:** Python 3.10+, PyYAML, and at least one backend:
- [Ollama](https://ollama.com) running locally (recommended for bulk)
- [OpenCode CLI](https://opencode.ai) for cloud models
- [cursor-agent](https://cursor.com) for code review
- Or just use Hermes native — no extra installs

---

## What It Does

The council reads your blog posts and generates:

| Output | Count | Personas |
|--------|-------|----------|
| **Tweets** | 7-15 | Leonardo, Archivist, Gemma4, Growth Hacker, Sir Spamalot |
| **LinkedIn Posts** | 2 | Thought Leader |
| **VEO3.1 Scripts** | 3 | VEO Director, Sir Spamalot (parody) |
| **Show Scenes** | ∞ | All 9 (diegetic content for "The Release Cycle") |

And now in v3.0:

| Output | Trigger | Personas |
|--------|---------|----------|
| **Code Review** | `--code-review file.py` | The Cursor |
| **Architecture Review** | `--architecture-review` | The Cursor + Leonardo + Thought Leader |
| **Meta-Review** | `--meta-review` | Brand Guardian synthesizes all 9 lenses |
| **Self-Reflection** | After N batches | Council reviews its own outputs and methodology |

Every piece of content is reviewed by the **Brand Guardian** for forbidden words, tone consistency, and thematic motifs.

---

## The Nine Council Members

| Member | Voice | Specialty |
|--------|-------|-----------|
| **Leonardo** | Renaissance inventor sketching flying machines | Conceptual hooks, architectural insights |
| **Atlantean Archivist** | Keeper of crystal-memory, speaks in harmonics | Poetic-prophetic framing, lower-case flow |
| **Gemma4** | Earnest junior engineer, Star Wars references | Open-weights perspective, edge-case hunter |
| **Viral Growth Hacker** | Engagement-obsessed X native | Algorithm-aware virality optimization |
| **LinkedIn Thought Leader** | Contrarian-but-helpful executive | Data-dense long-form authority posts |
| **VEO3.1 Director** | Thinks in shots, beats, visual gags | Timestamped video scripts, no lip-sync |
| **Sir Spamalot** | Monty Python + State Farm parody genius | Absurdist, legally-safe transformative parody |
| **Brand Guardian** | Sober final check | Quality gates, forbidden-word enforcement, security |
| **The Cursor** *(NEW in v3.0)* | Precision instrument, diff-native | Code review, refactoring, architecture deliberation |

Each member can be routed to a different model backend. Leonardo runs on your laptop via Ollama. The Cursor delegates to cursor-agent CLI. The Brand Guardian uses whatever deep-reasoning model your Hermes session provides.

---

## v3.0: What's New

### Coding Workflows
The council now reviews code, not just prose:

```bash
# Review specific files with The Cursor
python3 scripts/orchestrator.py --code-review src/api.py src/models.py

# Get architecture assessment
python3 scripts/orchestrator.py --architecture-review
```

The Cursor checks for bugs, security vulnerabilities, performance issues, missing error handling, and test coverage gaps. Every finding includes line numbers, severity (CRITICAL/WARNING/SUGGESTION), and proposed fixes.

**Safety rule:** The council advises; humans decide. No auto-deployment. No "fix it for me" mode. The Cursor reports; you refactor.

### Self-Reflection
After every 5 batches or 3 code reviews, the council can review itself:

```bash
# Meta-review: all 9 members assess the skill repository
python3 scripts/orchestrator.py --meta-review
```

Each member contributes from their lens:
- Leonardo assesses structural elegance
- The Cursor hunts technical debt
- Brand Guardian checks for failure modes
- Sir Spamalot... makes sure we're still funny

Output: a prioritized improvement plan with specific file references. See [meta_review/](meta_review/) for an example.

### Continuous Improvement
The council evaluates its own capabilities and explores new methodologies. The `self_reflection` config in `council.yaml` lets you set trigger thresholds, review questions, and output formats.

---

## The Release Cycle (TV Series)

This skill has a second life as the content engine behind **"The Release Cycle,"** a workplace mockumentary in the style of *Silicon Valley* (HBO) meets *The Office*.

**The premise:** Every piece of content the council generates is also canon in the show. The tutorial videos, parody ads, and LinkedIn posts created by the pipeline are the same ones the fictional Divinci team creates on-screen. The council IS the show's writers' room.

**Real stories, alt reality:** The show tells actual Divinci AI stories — customer demos that flopped, advisor meetings that went sideways, team members debugging at 3 AM, "building in public" mishaps — through a comedic lens. The AI industry news (Starbucks rolling back AI, Klarna's AI customer service, Salesforce rehiring humans) becomes fodder for the show's fictional news parodies.

**Characters:** The council personas map directly to show characters:
- Trevor (Content Strategist) channels Leonardo
- The Laptop (literal laptop on table) IS Gemma4
- Priya (Growth Lead) runs the Growth Hacker playbook
- Margaret (Marketing) gradually becomes Sir Spamalot
- Jordan (Brand Manager) enforces the forbidden words list

See [references/show-integration.md](references/show-integration.md) for the full mapping and [references/AI_INCIDENTS_REFERENCE.md](references/AI_INCIDENTS_REFERENCE.md) for the real-world comedy source material.

---

## Configuration

### council.yaml

```yaml
project_name: "Divinci AI"
source_domain: "https://divinci.ai/blog"

models:
  ollama_local:
    type: ollama
    url: http://localhost:11434/api/generate
    model: gemma4:latest

  cursor_agent:
    type: cursor
    cli_path: /Users/mikeumus/.local/bin/cursor-agent
    reasoning_model: ollama_local

personas:
  leonardo:
    model: ollama_local
    temperature: 0.9

  cursor:
    model: cursor_agent

coding:
  enabled: true
  review_paths:
    - ./src
    - ./scripts
  review_depth: comprehensive  # quick | standard | comprehensive

self_reflection:
  enabled: true
  trigger_after_batches: 5
  trigger_after_code_reviews: 3
  questions:
    - "What patterns are emerging in our outputs?"
    - "Which personas are most/least effective?"
    - "Are our coding reviews catching real issues?"
```

Full template: [templates/council.yaml](templates/council.yaml)

### Brand Voice

The council enforces your brand rules automatically:

```yaml
brand:
  forbidden_words:
    - "revolutionary"
    - "game-changing"
    - "disruptive"
  required_motifs:
    - "golden spiral"
    - "crystal lattice"
    - "solar abundance"
  character_desc: "Young Leonardo da Vinci sketching robots at a cleanroom bench"
```

Full template: [templates/brand-guide.md](templates/brand-guide.md)

---

## Model Backends

| Backend | Speed | Cost | Best For |
|---------|-------|------|----------|
| **Ollama** | ~30s/persona | Free | Bulk content, local privacy |
| **OpenCode** | ~15s/persona | Free/Paid | Fast cloud generation |
| **Hermes Native** | Instant | Session cost | Complex reasoning, Brand Guardian |
| **cursor-agent** | ~60s/file | Cursor sub | Code review, refactoring |
| **API** (OpenAI/Anthropic) | ~10s/persona | Per-token | High-quality output |

Mix and match per persona. Leonardo and Gemma4 run locally. The Cursor uses cursor-agent. Brand Guardian uses your Hermes session. No single vendor lock-in.

---

## Output Structure

```json
{
  "source_post": { "url": "...", "title": "...", "word_count": 4200 },
  "council_run": {
    "run_id": "2026-06-01T07-45-00Z",
    "council_version": "3.0",
    "deliberation": true,
    "models_used": ["ollama_local", "hermes_native"]
  },
  "tweets": [...],
  "linkedin_posts": [...],
  "veo_scripts": [...],
  "persona_outputs": { "leonardo": "...", "archivist": "..." },
  "brand_guardian_review": "APPROVED"
}
```

---

## Safety & Security

- **No auto-deployment.** The council generates; humans decide.
- **No secrets in prompts.** API keys are env vars only.
- **Input validation.** Config paths are validated before shell execution.
- **Security scan.** Run `grep -ri "password\|token\|secret" .` before committing.
- **Backup configs.** The skill creates `.bak` files before editing OpenCode configs.

See [references/opencode-config-fix.md](references/opencode-config-fix.md) for an example of safe config management.

---

## Meta-Review Example

The council reviewed itself in v3.0 and found:

> **Critical:** Zero unit tests on the 1041-line orchestrator.  
> **Critical:** cursor-agent path needs validation.  
> **High:** Shared HTTP logic should be extracted.  
> **Medium:** No file size limits for code review.

Full report: [meta_review/meta_review_20260601_074500.md](meta_review/meta_review_20260601_074500.md)

This is the first open-source project where the maintainers are also the primary QA team... and they happen to be fictional.

---

## Contributing

The council accepts contributions from humans and other LLMs. To contribute:

1. Fork the repository
2. Create a new council member in `personas/` (optional)
3. Add your backend to `scripts/orchestrator.py`
4. Run `python3 scripts/orchestrator.py --meta-review` to let the council review your changes
5. Open a PR with the council's feedback attached

**Code of conduct:** Be excellent to each other. The Archivist is watching.

---

## License

MIT — Use it for your startup, your podcast, your TV show, or your personal blog. Just don't say it was "revolutionary." The Brand Guardian will find you.

---

*Built by Divinci AI. The council deliberates; humans decide.*
