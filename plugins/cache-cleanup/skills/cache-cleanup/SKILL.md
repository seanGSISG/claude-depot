---
name: cache-cleanup
description: >-
  Clean up old cached plugin versions to free disk space. Use when the user
  says "clean cache", "cleanup plugins", "prune old versions", "free disk
  space", "plugin cache", "clear old plugins", or asks about plugin cache
  size.
disable-model-invocation: true
---

# Cache Cleanup

Remove old cached plugin versions from `~/.claude/plugins/cache/`. Claude Code
keeps every version it has ever downloaded — this skill prunes all but the
latest version of each plugin.

## Workflow

1. **Scan (dry-run)**: Always run the script in dry-run mode first:
   ```bash
   node "${CLAUDE_SKILL_DIR}/../../scripts/cleanup.js" --dry-run
   ```

2. **Report**: Show the user the output — which old versions would be removed
   and how much space would be freed. If no old versions are found, tell the
   user the cache is already clean and stop.

3. **Confirm**: Use the `AskUserQuestion` tool with a yes/no question to ask
   the user if they want to proceed with deletion. Do NOT delete without
   explicit confirmation via this tool.

4. **Delete**: Only after the user confirms, run:
   ```bash
   node "${CLAUDE_SKILL_DIR}/../../scripts/cleanup.js" --delete
   ```

5. **Report results**: Show the user what was deleted and total space freed.
