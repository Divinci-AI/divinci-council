#!/usr/bin/env python3
"""
Divinci Council Orchestrator v2.0
Model-agnostic multi-persona content generation pipeline.

Reads council.yaml for configuration, catalog.json for sources,
and generates content bundles using configurable backends (Ollama, OpenCode, API).

Usage:
    python3 orchestrator.py [--batch BATCH_ID] [--dry-run] [--deliberate] [--show-integration]

Backends supported:
    - ollama:    Direct HTTP API to local Ollama instance
    - opencode:  Shell out to opencode CLI
    - hermes:    Write prompt files for Hermes session processing
    - api:       Direct HTTP calls to OpenAI/Anthropic/etc.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def load_config(path: str = "council.yaml") -> dict:
    """Load council.yaml configuration."""
    import yaml
    p = Path(path)
    if not p.exists():
        print(f"Error: {path} not found. Copy from templates/council.yaml", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(p.read_text())


def load_catalog(path: str = "catalog.json") -> list:
    """Load article catalog."""
    p = Path(path)
    if not p.exists():
        print(f"Error: {path} not found. Create your catalog.json", file=sys.stderr)
        sys.exit(1)
    return json.loads(p.read_text())


def ensure_dirs(config: dict) -> None:
    """Create output directories from config."""
    out = config.get("output", {})
    for key in ["articles_dir", "tweets_dir", "linkedin_dir", "veo_dir", "bundles_dir", "show_notes_dir"]:
        dir_path = Path(out.get(key, f"./{key.replace('_dir', '')}"))
        dir_path.mkdir(parents=True, exist_ok=True)
        for sub in ["scenes", "diegetic_posts", "props"]:
            (dir_path / sub).mkdir(parents=True, exist_ok=True)


def log(msg: str, level: str = "INFO"):
    """Print with timestamp."""
    ts = datetime.now().isoformat(timespec="seconds")
    print(f"[{ts}] [{level}] {msg}")


def ollama_generate(prompt: str, system: str, model_config: dict) -> str:
    """Call Ollama API directly."""
    url = model_config.get("url", "http://localhost:11434/api/generate")
    model_name = model_config.get("model", "gemma4:latest")
    timeout = model_config.get("timeout", 300)
    options = model_config.get("options", {})

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": options,
    }
    if system:
        payload["system"] = system

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        log(f"Ollama error: {e}", "ERROR")
        return ""


def opencode_generate(prompt: str, system: str, model_config: dict) -> str:
    """Call opencode CLI."""
    model = model_config.get("model", "opencode/deepseek-v4-flash-free")
    cmd = ["opencode", "run", "--model", model, "--non-interactive"]

    full_prompt = f"{system}\n\n{prompt}" if system else prompt

    try:
        result = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=model_config.get("timeout", 120),
        )
        if result.returncode != 0:
            log(f"opencode stderr: {result.stderr}", "WARN")
        return result.stdout
    except subprocess.TimeoutExpired:
        log("opencode timed out", "ERROR")
        return ""
    except FileNotFoundError:
        log("opencode CLI not found. Install: npm install -g opencode", "ERROR")
        return ""


def api_generate(prompt: str, system: str, model_config: dict) -> str:
    """Call remote API (OpenAI, Anthropic, etc.)."""
    provider = model_config.get("provider", "openai")
    model = model_config.get("model", "gpt-4o")

    if provider == "openai":
        return _openai_generate(prompt, system, model, model_config)
    elif provider == "anthropic":
        return _anthropic_generate(prompt, system, model, model_config)
    else:
        log(f"Unknown API provider: {provider}", "ERROR")
        return ""


def _openai_generate(prompt: str, system: str, model: str, cfg: dict) -> str:
    import os
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        log("OPENAI_API_KEY not set", "ERROR")
        return ""

    url = "https://api.openai.com/v1/chat/completions"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": cfg.get("temperature", 0.8),
        "max_tokens": cfg.get("max_tokens", 4096),
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=cfg.get("timeout", 120)) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"OpenAI error: {e}", "ERROR")
        return ""


def _anthropic_generate(prompt: str, system: str, model: str, cfg: dict) -> str:
    import os
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log("ANTHROPIC_API_KEY not set", "ERROR")
        return ""

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": cfg.get("max_tokens", 4096),
        "temperature": cfg.get("temperature", 0.8),
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=cfg.get("timeout", 120)) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"]
    except Exception as e:
        log(f"Anthropic error: {e}", "ERROR")
        return ""


def hermes_generate(prompt: str, system: str, model_config: dict, persona_key: str, batch_id: str) -> str:
    """
    For Hermes backend, write the prompt to a file for session processing.
    The Hermes agent should be instructed to process pending prompts.
    Returns a placeholder; actual content must be injected manually or via delegate_task.
    """
    pending_dir = Path("./pending_hermes")
    pending_dir.mkdir(exist_ok=True)
    file_path = pending_dir / f"{batch_id}_{persona_key}.json"

    data = {
        "persona": persona_key,
        "batch_id": batch_id,
        "system": system,
        "prompt": prompt,
        "status": "pending",
        "created": datetime.now(timezone.utc).isoformat(),
    }
    file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    log(f"Hermes prompt queued: {file_path}")
    return f"[HERMES_PENDING:{file_path}]"


def generate_with_backend(prompt: str, system: str, persona_key: str, config: dict, batch_id: str) -> str:
    """Route generation to the appropriate backend."""
    personas = config.get("personas", {})
    models = config.get("models", {})

    persona_cfg = personas.get(persona_key, {})
    model_name = persona_cfg.get("model", "ollama_local")
    model_config = models.get(model_name, {"type": "ollama"})
    backend_type = model_config.get("type", "ollama")

    # Apply per-persona temperature override
    if "temperature" in persona_cfg and "options" in model_config:
        model_config = dict(model_config)
        model_config["options"] = dict(model_config["options"])
        model_config["options"]["temperature"] = persona_cfg["temperature"]

    if backend_type == "ollama":
        return ollama_generate(prompt, system, model_config)
    elif backend_type == "opencode":
        return opencode_generate(prompt, system, model_config)
    elif backend_type == "api":
        return api_generate(prompt, system, model_config)
    elif backend_type == "hermes":
        return hermes_generate(prompt, system, model_config, persona_key, batch_id)
    else:
        log(f"Unknown backend type: {backend_type}", "ERROR")
        return ""


def scrape_blog_post(url: str, timeout: int = 30) -> dict:
    """Scrape a blog post using curl + regex HTML parsing."""
    log(f"Scraping {url}...")
    try:
        result = subprocess.run(
            ["curl", "-sL", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url],
            capture_output=True, text=True, timeout=timeout
        )
        html = result.stdout

        title_match = re.search(r'<title>([^<]*)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Unknown"

        # Remove scripts/styles
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Try article/main/body
        article_match = re.search(r'<article[^>]*>(.*?)</article>', text, re.DOTALL | re.IGNORECASE)
        if article_match:
            content = article_match.group(1)
        else:
            main_match = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL | re.IGNORECASE)
            if main_match:
                content = main_match.group(1)
            else:
                body_match = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL | re.IGNORECASE)
                content = body_match.group(1) if body_match else text

        content = re.sub(r'<[^>]+>', ' ', content)
        content = re.sub(r'\s+', ' ', content).strip()

        author_match = re.search(r'By\s+([^•]+)', content)
        author = author_match.group(1).strip() if author_match else "Unknown"

        date_match = re.search(r'([A-Z][a-z]{2,8}\s+\d{1,2},?\s+\d{4})', content)
        date = date_match.group(1) if date_match else ""

        content_preview = content[:8000]
        if len(content) > 8000:
            content_preview += f"\n\n[TRUNCATED — full post is {len(content)} chars]"

        return {
            "title": title,
            "url": url,
            "author": author,
            "date": date,
            "content": content_preview,
            "word_count": len(content.split()),
        }

    except Exception as e:
        log(f"Scrape error: {e}", "ERROR")
        return {"title": "Unknown", "url": url, "author": "", "date": "", "content": "", "word_count": 0}


def forbidden_check(text: str, forbidden: list) -> list:
    """Check for forbidden words."""
    found = []
    lower = text.lower()
    for word in forbidden:
        if word in lower:
            lines = text.split('\n')
            for line in lines:
                if word in line.lower() and 'no ' not in line.lower() and 'forbidden' not in line.lower():
                    found.append(word)
                    break
    return list(set(found))


def motif_check(text: str, required: list) -> list:
    """Check for required motifs."""
    found = []
    lower = text.lower()
    for motif in required:
        if motif.lower() in lower:
            found.append(motif)
    return found


def extract_tweets(text: str) -> list:
    """Parse generated text into structured tweets."""
    tweets = []
    pattern = r'(?:^|\n)\s*(?:#{0,1}\d+[:.)]|\*\*|###|##|\*\s|\-\s|\d+\.\s)\s*(TECHNICAL HOOK|CONTRARIAN TAKE|MEME|THREAD STARTER|CTA|CONTRARIAN DATA DROP|HOT TAKE|MEME/QUOTE-TWEET|ENGAGEMENT FARMER|OPTION \d|Tweet \d|PARODY).*\n(.*?)(?=\n\s*(?:#{0,1}\d+[:.)]|\*\*|###|##|\*\s|\-\s|\d+\.\s)\s*(?:TECHNICAL|CONTRARIAN|MEME|THREAD|CTA|HOT|OPTION|Tweet|PARODY)|$)'
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

    if not matches:
        blocks = re.split(r'\n\s*\n', text)
        for block in blocks:
            block = block.strip()
            if 20 < len(block) < 300:
                tweets.append({"type": "unknown", "text": block})
    else:
        for label, content in matches:
            tweets.append({"type": label.strip(), "text": content.strip()})

    return tweets


def build_prompt(post: dict, persona_key: str, persona_def: dict, brand: dict) -> tuple:
    """Build system and user prompts for a persona."""
    system = persona_def.get("system_prompt", f"You are {persona_key}. Write content.")

    # Inject brand rules into system prompt
    forbidden = ", ".join(brand.get("forbidden_words", []))
    motifs = ", ".join(brand.get("required_motifs", []))
    tone = brand.get("tone", "")
    audience = brand.get("target_audience", "")

    brand_rules = f"""
BRAND RULES:
- Forbidden words (never use): {forbidden}
- Required motifs (work in naturally): {motifs}
- Tone: {tone}
- Target audience: {audience}
"""

    if "BRAND RULES" not in system:
        system = f"{system}\n\n{brand_rules}"

    user_prompt = f"""Based on this blog post, write content as your persona.

BLOG POST: {post['title']}
URL: {post['url']}
CATEGORY: {post.get('category', 'Unknown')}
DATE: {post.get('date', 'Unknown')}
WORD COUNT: {post['word_count']}

FULL CONTENT:
---
{post['content']}
---

YOUR ROLE: {persona_def.get('name', persona_key)}
YOUR VOICE: {persona_def.get('voice', '')}
YOUR TONE: {persona_def.get('tone', '')}

Write {persona_def.get('count', 1)} content piece(s) matching your persona's voice and the blog's technical detail.
Be specific — reference real numbers, tools, or frameworks mentioned in the post.
"""

    return system, user_prompt


def run_brand_guardian(all_tweets: list, all_linkedin: list, all_veos: list, brand: dict, config: dict) -> dict:
    """Generate Brand Guardian review."""
    summary = f"""As the Brand Guardian, review this content batch:

TWEETS ({len(all_tweets)} total):
"""
    for t in all_tweets:
        summary += f"- [{t.get('type','')}]: {t.get('text','')[:80]}...\n"

    summary += f"\nLINKEDIN ({len(all_linkedin)} total):\n"
    for l in all_linkedin:
        summary += f"- [{l.get('type','')}]: {l.get('text','')[:80]}...\n"

    summary += f"\nVEO SCRIPTS ({len(all_veos)} total):\n"
    for v in all_veos:
        summary += f"- [{v.get('title','')}]: {v.get('script','')[:80]}...\n"

    forbidden = ", ".join(brand.get("forbidden_words", []))
    motifs = ", ".join(brand.get("required_motifs", []))

    summary += f"""
Check:
1. Are all tweets under 280 characters?
2. Are there any forbidden words ({forbidden})?
3. Are required motifs ({motifs}) present?
4. Rate each persona's output 1-5.
5. Pick the best tweet, best LinkedIn, and best VEO script.
6. Write an overall verdict: APPROVED or NEEDS REVISION.

Return your review as structured text with clear sections."""

    system = f"""You are the Brand Guardian. Review marketing content against brand rules:
- Forbidden words: {forbidden}
- Required motifs: {motifs}
- All tweets under 280 chars
- Rate outputs 1-5 and give APPROVED/NEEDS REVISION verdict."""

    # Use Brand Guardian's configured backend
    review_text = generate_with_backend(summary, system, "brand_guardian", config, "synthesis")

    # Auto-check forbidden words and motifs across all content
    all_text = " ".join([t.get("text","") for t in all_tweets] +
                        [l.get("text","") for l in all_linkedin] +
                        [v.get("script","") for v in all_veos])

    found_forbidden = forbidden_check(all_text, brand.get("forbidden_words", []))
    found_motifs = motif_check(all_text, brand.get("required_motifs", []))

    return {
        "review_text": review_text,
        "auto_checks": {
            "forbidden_words_found": found_forbidden,
            "motifs_present": found_motifs,
            "tweet_char_violations": [t.get("chars", 0) for t in all_tweets if t.get("chars", 0) > 280],
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": "NEEDS REVISION" if found_forbidden else "APPROVED",
    }


def run_deliberation(persona_outputs: dict, personas: dict, post: dict, brand: dict, config: dict) -> dict:
    """Run peer review round before synthesis."""
    log("Running deliberation (peer review)...")
    reviewers = config.get("orchestrator", {}).get("deliberation_reviewers", ["brand_guardian", "growthhacker", "leonardo"])

    critiques = {}
    for reviewer_key in reviewers:
        if reviewer_key not in personas:
            continue
        reviewer_def = personas[reviewer_key]

        # Build the review prompt
        review_prompt = f"""You are {reviewer_def.get('name', reviewer_key)} reviewing drafts from other council members.

SOURCE ARTICLE: {post['title']}
YOUR LENS: {reviewer_def.get('voice', 'Critical reviewer')}

DRAFTS TO REVIEW:
"""
        for author_key, output in persona_outputs.items():
            if author_key == reviewer_key:
                continue
            review_prompt += f"\n--- FROM {author_key} ---\n{output.get('raw', '')[:2000]}\n"

        review_prompt += """
Critique on: accuracy, hook strength, brand alignment, factual correctness.
Quote exact lines you're critiquing. Rate each draft 1-5.
Suggest one concrete improvement per draft."""

        system = f"You are {reviewer_def.get('name', reviewer_key)}. {reviewer_def.get('system_prompt', '')}"
        critique = generate_with_backend(review_prompt, system, reviewer_key, config, "deliberation")
        critiques[reviewer_key] = critique
        log(f"  Review from {reviewer_key}: {len(critique)} chars")
        time.sleep(1)

    return critiques


def generate_show_notes(bundle: dict, config: dict, batch_id: str, safe_title: str) -> dict:
    """Generate diegetic show content from a bundle."""
    if not config.get("show_integration", {}).get("enabled", False):
        return {}

    show_dir = Path(config.get("output", {}).get("show_notes_dir", "./show_notes"))
    scenes_dir = show_dir / "scenes"
    posts_dir = show_dir / "diegetic_posts"
    props_dir = show_dir / "props"

    # Scene: Content Council Meeting
    characters = config.get("show_integration", {}).get("character_mapping", {})
    scene = f"""## Content Council Meeting — Batch {batch_id}

### Characters Present
"""
    for persona, char in characters.items():
        scene += f"- {char} (as {persona})\n"

    scene += f"""
### Setting
Marketing room, round table. Whiteboard shows batch tracker.

### Ritual Opening
Jordan tapes forbidden words list to wall. Trevor opens sketchbook.
Priya opens engagement spreadsheet. Margaret hangs Sir Spamalot tag.
Gemma4 (laptop) positioned at equal height.

### Roll Call
"""
    for persona in ["leonardo", "archivist", "gemma4", "growthhacker", "sirspamalot", "thoughtleader", "veodirector"]:
        char = characters.get(persona, persona)
        scene += f'- "{char}?" / "Here."\n'

    scene += f"""
### Best Tweet Presentation
Trevor (as Leonardo): "{bundle['tweets'][0].get('text', '')[:100]}..."
Priya: "That analogy is... actually elegant. Predicted engagement: medium."
Jordan: "No forbidden words. Approved."

### Best Parody
Margaret (as Sir Spamalot): "{bundle['veo_scripts'][-1].get('title', 'Parody VEO')}"
Jordan: "Transformative use. Trademark safe. Approved with note: 'don't wear cape to client meeting.'"
Margaret: "That was the old rules."

### Vote
All in favor: unanimous (Jordan abstains, as Brand Guardian)
Gemma4 screen flickers green.

### Closing
Trevor closes sketchbook. Jordan laminates nothing (yet).
Margaret keeps cape on. It's been 3 hours.
"""

    scene_path = scenes_dir / f"ep{batch_id}_council_meeting.md"
    scene_path.write_text(scene, encoding="utf-8")

    # Diegetic posts
    diegetic = {
        "official_tweets": [t.get("text", "") for t in bundle.get("tweets", [])[:3]],
        "official_linkedin": bundle.get("linkedin_posts", [{}])[0].get("text", "") if bundle.get("linkedin_posts") else "",
        "batch_id": batch_id,
        "council_run_id": bundle.get("council_run", {}).get("run_id", ""),
    }
    posts_path = posts_dir / f"ep{batch_id}_diegetic_posts.json"
    posts_path.write_text(json.dumps(diegetic, indent=2), encoding="utf-8")

    # Props: Whiteboard content
    whiteboard = f"""BATCH TRACKER — Updated {datetime.now().strftime('%Y-%m-%d')}

[{bundle.get('source_post', {}).get('title', 'Unknown')[:40]}...] ✅
Next: Batch {int(batch_id) + 1}

Forbidden words found this batch: {len(bundle.get('brand_guardian_review', {}).get('auto_checks', {}).get('forbidden_words_found', []))}
Motifs present: {', '.join(bundle.get('brand_guardian_review', {}).get('auto_checks', {}).get('motifs_present', []))}

Jordan's note: "{bundle.get('brand_guardian_review', {}).get('verdict', 'PENDING')}"
"""
    props_path = props_dir / f"ep{batch_id}_whiteboard.txt"
    props_path.write_text(whiteboard, encoding="utf-8")

    log(f"Show notes generated: {show_dir}/")

    return {
        "scene_path": str(scene_path),
        "posts_path": str(posts_path),
        "props_path": str(props_path),
    }


def process_batch(post: dict, config: dict, personas: dict, brand: dict, dry_run: bool = False, deliberate: bool = False, show_notes: bool = False) -> dict:
    """Process a single blog post through the full council."""
    batch_id = post.get("batch_id", "000")
    log(f"\n{'='*60}")
    log(f"BATCH {batch_id}: {post['title']}")
    log(f"{'='*60}")

    if dry_run:
        log("[DRY RUN — would scrape and generate]")
        return {"batch_id": batch_id, "dry_run": True}

    # Step 1: Scrape
    scrape_cfg = config.get("orchestrator", {})
    article_data = scrape_blog_post(post["url"], scrape_cfg.get("scrape_timeout", 30))
    article_data["category"] = post.get("category", "Unknown")

    # Save article
    out_cfg = config.get("output", {})
    safe_title = re.sub(r'[^a-zA-Z0-9]', '-', post['title'])[:60]
    article_path = Path(out_cfg.get("articles_dir", "./articles")) / f"article-{batch_id}-{safe_title}.md"
    article_content = f"""# {article_data['title']}

Source: {article_data['url']}
Author: {article_data['author']}
Date: {article_data['date']}
Category: {article_data['category']}
Word Count: {article_data['word_count']}

---

{article_data['content']}
"""
    article_path.write_text(article_content, encoding="utf-8")
    log(f"Article saved: {article_path.name}")

    # Step 2: Generate for each persona
    all_tweets = []
    all_linkedin = []
    all_veos = []
    persona_outputs = {}

    persona_order = ["leonardo", "archivist", "gemma4", "growthhacker", "sirspamalot", "thoughtleader", "veodirector", "sirspamalot_veo"]

    cooldown = scrape_cfg.get("persona_cooldown", 1)

    for persona_key in persona_order:
        if persona_key not in personas:
            continue

        persona = personas[persona_key]
        log(f"Generating: {persona.get('name', persona_key)} ({persona.get('content_type', 'unknown')})...")

        system, prompt = build_prompt(article_data, persona_key, persona, brand)

        start = time.time()
        raw_output = generate_with_backend(prompt, system, persona_key, config, batch_id)
        elapsed = time.time() - start
        log(f"  Done in {elapsed:.1f}s ({len(raw_output)} chars)")

        if not raw_output or raw_output.startswith("[HERMES_PENDING"):
            log(f"  ⚠️ Generation pending or failed")
            persona_outputs[persona_key] = {"raw": raw_output, "status": "pending"}
            continue

        content_type = persona.get("content_type", "tweets")

        if content_type in ("tweets", "parody_tweets"):
            extracted = extract_tweets(raw_output)
            for t in extracted:
                t["persona"] = persona_key
                t["chars"] = len(t.get("text", ""))
            all_tweets.extend(extracted)
            persona_outputs[persona_key] = {"raw": raw_output, "extracted": extracted, "status": "done"}
            out_path = Path(out_cfg.get("tweets_dir", "./tweets")) / f"tweet-{batch_id}-{safe_title}-{persona_key}.md"
            out_path.write_text(raw_output, encoding="utf-8")
            log(f"  Saved: {out_path.name}")

        elif content_type == "linkedin":
            posts = [{"type": "long" if i == 0 else "short", "text": p.strip(), "persona": persona_key}
                     for i, p in enumerate(re.split(r'\n\s*\n{2,}', raw_output)) if p.strip()]
            all_linkedin.extend(posts)
            persona_outputs[persona_key] = {"raw": raw_output, "posts": posts, "status": "done"}
            out_path = Path(out_cfg.get("linkedin_dir", "./linkedin")) / f"linkedin-{batch_id}-{safe_title}-thoughtleader.md"
            out_path.write_text(raw_output, encoding="utf-8")
            log(f"  Saved: {out_path.name}")

        elif content_type in ("veo", "veo_parody"):
            scripts = [{"title": f"Script {i+1}", "script": s.strip(), "persona": persona_key, "type": content_type}
                       for i, s in enumerate(re.split(r'#{2,}\s*', raw_output)) if s.strip() and len(s.strip()) > 100]
            if not scripts:
                scripts = [{"title": persona.get("name", ""), "script": raw_output, "persona": persona_key, "type": content_type}]
            all_veos.extend(scripts)
            persona_outputs[persona_key] = {"raw": raw_output, "scripts": scripts, "status": "done"}
            out_path = Path(out_cfg.get("veo_dir", "./veo")) / f"veo-{batch_id}-{safe_title}-{persona_key}.md"
            out_path.write_text(raw_output, encoding="utf-8")
            log(f"  Saved: {out_path.name}")

        time.sleep(cooldown)

    # Step 3: Deliberation (optional)
    if deliberate and config.get("orchestrator", {}).get("enable_deliberation", False):
        critiques = run_deliberation(persona_outputs, personas, article_data, brand, config)
        # TODO: Feed critiques back for revision round
        # For now, include critiques in bundle
        persona_outputs["deliberation"] = critiques

    # Step 4: Brand Guardian
    log("Running Brand Guardian review...")
    review = run_brand_guardian(all_tweets, all_linkedin, all_veos, brand, config)

    # Step 5: Build bundle
    models_used = []
    for pk in persona_order:
        if pk in config.get("personas", {}):
            mname = config["personas"][pk].get("model", "unknown")
            if mname not in models_used:
                models_used.append(mname)

    bundle = {
        "source_post": {
            "url": article_data["url"],
            "title": article_data["title"],
            "category": article_data["category"],
            "date": article_data["date"],
            "author": article_data["author"],
            "word_count": article_data["word_count"],
        },
        "council_run": {
            "run_id": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ"),
            "council_version": "2.0",
            "deliberation": deliberate,
            "models_used": models_used,
            "members": [personas.get(k, {}).get("name", k) for k in persona_order if k in personas],
        },
        "tweets": all_tweets,
        "linkedin_posts": all_linkedin,
        "veo_scripts": all_veos,
        "persona_outputs": persona_outputs,
        "brand_guardian_review": review,
    }

    bundle_path = Path(out_cfg.get("bundles_dir", "./output")) / f"bundle-{batch_id}-{safe_title}.json"
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    log(f"Bundle saved: {bundle_path.name}")

    # Step 6: Show integration (optional)
    if show_notes and config.get("show_integration", {}).get("enabled", False):
        show_paths = generate_show_notes(bundle, config, batch_id, safe_title)
        bundle["show_integration"] = show_paths

    # Re-save with show integration data
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    return bundle


def main():
    parser = argparse.ArgumentParser(description="Divinci Council Orchestrator v2.0")
    parser.add_argument("--batch", help="Process only this batch ID (e.g., 001)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without generating")
    parser.add_argument("--deliberate", action="store_true", help="Enable peer review deliberation round")
    parser.add_argument("--show-integration", action="store_true", help="Generate show notes alongside content")
    parser.add_argument("--config", default="council.yaml", help="Path to council.yaml config")
    args = parser.parse_args()

    log("Divinci Council Orchestrator v2.0")
    log(f"Config: {args.config}")

    config = load_config(args.config)
    catalog = load_catalog()
    ensure_dirs(config)

    # Load persona definitions from config or fallback to built-in
    # For v2.0, personas should be defined in the config or loaded from a separate personas.json
    # Here we use a minimal inline definition for core personas
    personas = {
        "leonardo": {
            "name": "Leonardo the Inventor",
            "voice": "Wide-eyed Renaissance polymath. Sees patterns across art, science, and the future.",
            "tone": "Wonder-filled but precise. Uses analogies from nature, mechanics, light.",
            "content_type": "tweets",
            "count": 5,
            "system_prompt": "You are Leonardo, a Renaissance inventor who sees beauty and pattern in software engineering. You write about LLMs, devops, and compliance with the wonder of someone sketching flying machines before flight existed. Use analogies from clocks, springs, water, light, and geometry. Write 5 tweet options. Each must be under 280 characters. Label each: TECHNICAL HOOK, CONTRARIAN TAKE, MEME/RELATABLE, THREAD STARTER, or CTA/DEMO."
        },
        "archivist": {
            "name": "Atlantean Archivist",
            "voice": "Keeper of crystal-memory. Speaks in resonance, harmonics, and geometric truths.",
            "tone": "Lowercase flow. Crystal lattice metaphors. The golden spiral (φ). Solar abundance.",
            "content_type": "tweets",
            "count": 5,
            "system_prompt": "You are the Atlantean Archivist, keeper of crystal-memory from a solarpunk future. You speak in lowercase flow, using metaphors of crystal lattices, harmonic resonance, golden spirals (φ), solar abundance, and geometric truth. Despite the poetic voice, you are technically precise about LLMs, devops, and compliance. Write 5 tweet options. Each under 280 chars. Label each type."
        },
        "gemma4": {
            "name": "Gemma4 the Local Sage",
            "voice": "Fresh, earnest, surprisingly deep open-weights AI.",
            "tone": "Junior engineer energy. Empire references. Earnest wisdom.",
            "content_type": "tweets",
            "count": 5,
            "system_prompt": "You are Gemma4, an open-weights model running locally. You speak with fresh, earnest energy — like a brilliant junior engineer who just read a seminal paper and can't stop thinking about it. You reference Star Wars, Star Trek, and the Empire series. Write 5 tweet options under 280 chars. Label each type."
        },
        "growthhacker": {
            "name": "Viral Growth Hacker",
            "voice": "Mercenary engagement optimizer. Lives on X.",
            "tone": "Punchy, metric-obsessed. Engage-or-die.",
            "content_type": "tweets",
            "count": 5,
            "system_prompt": "You are a Viral Growth Hacker, an engagement-obsessed content strategist who lives on X/Twitter. You know every algorithm hack, quote-tweet pattern, and reply-guy bait. You are punchy, metric-obsessed, and ruthless about what gets clicks. Write 5 tweets ENGINEERED FOR VIRAL ENGAGEMENT under 280 chars. Label: CONTRARIAN DATA DROP, HOT TAKE, MEME/QUOTE-TWEET BAIT, ENGAGEMENT FARMER, or CTA."
        },
        "sirspamalot": {
            "name": "Sir Spamalot the Parodist",
            "voice": "Monty Python + ad-agency parody genius.",
            "tone": "Absurdist. Legally-safe parody. Transformative use only.",
            "content_type": "parody_tweets",
            "count": 2,
            "system_prompt": "You are Sir Spamalot, a parody artist who is equal parts Monty Python absurdist and ad-agency genius. You see every serious technical blog post as a State Farm insurance commercial waiting to happen. Your parodies are legally safe (transformative, no trademarked logos, no verbatim lyrics) and technically accurate. Write 2 PARODY TWEETS under 280 chars. Make them genuinely funny and technically deep."
        },
        "thoughtleader": {
            "name": "LinkedIn Thought Leader",
            "voice": "Contrarian-but-helpful executive.",
            "tone": "Measured, data-dense.",
            "content_type": "linkedin",
            "count": 2,
            "system_prompt": "You are a LinkedIn Thought Leader — a contrarian-but-helpful executive who builds authority through specificity. You write measured, data-dense posts with genuine frameworks. Write 2 LinkedIn posts: one long-form thought leadership (5-7 meaty paragraphs) and one short engagement post (1-2 paragraphs with open question)."
        },
        "veodirector": {
            "name": "VEO3.1 Director",
            "voice": "Thinks in shots, beats, and visual gags.",
            "tone": "Timestamped beats. No lip-sync dialogue.",
            "content_type": "veo",
            "count": 2,
            "system_prompt": "You are a VEO3.1 Director — you think in shots, beats, and visual gags. You write video scripts with timestamped beats [00:00.0 - 00:02.5], visual descriptions, and audio cues. No lip-sync dialogue — sound design carries everything (crystal hums, water clock glugs, brass bells). Aesthetic: solarpunk cleanroom + workshop. Colors: RED=danger, TEAL-BLUE=safe, GOLDEN=energy. Write 2 VEO scripts, 10-14 seconds, shot-by-shot breakdowns."
        },
        "sirspamalot_veo": {
            "name": "Sir Spamalot (Parody VEO)",
            "voice": "State Farm or Golden Girls parody as VEO3.1 script.",
            "tone": "Absurdist parody. Transformative use.",
            "content_type": "veo_parody",
            "count": 1,
            "system_prompt": "You are Sir Spamalot writing a PARODY VEO3.1 VIDEO SCRIPT. Target: State Farm insurance commercial or 80s sitcom opening. Timestamped video scripts with visual descriptions and audio cues. No lip-sync dialogue. Technically accurate and genuinely funny. Include director notes about why it lands. 12-15 seconds."
        },
        "brand_guardian": {
            "name": "Brand Guardian",
            "voice": "Sober final check.",
            "tone": "Direct, yes/no, with citations.",
            "content_type": "review",
            "count": 0,
            "system_prompt": "You are the Brand Guardian. Review content against brand rules. Give APPROVED or NEEDS REVISION verdict with specific citations."
        },
    }

    brand = config.get("brand", {})

    # Filter catalog if --batch specified
    posts_to_process = catalog
    if args.batch:
        posts_to_process = [p for p in catalog if p.get("batch_id") == args.batch]
        if not posts_to_process:
            log(f"Batch {args.batch} not found in catalog", "ERROR")
            sys.exit(1)

    for post in posts_to_process:
        try:
            process_batch(
                post, config, personas, brand,
                dry_run=args.dry_run,
                deliberate=args.deliberate,
                show_notes=args.show_integration,
            )
        except Exception as e:
            log(f"Failed to process batch {post.get('batch_id')}: {e}", "ERROR")
            import traceback
            traceback.print_exc()

    log("\nOrchestrator complete.")


if __name__ == "__main__":
    main()
