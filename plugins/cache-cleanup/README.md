# cache-cleanup

Prune old cached plugin versions from `~/.claude/plugins/cache/` to free disk space.

Claude Code caches every version of every installed plugin but never garbage collects old ones ([anthropics/claude-code#36245](https://github.com/anthropics/claude-code/issues/36245)). Over time this leads to unbounded cache growth — one user reported 1.2 GB of dead cache from a single plugin.

## Install

```
/plugin marketplace add seanGSISG/claude-depot
/plugin install cache-cleanup@claude-depot
```

## Usage

```
/cache-cleanup:cache-cleanup
```

The skill runs a dry-run scan first, shows you exactly what would be deleted and how much space would be freed, then asks for confirmation before removing anything.

### What it cleans

- **Old plugin versions**: For each plugin with multiple cached versions, keeps only the latest and removes the rest
- **Orphaned temp directories**: `temp_local_*` and `temp_git_*` directories left behind by interrupted installs

### What it never touches

- The latest (active) version of any plugin
- `~/.claude/plugins/data/` (persistent plugin state that survives updates)

## Manual usage

The cleanup script can also be run directly without Claude Code:

```bash
# Preview what would be deleted
node ~/.claude/plugins/cache/claude-depot/cache-cleanup/1.0.2/scripts/cleanup.js

# Actually delete (no confirmation prompt)
node ~/.claude/plugins/cache/claude-depot/cache-cleanup/1.0.2/scripts/cleanup.js --delete
```

## Requirements

- Node.js (bundled with Claude Code)
- No external dependencies — uses only built-in `fs`, `path`, and `os` modules
- Cross-platform: macOS, Linux, Windows
