---
name: import-plans
description: >-
  Bulk import existing Claude Code plan files from ~/.claude/plans/ into the
  Obsidian vault. Triggers: "import plans", "bulk import plans", "sync old
  plans", "bring in my plans", "migrate plans", "copy plans to vault", "load
  plans into obsidian".
---

# Import Plans

Bulk import all existing Claude Code plan files from `~/.claude/plans/` into the Obsidian vault as properly formatted notes.

## Workflow

1. Check that the vault path is configured by reading `$CLAUDE_PLUGIN_OPTION_VAULT_PATH`. If empty, tell the user to configure the `vault_path` setting for the plan-to-vault plugin.

2. Run the import script:
   ```bash
   node "${CLAUDE_SKILL_DIR}/../../scripts/bulk-import-plans.js"
   ```

3. The script outputs individual lines for each imported plan (`+ <slug>.md (from <original>.md)`) followed by a summary: `Done. Imported: N, Skipped (duplicate): N, Skipped (no title): N`. Report these counts to the user.

4. If any plans were skipped due to duplicate titles, mention that the user can find and rename them manually in `~/.claude/plans/`.

5. If the script exits with an error (e.g., vault path not found, plans directory missing), report the error message to the user and suggest checking the vault_path configuration.

## What the Script Does

- Reads all `.md` files from `~/.claude/plans/` (excluding agent subplans)
- Extracts the H1 title and converts it to a kebab-case filename
- Wraps the content in vault frontmatter: `type: plan`, `tags: [planning, claude-code]`, `origin: <hostname>`
- Writes to `Notes/plan/<slug>.md` in the vault
- Skips plans that already exist in the vault (idempotent)
