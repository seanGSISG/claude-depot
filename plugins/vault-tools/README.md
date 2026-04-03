# vault-tools

Vault-specific skills, rules, and hooks for the MyVault Obsidian knowledge base. Install this plugin on any machine to get the full vault management experience — no need to sync `.claude/` hidden folders.

## What's Included

### Skills (8)

| Skill | Purpose |
|-------|---------|
| `/new-note` | Create a note with proper frontmatter |
| `/vault-search` | Natural language search across vault |
| `/process-inbox` | Classify Inbox/ files and move to Notes/ |
| `/auto-categorize` | Turn raw text or URL into a note |
| `/vault-stats` | Note counts by type, tag, status |
| `/vault-maintenance` | Health checks (orphans, stale drafts, duplicates) |
| `/reclassify` | Suggest better type/tags for a note |
| `/weekly-review` | Weekly activity digest |

### Hooks

- **PostToolUse (Write|Edit)**: Validates YAML frontmatter for files written to `Notes/`. Checks type, tags, created, status, and title fields.
- **SessionStart**: Bootstraps `.claude/rules/` with bundled rule files (archive protection + frontmatter requirements).

### Rules (bootstrapped on session start)

- **archive-protection**: Prevents modification of files in `Archive/`
- **notes-frontmatter**: Enforces the required frontmatter schema for `Notes/` files

## Setup

1. Install the plugin from the claude-depot marketplace
2. Run `/vault-tools:setup` or go to `/plugin` → vault-tools → Configure options
3. Set `vault_path` to your Obsidian vault's absolute path
4. Restart the session (`/reload-plugins`) for the configuration to take effect

## How It Works

This plugin replaces the need for project-level `.claude/skills/`, `.claude/hooks/`, and `.claude/rules/` in your vault. Since Obsidian Sync skips hidden folders, those files wouldn't propagate to other machines. Instead, this plugin:

- Provides all skills natively (auto-discovered by Claude Code)
- Registers the validation hook via `hooks.json`
- Copies rule files to `.claude/rules/` on each session start

The only thing that stays in `.claude/` is `settings.local.json` with machine-specific permissions (MCP tool allowlists).
