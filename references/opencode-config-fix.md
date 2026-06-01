# OpenCode CLI Config Fix Pattern
# Reference: how to resolve model routing to antigravity/google models

document: "OPENCODE_CONFIG_FIX"
version: "0.1.0"
opencode_version: "1.15.13"
platform: "macOS"
---

# OpenCode Config Fix Pattern

## The Problem

OpenCode CLI resolves models from five config layers in order:
1. Project `opencode.json` (current working directory)
2. Agent config `~/.config/opencode/oh-my-openagent.json`
3. Global config `~/.config/opencode/opencode.json`
4. Legacy config `~/.opencode/opencode.json`
5. CLI flags (`--model`)

If ANY layer hardcodes `google/antigravity-*`, the `opencode-antigravity-auth@1.6.0` plugin intercepts the request and forces Google OAuth. Even if you set `--model opencode/deepseek-v4-flash`, a project-level `opencode.json` override can force it back to Cloudflare or Google.

## The Five Config Layers

| Priority | File | Typical Override |
|----------|------|------------------|
| 1 (highest) | `./opencode.json` | Often overrides to `cloudflare/@cf/meta/llama-3.1-8b-instruct-fast` |
| 2 | `~/.config/opencode/oh-my-openagent.json` | Often hardcodes ALL agents to `google/antigravity-*` |
| 3 | `~/.config/opencode/opencode.json` | Often hardcodes `model: google/antigravity-claude-opus-4-5-thinking` |
| 4 | `~/.opencode/opencode.json` | Legacy, may contain minimal config |
| 5 (lowest) | CLI flags | `--model opencode/deepseek-v4-flash` |

## The Fix: Patch All Five Layers

### 1. Global Config

```bash
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.$(date +%s).bak
```

Edit `~/.config/opencode/opencode.json`:
```json
{
  "model": "opencode/deepseek-v4-flash",
  "small_model": "opencode/deepseek-v4-flash-free",
  "disabled_providers": ["google"],
  "providers": {
    "opencode": {
      "models": {
        "deepseek-v4-flash": {},
        "deepseek-v4-flash-free": {}
      }
    }
  }
}
```

### 2. Agent Config

```bash
cp ~/.config/opencode/oh-my-openagent.json ~/.config/opencode/oh-my-openagent.json.$(date +%s).bak
```

Edit `~/.config/opencode/oh-my-openagent.json`:
- Remap ALL agent entries (`sisyphus`, `oracle`, `prometheus`, etc.) to `opencode/deepseek-v4-flash` or `opencode/deepseek-v4-flash-free`
- Remap ALL category entries (`visual-engineering`, `ultrabrain`, etc.) similarly
- Set `"google_auth": false`

### 3. Legacy Config

Reduce `~/.opencode/opencode.json` to minimal:
```json
{
  "mcp_servers": {
    "fulcrum": { "command": "node", "args": ["/path/to/mcp-server"] }
  }
}
```

### 4. Project Configs

For EACH worktree with an `opencode.json`:
```bash
# Example worktrees (replace with your paths):
# /path/to/project/opencode.json
# /path/to/project-fv-worktree/opencode.json
# /path/to/project-rag-cli-worktree/opencode.json

# Backup first
cp opencode.json opencode.json.$(date +%s).bak

# Change model line
sed -i '' 's/"model": "cloudflare\/.*"/"model": "opencode\/deepseek-v4-flash"/' opencode.json
```

### 5. CLI Verification

```bash
cd /your/project/path
opencode run --model opencode/deepseek-v4-flash-free "Testing"
# Expected: "Sisyphus - ultraworker · deepseek-v4-flash-free"
```

## The Billing Gotcha

After fixing routing, `opencode/deepseek-v4-flash` (paid) may fail with:
```
Error: No payment method. Add a payment method here:
https://opencode.ai/workspace/WRK_ID/billing
```

Use `opencode/deepseek-v4-flash-free` instead for zero-cost usage.

## Account Selection

`~/.config/opencode/antigravity-accounts.json` may contain multiple Google accounts:
`- Account 0: `user@example.com` (Free Tier, active for Claude family)
`- Account 1: `work@example.com` (Tier 3, active for Gemini family)

If you need antigravity for specific tasks, ensure the Tier 3 account is active:
```bash
opencode providers auth google
# Select the appropriate account for your tier
```

## Key Principle

The fix requires patching ALL layers simultaneously. A single unpatched project-level `opencode.json` will override everything else. Always check `opencode debug config` after patching to verify the resolved model.
