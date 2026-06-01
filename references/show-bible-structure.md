# Show Bible Document Structure
# Reference: how to scaffold a TV series bible from content council outputs

document: "SHOW_BIBLE_STRUCTURE"
version: "0.1.0"
show: "The Release Cycle"
---

# Show Bible Document Structure

## Purpose

When a content council's output becomes diegetic content within a TV series, the show bible serves as the canonical reference for how council personas map to show characters, how batches become episodes, and how marketing content exists within the narrative.

## Document Set

A complete show bible requires 5-6 documents:

| Document | Purpose | Size | Status Indicator |
|----------|---------|------|------------------|
| **SHOW_BIBLE.md** | Logline, world, timeline, factions, tone, visual identity | 5-8K | Required |
| **CHARACTERS.md** | All characters across all factions with relationships | 12-16K | Required |
| **SEASON_ARC.md** | Episode-by-episode plot summaries with A/B/C plots | 14-18K | Required |
| **EPISODE_GUIDE.md** | Structural templates, scene types, dialogue rules, pacing | 15-20K | Required |
| **META_CONTENT_MAP.md** | How real content becomes in-show content | 10-14K | Required |
| **SHOW_INTEGRATION.md** | Cross-reference between content batches and episode scenes | 12-16K | Auto-generated |

## Character Faction Design

Design characters around the content production teams that exist in real life:

| Faction | Real-World Role | Show Role | Comedy Engine |
|---------|-----------------|-----------|---------------|
| Core Engineering | Build the product | Main characters, stakes | Competence vs. chaos |
| Content/Marketing | Create social content | Council meetings, rituals | Process as religion |
| Tutorial Team | Educational videos | Production disasters | Aspiration vs. reality |
| Parody Collective | Unofficial content | Supply closet productions | Unsanctioned genius |
| Client Team | External stakeholder | Outside perspective | They ask the right wrong questions |
| Competitor | Rival company | Antagonist, foil | Their failures validate our approach |

## Council Persona → Show Character Mapping

Each content council persona should map to a specific show character:

```yaml
# From council.yaml show_integration.character_mapping
leonardo: "Trevor (Content Strategist)"
archivist: "Trevor (channeling Atlantean mode)"
gemma4: "The Laptop (literal laptop on table)"
growthhacker: "Priya (Growth Lead)"
thoughtleader: "Trevor (switching to exec mode)"
veodirector: "Dana (Tutorial Director, in visor)"
sirspamalot: "Margaret (Marketing, gradually losing grip)"
brand_guardian: "Jordan (Brand Manager, forbidden words list)"
```

## Batch → Episode Mapping

| Batch | Episode | Scene Type | Characters | Prop/Artifact |
|-------|---------|------------|------------|---------------|
| 001 | Ep 2 | Council meeting | Trevor, Priya, Jordan, Margaret | Whiteboard: first batch |
| 002 | Ep 2 | Whiteboard session | Trevor, Priya | Forbidden words: 3 found |
| ... | ... | ... | ... | ... |

Generate this table automatically via `--show-integration` flag on the orchestrator.

## Cold Open Types

| Type | Description | Best For |
|------|-------------|----------|
| **News** | News anchor montage setting world context | Premiere, season openers |
| **Character gag** | Single character doing something absurd | Mid-season, relationship episodes |
| **Flashback** | Founding moment, origin story | Character development episodes |
| **Content** | In-show content going viral/awry | Meta-commentary episodes |

## Meta-Layer: The Show Is The Content

The deepest integration: the show itself is content made by the content machine it portrays. This requires:

- A documentary crew as character (speaks by Episode 3)
- Recursive parody (Episode 7 parodies The Office using the same documentary crew)
- Final frame: AI avatar addresses camera with content CTA

## Production Note

Total word count for a full show bible: 60-90K words across all documents.
Episode scripts: 20-30K words each (Act One fully scripted, Acts 2-3 outlined).

## Example Path

```
show/
├── SHOW_BIBLE.md
├── CHARACTERS.md
├── SEASON_ARC.md
├── EPISODE_GUIDE.md
├── META_CONTENT_MAP.md
└── scripts/
    ├── EPISODE_101_Hello_World_of_Pain.md
    ├── EPISODE_102_The_Reckoning.md
    └── ...
```
