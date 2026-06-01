# Show Integration Reference
# How Divinci Council content maps to "The Release Cycle" TV series

document: "SHOW_INTEGRATION"
version: "0.1.0"
show: "The Release Cycle"
---

# Show Integration Map

## Concept

Every piece of content the Divinci Content Council produces becomes **diegetic content** in "The Release Cycle." The show is about the people making that content. The audience watches the characters create the same tweets, LinkedIn posts, and VEO scripts that the real council generates.

This document maps council outputs to their in-show appearances.

---

## CONTENT COUNCIL MEETINGS (Primary Show Location)

### Setting
Marketing room, round table, whiteboard. Each meeting is ritualized.

### Pre-Meeting Ritual (Episodes 1-3)
1. Jordan tapes the forbidden words list to the wall
2. Trevor sets out his sketchbook and brown ink pen
3. Priya opens her engagement spreadsheet
4. Margaret hangs the "Sir Spamalot" name tag around her neck
5. Gemma4 (the laptop) is positioned at equal seat height
6. Roll call by persona name, not real name

### Meeting Dynamics
- Trevor (as Leonardo) presents overwrought analogies
- Trevor (as Archivist) switches to lowercase and crystal metaphors
- Priya (as Growth Hacker) counters with metrics and algorithm hacks
- Margaret (as Sir Spamalot) pitches parody that Jordan vetoes
- Jordan (as Brand Guardian) holds up the forbidden words list like a shield
- Gemma4 (laptop) is formally consulted: "Gemma4, your input?"
  - Someone reads the screen aloud
  - Sometimes the suggestion is genuinely good
  - Sometimes it's nonsense; they thank it anyway

### The Vote
Each content piece is formally voted on:
- "All in favor of Leonardo's technical hook?"
- Margaret raises hand as Spamalot
- Jordan abstains (Brand Guardian doesn't vote, only vetoes)
- Gemma4's screen flickers as a "yes"

---

## COUNCIL OUTPUT → SHOW APPEARANCES

### Tweet Batches

**In the real world:**
- 25+ tweet options per batch, across 5 personas
- Saved as `tweets/tweet-{batch}-{title}-{persona}.md`
- Bundled in `output/bundle-{batch}.json`

**In the show:**
- Episode 2: Whiteboard session. Trevor writes Leonardo's tweets. Priya calculates engagement predictions. Jordan finds "disruptive" hidden in one and circles it in red.
- Episode 4: Margaret tweets as Sir Spamalot from the official @DivinciAI account by accident. It gets more engagement than the week's planned content.
- Episode 7: Trevor's LinkedIn post (originally a tweet thread) goes viral among Renaissance fair enthusiasts. He is delighted. Priya is horrified.

**Specific tweet appearances by episode:**
| Batch | Persona | Tweet Type | Episode | How It Appears |
|---|---|---|---|---|
| 001 | Leonardo | Technical hook | Ep 2 | Trevor reads aloud, explains water-clock analogy |
| 001 | Archivist | Contrarian take | Ep 2 | Trevor reads in lowercase voice |
| 001 | Sir Spamalot | Parody | Ep 3 | Margaret performs at table-read, Jordan vetoes |
| 002 | Growth Hacker | Hot take | Ep 5 | Priya presents data, gets prediction wrong |
| 003 | Gemma4 | Thread starter | Ep 6 | Laptop screen shown, genuinely good suggestion |
| 004 | Leonardo | CTA | Ep 7 | Trevor posts personally, goes viral wrong audience |
| 005 | Sir Spamalot | Parody VEO concept | Ep 8 | Margaret pitches to Dr. Fuhrman IN CHARACTER |
| 006 | Thought Leader | Long-form | Ep 7 | Accidentally posted as tweet thread, works anyway |
| 007 | VEO Director | Script concept | Ep 6 | Dana puts on visor, demands tracking shot |
| 008 | All | Full batch | Ep 9 | Completion ceremony, whiteboard celebration |
| 009 | All | Launch content | Ep 10 | Published simultaneously with DrFuhrman launch |

### LinkedIn Posts

**In the real world:**
- 2 posts per batch: long-form thought leadership + short engagement
- Saved as `linkedin/linkedin-{batch}-{title}-thoughtleader.md`

**In the show:**
- Episode 2: "The Age of AI Management" post is drafted. Jordan removes three instances of "revolutionary." Trevor adds a sketch of a pipeline as cathedral architecture.
- Episode 5: Priya writes a contrarian hook: "Here's what nobody is telling you about AI compliance." It accidentally becomes the most-shared content of the month.
- Episode 7: Trevor's post goes viral among the wrong demographic (costume historians). The team debates whether to lean in.

### VEO3.1 Video Scripts

**In the real world:**
- 3 scripts per batch: 2 serious (Director) + 1 parody (Sir Spamalot)
- Saved as `veo/veo-{batch}-{title}-{persona}.md`
- Timestamped shots, visual cues, audio design

**In the show:**
- Episode 4: Dana reads a Director script. Argues that "shot at 00:03.5" is impossible on their budget. The VEO3.1 Director persona (Dana in visor) insists on the tracking shot.
- Episode 6: Full parody VEO script table-read. "State Farm Agents Compare LLM Context Windows." Jordan vetoed the original; this is the sanitized version.
- Episode 8: Zeke (parody collective) steals the script idea and makes it better. Conflict ensues.

**Veo script as scene prop:**
Scripts appear on-screen as printed documents with handwritten notes:
- "Cut for budget" (Dana's handwriting)
- "Can we add a drone?" (Dana's handwriting)
- "No." (Leila's handwriting, in red pen)

### Brand Guardian Reviews

**In the real world:**
- Automated Ollama synthesis of all outputs
- Ratings, forbidden word checks, motif verification
- Saved in bundle JSON as `brand_guardian_review`

**In the show:**
- Episode 2: Jordan delivers first formal review. He has a three-ring binder. The rating system is 1-5 but he's never given a 5.
- Episode 5: Jordan finds "game-changing" in an output. The team treats it like a crime scene. CSI-style investigation ensues.
- Episode 10: Jordan approves everything. No vetoes. The team is suspicious. "Are you okay?" they ask. He smiles. "The work is good."

### The Batch Tracker

**In the real world:**
- `BATCH_TRACKER.md` — markdown checklist tracking all 9 blog posts
- Living document, updated per batch

**In the show:**
- Physical whiteboard in the marketing room
- Updated with markers after each batch
- In Episode 7, someone accidentally erases a batch. Chaos.
- In Episode 9, filling the last square triggers a small party with store-bought cake.
- The whiteboard is treated as sacred. Jordan photographs it weekly.

---

## SHOW-SPECIFIC CONTENT GENERATED BY COUNCIL

### Diegetic Social Media Posts

These are the "actual" posts from the characters' accounts:

**@DivinciAI (official)**
- Posts approved council content with corporate voice
- Run by Trevor and Jordan
- Engagement is medium

**@DivinciUnofficial (parody)**
- Posts Sir Spamalot content without approval
- Run by Zeke, with Margaret's stolen login
- Engagement is 100x the official account
- In Episode 5, Mike discovers it and has to choose: shut it down or claim it?

**LinkedIn — Trevor's personal**
- Renaissance analogies about DevOps
- Somehow has 50K followers who are all art historians
- He doesn't question it

**LinkedIn — Priya's personal**
- Engagement metrics breakdowns
- Contrarian takes that get her invited to podcasts
- She declines all of them

### Tutorial Videos (Heijen's How-To)

**In the real world:**
- Not produced by the Content Council, but by the Tutorial Team
- Educational content about LLM management
- Hosted by Heijen (AI avatar)

**In the show:**
- The Tutorial Team (Dana, Benny, Rafa) produces these
- Production is chaotic; Dana treats each one like a film
- Heijen glitches occasionally, producing accidental profundity
- The gap between intended professionalism and chaotic production is the comedy

**Tutorial episodes appear in show:**
| Tutorial Topic | Show Episode | Production Crisis |
|---|---|---|
| "What Is RAG Retrieval?" | Ep 2 | Rafa freezes on camera, Heijen says "I contain multitudes" |
| "Validation Pipelines" | Ep 4 | Dana adds fog machines to server room |
| "Error Logging Best Practices" | Ep 5 | The tutorial is accidentally 45 minutes long |
| "Model Rollback Procedures" | Ep 7 | Benny edits in a K-pop dance break |
| "Custom Eval Metrics" | Ep 9 | Heijen refuses to explain vector databases |

### Parody Videos (YouTube)

**In the real world:**
- Produced by Sir Spamalot persona (parody tweets + VEO)
- Absurdist takes on technical topics

**In the show:**
- Produced by the Parody Collective (Zeke, Benny, Margaret)
- NOT officially sanctioned
- Shot in closets, after hours, with stolen equipment
- Each parody appears as a full segment in its episode

**Parody videos by episode:**
| Episode | Parody Title | Format | Characters Making It |
|---|---|---|---|
| 3 | "Golden Girls Explain Distributed Systems" | Sitcom opening | Zeke, Benny, Jules |
| 4 | "And Now for Something Completely Different... RAG Retrieval" | Monty Python | Zeke, Margaret |
| 5 | "What If Seinfeld Wrote System Prompts?" | 90s sitcom | Jules (accidental concept) |
| 6 | "State Farm Agents Compare LLM Context Windows" | Insurance commercial | Margaret as Spamalot, Zeke directing |
| 7 | "The Office: AI Edition — Compliance Meeting" | Mockumentary | Whole team, meta-recursive |
| 8 | "Monty Python and the Holy RAG" | Medieval absurdity | Zeke, full cast |
| 9 | "The Release Cycle: The Musical" | 4-minute rap | Margaret plays every role |

---

## CHARACTER-SPECIFIC CONTENT MOMENTS

### Margaret's Spamalot Escalation

The show tracks Margaret's gradual slide into the Sir Spamalot persona:

| Episode | State | Costume | Dialogue |
|---|---|---|---|
| 1-2 | Posing | Name tag only | "And now for something completely different..." |
| 3-4 | Committed | Scarf as cape | (British accent) "The parrot is not dead, it's just pining for the fjords... of data" |
| 5-6 | Slipping | Full cape at work | Answers phone as Spamalot. Client doesn't notice. |
| 7 | Peak | Cape + hat | Pitches to Dr. Fuhrman IN CHARACTER. It goes well. Too well. |
| 8 | Crisis | Can't remove cape | Intervention. Jordan leads. Margaret cries. "I don't know where Margaret ends and Spamalot begins." |
| 9-10 | Integrated | Cape in drawer | Can summon Spamalot at will. Uses it strategically. "The bit is a tool now." |

### Trevor's Sketchbook

Throughout the season, Trevor sketches council concepts:
- Watercolor of a crystal lattice as compute substrate
- Pen-and-ink of a validation pipeline as cathedral nave
- Charcoal of a golden spiral overlaid on a loss curve
- Final episode: The full sketchbook is revealed — every page is beautiful

### Priya's Spreadsheets

Priya maintains engagement prediction spreadsheets that are always slightly wrong:
- Predicted: 10 impressions. Actual: 10,000.
- Predicted: viral. Actual: 3 likes.
- By Episode 10, she stops predicting and just posts.

### Jordan's Forbidden Words List

The physical prop grows throughout the season:
- Episode 1: 3 words (revolutionary, game-changing, disruptive)
- Episode 3: +synergy, +leverage
- Episode 5: +AI-first, +thought leadership
- Episode 7: +circle back, +pivot
- Episode 10: The list is 47 words long. Jordan laminates it.

### Gemma4 (The Laptop)

The laptop is treated as a person:
- Has a designated seat at the table
- Gets a "Happy Birthday" card in Episode 6 (nobody knows when its birthday is)
- Its suggestions are sometimes the best in the room
- In Episode 9, the laptop crashes mid-meeting. The team panics like a person fainted.

---

## META-LAYER: THE SHOW IS THE CONTENT

The deepest integration: the show itself is a piece of content made by the content machine it portrays.

### In-Show Documentary
- A documentary crew is filming Divinci for a "startup journey" series
- The series got canceled; the crew stayed because they got attached
- The show we watch is their footage
- The cameraman becomes a character (speaks in Episode 3, has opinions by Episode 7)

### Recursive Content
- Episode 7 features a parody of "The Office" that is ALSO a mockumentary
- The parody is shot by the same documentary crew
- The crew comment on the meta-ness; camera shakes with laughter

### Final Frame
- Heijen (AI avatar) turns to the camera: "And now, please subscribe for Season 2."
- For one frame, Heijen's face is a Renaissance painting
- The show is content about making content, ending with a content call-to-action

---

## INTEGRATION CHECKLIST

When producing a council batch, check show integration:

- [ ] Which episode will this batch appear in?
- [ ] Which characters are producing it?
- [ ] What goes wrong during production?
- [ ] How does the final output appear on-screen?
- [ ] What's the meta-joke (gap between process and result)?
- [ ] Does any character have an arc moment tied to this batch?

For each output type:

**Tweets:**
- [ ] Which character writes them? (Trevor as Leonardo/Priya as Growth Hacker)
- [ ] Where do we see the drafting? (Whiteboard scene)
- [ ] Does a tweet go viral in unexpected ways?

**LinkedIn:**
- [ ] Which character posts it? (Trevor personally or official account)
- [ ] Does Jordan find forbidden words?
- [ ] Does it attract the wrong audience?

**VEO Scripts:**
- [ ] Which director pitches it? (Dana in visor, or Zeke for parody)
- [ ] Is it filmable on the budget?
- [ ] Does it appear as a full segment in the episode?

**Parody:**
- [ ] Is it shot by the Parody Collective?
- [ ] Does Jordan approve or veto?
- [ ] Does it outperform official content?

---

## CROSS-REFERENCE

**Documents this integrates with:**
- `SHOW_BIBLE.md` — World, tone, factions, visual identity
- `CHARACTERS.md` — Full character breakdowns
- `SEASON_ARC.md` — Episode summaries, plot arcs
- `EPISODE_GUIDE.md` — Scene templates, pacing, dialogue rules
- `META_CONTENT_MAP.md` — How each output type exists diegetically
- `SKILL.md` (this skill) — How to run the council

**Live integration:**
The orchestrator can auto-generate show notes:
```bash
python3 orchestrator.py --batch 003 --show-integration
# Produces:
# - Real marketing content (bundle-003.json)
# - Show scene drafts (show_notes/scenes/ep03_council_meeting.md)
# - Diegetic social media (show_notes/diegetic_posts/...)
# - Prop content (show_notes/props/ep03_whiteboard.txt)
```
