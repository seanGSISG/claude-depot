---
name: setup-vault-tools
description: >-
  Configure vault-tools for first-time use or change the vault path. Covers
  both note management and plan archival. Triggers: "setup vault-tools",
  "configure vault-tools", "set vault path", "install vault-tools", "get
  started with vault-tools", "setup plan archival", or when vault path is not
  configured.
---

# Vault Tools Setup

Guide the user through configuring the vault-tools plugin. This covers both vault management (notes, search, maintenance) and automatic plan archival on `ExitPlanMode`.

## Workflow

1. **Check current state**: Read `$CLAUDE_PLUGIN_OPTION_VAULT_PATH`. If already set, tell the user and ask if they want to change it.

2. **Auto-detect vaults**: Search common locations:
   ```bash
   find ~/Vaults ~/Documents ~/OneDrive -maxdepth 2 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
   ```
   Present found vaults as options.

3. **Ask the user** which vault to use, or let them provide a custom path. Verify the path exists and has a `Notes/` directory with type subfolders.

4. **Apply**: Tell the user to run:
   > Go to `/plugin` → select **vault-tools** → **Configure options** → set `vault_path` to: `<chosen path>`

   Note: Plugin options cannot be set programmatically — the user must configure via the plugin menu.

5. **Verify**: After user confirms, check `$CLAUDE_PLUGIN_OPTION_VAULT_PATH`. A `/reload-plugins` may be needed.

6. **Confirm rules bootstrapping**: Check `.claude/rules/` in vault for expected rule files.

7. **Plan archival setup**: Verify `Notes/plan/` exists in the vault (the archival hook creates it if missing, but confirm now so the user knows where plans will land). If the vault has a `CLAUDE.md` defining valid note types, check that `plan` is in the list — warn the user to add it if missing, otherwise the frontmatter validator will flag every archived plan.

8. **Offer bulk import**: Ask whether the user wants to import any existing plans from `~/.claude/plans/` into the vault via `/vault-tools:import-plans`. Skip if `~/.claude/plans/` is empty.

9. **Remind**: This plugin replaces `.claude/skills/`, `.claude/hooks/`, `.claude/rules/` in the vault — they're provided by the plugin on every machine. The `ExitPlanMode` hook archives new plans automatically once `vault_path` is set.
