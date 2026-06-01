# Batch Tracker Template
# Copy to your project root as BATCH_TRACKER.md and update per run.

# Divinci Content Council — Batch Tracker

| Batch | Article Title | URL Status | Leonardo | Archivist | Gemma4 | Growth Hacker | Sir Spamalot | Thought Leader | VEO Director | Spamalot VEO | Brand Guardian | Bundle | Notes |
|-------|---------------|------------|----------|-----------|--------|---------------|--------------|----------------|--------------|--------------|----------------|--------|-------|
| 001 | How to Diagnose Custom LLM QA Failures | ✅ 200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Manual run |
| 002 | Automated CI/CD Pipelines with Instant Rollback | ✅ 200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Manual run |
| 003 | Validating and Releasing Custom LMs in Regulated Fields | ✅ 200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Unattended |
| 004 | The 12 QA + Release Capabilities... | ❌→✅ 404→200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Slug fixed, re-ran |
| 005 | 10 CI/CD Release Failures in Custom LMs | ❌→✅ 404→200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Slug fixed, re-ran |
| 006 | CI Testing for Custom Language Models in 2026 | ✅ 200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Unattended |
| 007 | Automated Regression Testing for Custom LLMs in 2026 | ✅ 200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Unattended |
| 008 | Deleting Paris from a Language Model | ✅ 200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Unattended |

## Status Legend

- ✅ Done — batch complete, bundle valid
- 🔄 In Progress — currently generating
- ⏸ Paused — waiting for fix or review
- ❌ Failed — needs repair (see Notes)
- ⏳ Pending — not started

## Bundle Validation Criteria

A bundle is considered valid when ALL of the following pass:

1. **File size > 15KB** (empty or tiny bundles indicate failure)
2. **JSON parses cleanly** (no syntax errors)
3. **All required keys present** (tweets, linkedin_posts, veo_scripts, brand_guardian_review)
4. **Tweets array length >= 7** (at minimum: Leonardo 5 + Archivist 5 + ...)
5. **No forbidden words found** in any output text
6. **Brand motifs present** in at least 2 outputs per batch
7. **Article word count > 800** (indicates real article was scraped, not 404 page)

## Repair Protocol

1. Note the failure in this tracker (status = ❌, add note with diagnosis)
2. Check the specific failure:
   - 404 URL? → Fix slug in orchestrator catalog
   - Empty content? → Re-scrape with browser tools
   - Missing persona output? → Re-run with `--batch N`
   - Invalid JSON? → Check model output for truncation
3. Fix the root cause
4. Re-run the single batch: `python3 orchestrator.py --batch N`
5. Run validation checklist above
6. Update tracker: ❌ → ✅

## Naming Convention

Bundles are named: `bundle-{batch_id}-{sanitized-title}.json`

Sanitized title rules:
- Alphanumeric and hyphens only
- Max 60 chars
- No special characters
- Lowercase

Example: `bundle-003-Validating-and-Releasing-Custom-LMs-in-Regulated-F.json`

## Archive Policy

Invalid bundles are NOT deleted (per user policy). Instead:
- Valid bundles live in `output/`
- Invalid batches may produce `.invalid` suffix files if writing fails
- If a re-run produces two bundles for same batch, use the larger/more recent one
- Document any manual cleanup in Notes column

## Show Integration Tracker

| Batch | Episode | Scene Type | Characters | Prop/Artifact |
|-------|---------|------------|------------|---------------|
| 001 | Ep 2 | Council meeting | Trevor, Priya, Jordan, Margaret | Whiteboard: first batch |
| 002 | Ep 2 | Whiteboard session | Trevor, Priya | Forbidden words: 3 found |
| 003 | Ep 3 | Table-read | Margaret, Jordan | Sir Spamalot vetoed |
| 004 | Ep 4 | Client demo | Carly, Mike | Batch content as pitch deck |
| 005 | Ep 5 | War room | Leila, Rafa | Parody video interrupt |
| 006 | Ep 6 | Tutorial chaos | Dana, Benny, Rafa | VEO script for tutorial intro |
| 007 | Ep 7 | Viral wrong-audience | Trevor | Renaissance fair enthusiasts |
| 008 | Ep 8 | Completion ceremony | All + Gemma4 | Candle, cake, whiteboard photo |

---

## Quick Stats

- Total batches: 9
- Completed: 9
- Automated runs: 6
- Manual runs: 2
- Repairs needed: 2 (batches 004, 005 — URL slug errors)
- Average batch time: ~3 minutes (Ollama gemma4:latest)
- Total generation time: ~28 minutes (6 batches unattended)
- Show scenes generated: 8

Last updated: 2026-06-01
