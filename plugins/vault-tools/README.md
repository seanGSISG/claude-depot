# vault-tools

Skills, rules, and hooks for an Obsidian vault. Install on any machine to get full vault management (notes, search, maintenance, validation) plus automatic plan archival on `ExitPlanMode` — no need to sync hidden `.claude/` folders across machines.

## What's Included

### Skills (10)

| Skill | Purpose |
|-------|---------|
| `/vault-tools:setup` | First-time configuration (set vault path, offer plan bulk-import) |
| `/vault-tools:new-note` | Create a note with proper frontmatter |
| `/vault-tools:vault-search` | Natural language search across vault |
| `/vault-tools:process-inbox` | Classify `Inbox/` files and move to `Notes/` |
| `/vault-tools:auto-categorize` | Turn raw text or a URL into a note |
| `/vault-tools:vault-stats` | Note counts by type, tag, status |
| `/vault-tools:vault-maintenance` | Health checks (orphans, stale drafts, duplicates) |
| `/vault-tools:reclassify` | Suggest better type/tags for a note |
| `/vault-tools:weekly-review` | Weekly activity digest |
| `/vault-tools:import-plans` | Bulk-import existing `~/.claude/plans/` into `Notes/plan/` |

### Hooks

- **SessionStart** — runs two idempotent bootstrappers:
  - `bootstrap-rules.js` copies bundled rule files to `<vault>/.claude/rules/`
  - `bootstrap-symlinks.js` reads optional `<vault>/vault-config.json` and creates host-specific symlinks (junctions on Windows)
- **PostToolUse `Write|Edit`** — `validate-frontmatter.js` checks every `Notes/**/*.md` write against the required frontmatter schema (type, tags, created, status, title, subfolder match).
- **PostToolUse `ExitPlanMode`** — `copy-plan-to-vault.js` archives the most recently modified plan from `~/.claude/plans/` into `Notes/plan/<slug>.md` with `origin: <hostname>` frontmatter for multi-device traceability.

### Rules (bootstrapped on session start)

- **archive-protection** — prevents modification of files under `Archive/`
- **notes-frontmatter** — enforces the required frontmatter schema for `Notes/` files

### Utility scripts

- `migrate-to-subfolders.js` — one-time migration to move legacy top-level `Notes/*.md` into `Notes/<type>/` based on frontmatter.

## Setup

1. Install the plugin from the `claude-depot` marketplace:
   ```
   /plugin install vault-tools@claude-depot
   ```
2. Run `/vault-tools:setup` or go to `/plugin` → **vault-tools** → **Configure options**.
3. Set `vault_path` to your Obsidian vault's absolute path (Linux / WSL2 / Windows all supported).
4. `/reload-plugins` so the env var takes effect.

## Plan Archival

When you call `ExitPlanMode`, the hook writes the plan to `<vault>/Notes/plan/<slug>.md` with frontmatter like:

```yaml
---
title: "Plan Title (from H1)"
type: plan
tags:
  - planning
  - claude-code
origin: spark
plan-file: "mossy-puzzling-bee.md"
session-id: "abc123"
created: 2026-04-22
status: active
---
```

- `origin` — hostname of the machine that produced the plan
- `plan-file` — original filename in `~/.claude/plans/` for traceability
- Idempotent — re-archiving the same plan is a no-op

To import plans you already have locally, run `/vault-tools:import-plans`.

## Vault Requirements

- A `Notes/` directory with `<type>/` subfolders (e.g., `Notes/plan/`, `Notes/note/`, `Notes/guide/`).
- If you use a `CLAUDE.md` schema in the vault, include `plan` in the valid types list so archived plans pass frontmatter validation.

## Cross-Platform

All scripts are pure Node.js stdlib (no bash, jq, or npm dependencies). Works on Linux, WSL2, and Windows. Symlink bootstrap uses junctions on Windows so admin rights are not required.

## Multi-Machine

Each machine archives its own plans independently; Obsidian Sync (or any vault sync tool) propagates them. The `origin` field disambiguates which machine produced each plan.

## Why a Plugin Instead of `.claude/`

Obsidian Sync skips hidden folders, so `.claude/skills/`, `.claude/hooks/`, and `.claude/rules/` wouldn't propagate across machines. This plugin provides those surfaces natively — only machine-specific `settings.local.json` needs to stay under `.claude/`.
