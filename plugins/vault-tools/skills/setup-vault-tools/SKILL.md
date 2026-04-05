---
name: setup-vault-tools
description: >-
  Configure vault-tools for first-time use or change the vault path. Triggers:
  "setup vault-tools", "configure vault-tools", "set vault path", "install
  vault-tools", "get started with vault-tools", or when vault path is not
  configured.
---

# Vault Tools Setup

Guide the user through configuring the vault-tools plugin.

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

7. **Remind**: This plugin replaces `.claude/skills/`, `.claude/hooks/`, `.claude/rules/` in the vault — they're provided by the plugin on every machine.
