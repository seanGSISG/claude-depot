---
name: setup-vault-tools
description: >-
  Configure vault-tools for first-time use, or when the vault path needs
  to be changed. Trigger phrases include "setup vault-tools",
  "configure vault-tools", "set vault path for vault-tools", or when the
  SessionStart hook reports that the vault path is not configured.
---

# Vault Tools Setup

Guide the user through configuring the vault-tools plugin.

## Workflow

1. **Check current state**: Read `$CLAUDE_PLUGIN_OPTION_VAULT_PATH`. If already set, tell the user it's configured and ask if they want to change it.

2. **Auto-detect vaults**: Search common locations for Obsidian vaults:
   ```bash
   find ~/Vaults ~/Documents ~/OneDrive -maxdepth 2 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
   ```
   Present any found vaults as options.

3. **Ask the user** which vault to use, or let them provide a custom path. Verify the path exists and has a `Notes/` directory.

4. **Apply the configuration**: Tell the user to run this exact step:
   > Go to `/plugin` → select **vault-tools** → **Configure options** → set `vault_path` to: `<the chosen path>`

   Note: Due to a known Claude Code issue (anthropics/claude-code#39455), plugin options cannot be set programmatically — the user must configure via the plugin menu.

5. **Verify**: After the user confirms they've set it, check `$CLAUDE_PLUGIN_OPTION_VAULT_PATH` again to confirm it's populated. A session restart (`/reload-plugins`) may be needed for the env var to take effect.

6. **Confirm rules bootstrapping**: Check if `.claude/rules/` exists in the vault with the expected rule files (archive-protection.md, notes-frontmatter.md). If missing, explain that they will be created on next session start.

7. **Recommend Obsidian Sync check**: Remind the user that this plugin replaces the need for `.claude/skills/`, `.claude/hooks/`, and `.claude/rules/` in the vault's hidden folder. These will be provided by the plugin on every machine where it's installed.
