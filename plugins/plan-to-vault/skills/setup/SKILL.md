---
name: setup
description: >-
  This skill should be used to configure the plan-to-vault plugin for first-time
  use, or when the vault path needs to be changed. Trigger phrases include
  "setup plan-to-vault", "configure plan-to-vault", "set vault path",
  "plan-to-vault setup", or when the SessionStart hook reports that the vault
  path is not configured.
---

# Plan-to-Vault Setup

Guide the user through configuring the plan-to-vault plugin.

## Workflow

1. **Check current state**: Read `$CLAUDE_PLUGIN_OPTION_VAULT_PATH`. If already set, tell the user it's configured and ask if they want to change it.

2. **Auto-detect vaults**: Search common locations for Obsidian vaults:
   ```bash
   find ~/Vaults ~/Documents ~/OneDrive -maxdepth 2 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
   ```
   Present any found vaults as options.

3. **Ask the user** which vault to use, or let them provide a custom path. Verify the path exists and has a `Notes/` directory.

4. **Apply the configuration**: Tell the user to run this exact step:
   > Go to `/plugin` → select **plan-to-vault** → **Configure options** → set `vault_path` to: `<the chosen path>`

   Note: Due to a known Claude Code issue (anthropics/claude-code#39455), plugin options cannot be set programmatically — the user must configure via the plugin menu.

5. **Verify**: After the user confirms they've set it, check `$CLAUDE_PLUGIN_OPTION_VAULT_PATH` again to confirm it's populated. A session restart (`/reload-plugins`) may be needed for the env var to take effect.

6. **Check vault schema**: Verify the vault has `plan` as a valid type by reading the vault's `CLAUDE.md`. If not, warn the user they need to add it.

7. **Offer bulk import**: Ask if the user wants to import existing plans from `~/.claude/plans/` using `/plan-to-vault:import-plans`.
