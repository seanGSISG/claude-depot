# plan-to-vault

Automatically archive Claude Code plan files to an Obsidian vault when exiting plan mode. Each plan is labeled with the originating machine's hostname, so plans from multiple devices are browsable in one place.

## How It Works

A `PostToolUse` hook fires on `ExitPlanMode`. It finds the most recently modified plan file in `~/.claude/plans/`, wraps it in Obsidian-compatible YAML frontmatter (`type: plan`, `origin: <hostname>`, etc.), and writes it to your vault's `Notes/` directory.

## Setup

1. Install the plugin:
   ```
   /plugin install plan-to-vault@claude-depot
   ```

2. Configure your vault path when prompted (or set it manually in plugin settings):
   - Linux: `/home/user/Vaults/MyVault`
   - WSL2: `/mnt/c/Users/user/Vaults/MyVault`
   - Windows: `C:\Users\user\Vaults\MyVault`

3. Ensure your vault has `plan` as a valid note type (see Vault Requirements below).

## Vault Requirements

Your Obsidian vault needs:

- A `Notes/` directory where plan notes are written
- `plan` added as a valid type in your vault's schema/validation
- Optionally, a Bases view filtering `type == "plan"` for browsing plans

## Bulk Import

To import existing plans from `~/.claude/plans/`:

```
/plan-to-vault:import-plans
```

## Frontmatter

Each archived plan gets this frontmatter:

```yaml
---
title: "Plan Title (from H1)"
type: plan
tags:
  - planning
  - claude-code
origin: spark
plan-file: "mossy-puzzling-bee.md"
created: 2026-04-02
status: active
---
```

- `origin` — machine hostname, for multi-device tracking
- `plan-file` — original filename in `~/.claude/plans/` for traceability

## Cross-Platform

Scripts are pure Node.js (no bash, no jq, no npm dependencies). Works on Linux, WSL2, and Windows.

## Multi-Machine

Each machine independently archives its plans. Obsidian Sync (or any vault sync tool) propagates the notes. The `origin` field disambiguates which machine produced each plan.
