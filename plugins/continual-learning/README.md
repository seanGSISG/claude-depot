# continual-learning

Hooks that enable Claude Code to learn, reflect, and persist knowledge across sessions via two-tier SQLite memory.

## What It Does

Captures tool usage patterns, mistakes, and preferences during each Claude Code session and stores structured learnings in SQLite databases. On session start, relevant past learnings are surfaced to inform Claude's behavior.

## Architecture

Two-tier memory system:

- **Global** (`~/.claude/learnings.db`) — cross-project learnings (tool preferences, common patterns)
- **Per-repo** (`.claude-memory/learnings.db`) — project-specific learnings (build commands, test patterns, codebase conventions)

## Hook Events

| Event | What It Does | Timeout |
|-------|-------------|---------|
| `SessionStart` | Loads relevant learnings into context | 5s |
| `PostToolUse` | Logs tool invocations for pattern analysis | 3s |
| `PostToolUseFailure` | Captures failed tool uses for mistake detection | 3s |
| `SessionEnd` | Analyzes session, extracts and persists learnings | 10s |

## Learning Categories

The `SessionEnd` analysis covers:
- **Tool insights** — which tools work well for which tasks
- **Mistakes** — errors made and how they were resolved
- **Patterns** — recurring workflows and approaches
- **Preferences** — user's preferred coding style and conventions

## Setup

```
/plugin install continual-learning@claude-depot
```

No configuration required. Databases are auto-initialized on first run.

## Opt-Out

Set `SKIP_CONTINUAL_LEARNING=true` to disable learning for a session.

## Inspecting Learnings

```bash
sqlite3 ~/.claude/learnings.db "SELECT * FROM learnings ORDER BY created_at DESC LIMIT 10;"
```

## Data Retention

- Tool logs: 7 days
- Learnings: 60-day decay (older entries are pruned)
