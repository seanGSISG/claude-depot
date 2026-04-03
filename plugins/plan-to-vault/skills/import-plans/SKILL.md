---
name: import-plans
description: >-
  Bulk import existing Claude Code plan files into the Obsidian vault. Use when
  the user says "import plans", "import existing plans", "bulk import plans",
  "sync old plans", "bring in my plans", or has just installed the plan-to-vault
  plugin and wants to backfill their existing plans.
---

# Import Plans

Bulk import all existing Claude Code plan files from `~/.claude/plans/` into the Obsidian vault as properly formatted notes.

## Workflow

1. Check that the vault path is configured by reading `$CLAUDE_PLUGIN_OPTION_VAULT_PATH`. If empty, tell the user to configure it in their plugin settings.

2. Run the import script:
   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/scripts/bulk-import-plans.js"
   ```

3. Report the results to the user (imported count, skipped duplicates, skipped no-title).

4. If any plans were skipped due to duplicate titles, mention that the user can find and rename them manually in `~/.claude/plans/`.

## What the Script Does

- Reads all `.md` files from `~/.claude/plans/` (excluding agent subplans)
- Extracts the H1 title and converts it to a kebab-case filename
- Wraps the content in vault frontmatter: `type: plan`, `tags: [planning, claude-code]`, `origin: <hostname>`
- Writes to `Notes/<slug>.md` in the vault
- Skips plans that already exist in the vault (idempotent)
