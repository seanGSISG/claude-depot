---
name: docs
description: "Search and access Anthropic documentation covering Claude Code CLI, API, Agent SDK, and more. Supports natural language queries, content search, and direct topic lookup. Trigger on: /docs, documentation questions about Claude Code, Claude API, Agent SDK, prompt engineering, MCP, hooks, skills, tool use, streaming, batch processing, extended thinking, or any Anthropic platform feature."
allowed-tools: Bash Read Glob Grep AskUserQuestion
---

## Overview

This skill provides AI-powered search and access to a locally mirrored copy of Anthropic's official documentation. The documentation lives at `~/.claude-code-docs` and covers ~1,700 paths across four categories.

When a user asks about Anthropic documentation, use the search tools and reference files described below to find the relevant content, read it, and synthesize an answer. Do not guess — always read the actual documentation before answering.

## Domain Concept Map

**Documentation sources:** Two Anthropic domains are mirrored:
- `code.claude.com` — Claude Code CLI documentation
- `platform.claude.com` — Everything else: API, Agent SDK, guides

**Four categories** organize the paths (approximate counts as of 2026-06):

| Category | User Label | Paths | Covers |
|---|---|---|---|
| `claude_code` | Claude Code CLI | ~43 | CLI setup, hooks, skills, MCP, memory, plugins, settings, sub-agents |
| `api_reference` | Claude API | ~1,460 | Messages API, models, batches, files, admin, multi-language SDKs (Python/TS/Go/Java/Kotlin/Ruby), Agent SDK |
| `core_documentation` | Claude Documentation | ~200 | Prompt engineering, tool use, vision, streaming, extended thinking, evaluation, release notes, resources |
| `uncategorized` | Other | ~1 | Paths not yet assigned to a category |

**Agent SDK** paths live within `api_reference` but are labeled "Claude Agent SDK" for users. They cover: overview, Python/TypeScript SDKs, sessions, skills, subagents, MCP, plugins, structured outputs, and more.

**File naming convention:** Documentation files use double underscores for path separators:
- `docs__en__hooks.md` — Claude Code CLI page `/docs/en/hooks`
- `en__docs__claude-code__hooks.md` — Alternate format for the same page
- `en__api__messages__create.md` — API reference page `/en/api/messages/create`

## How to Search

Follow this workflow when handling documentation queries:

### Step 1: Sync the latest docs (MANDATORY — always do this first)

Before searching or reading anything, pull the latest documentation. This is the
first action for **every** docs request — it guarantees fresh content and a current
search index, and clones the mirror on first use. Run exactly this:

```bash
DOCS="$HOME/.claude-code-docs"
if [ -d "$DOCS/.git" ]; then
  pre=$(git -C "$DOCS" rev-parse HEAD 2>/dev/null || echo none)
  git -C "$DOCS" pull --ff-only --quiet 2>/dev/null || true
  post=$(git -C "$DOCS" rev-parse HEAD 2>/dev/null || echo none)
else
  git clone --quiet https://github.com/seanGSISG/claude-code-docs.git "$DOCS" && pre=none && post=new
fi
# Refresh the runtime helper from tracked source
if [ -f "$DOCS/scripts/claude-docs-helper.sh" ]; then
  cp "$DOCS/scripts/claude-docs-helper.sh" "$DOCS/claude-docs-helper.sh" 2>/dev/null || true
  chmod +x "$DOCS/claude-docs-helper.sh" 2>/dev/null || true
fi
# Rebuild the search index only when docs changed or the index is missing
if [ "$pre" != "$post" ] || [ ! -f "$DOCS/docs/.search_index.json" ]; then
  for py in python3 python; do command -v "$py" >/dev/null 2>&1 && { (cd "$DOCS" && "$py" scripts/build_search_index.py >/dev/null 2>&1); break; }; done
fi
echo "Docs ready: $(find "$DOCS/docs" -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files"
```

Proceed to the next step regardless of the sync result — if the network is down,
the existing local mirror is still usable.

### Step 2: Analyze Intent

Extract from the user's query:
- **Keywords** — the specific concepts they want (e.g., "hooks", "extended thinking", "batch API")
- **Product context** — if they specify one (e.g., "in the agent sdk", "cli hooks", "api rate limits")
- **Query type** — how-to, reference lookup, comparison, discovery

### Step 3: Run Search

Use the upstream helper script at `~/.claude-code-docs/claude-docs-helper.sh`:

```bash
# Content search (best for questions and concepts)
~/.claude-code-docs/claude-docs-helper.sh --search-content "<keywords>"

# Path search (best for finding specific docs)
~/.claude-code-docs/claude-docs-helper.sh --search "<keywords>"

# Direct topic lookup (fastest for known topics)
~/.claude-code-docs/claude-docs-helper.sh <topic>
```

If the helper script is unavailable, fall back to Grep:
```bash
grep -ril "<keyword>" ~/.claude-code-docs/docs/ | head -20
```

See `references/search-guide.md` for detailed search tool usage.

### Step 4: Decide — Synthesize or Ask

Check which product categories the results span:

- **Same category** (e.g., all Claude Code CLI) → **Read all matching docs silently, synthesize a unified answer.** Never ask "which doc do you want?" when results are in the same product context.
- **Multiple categories** (e.g., CLI + API + Agent SDK) → **Ask the user which product context** using AskUserQuestion with user-friendly product labels.

See `references/category-map.md` for the full category-to-label mapping and disambiguation rules.

### Step 5: Read and Present

1. Read the matching documentation files using their file paths from the search results
2. Extract sections relevant to the user's question
3. Synthesize a unified answer combining insights from all sources
4. Cite all sources at the end with official documentation URLs

## Reference Navigation

Load the reference file matching the topic before answering detailed questions about search mechanics or category routing.

| Topic | Reference File | Key Contents |
|---|---|---|
| How to use search tools, filename conventions, Python fallback, direct doc reading | `references/search-guide.md` | Search commands, output formats, file naming patterns, graceful degradation |
| Product categories, user-facing labels, disambiguation rules, when to ask vs synthesize | `references/category-map.md` | Category-to-label map, path patterns, cross-context resolution strategy |

## Cross-Reference Guide

Some queries span multiple reference files or require special handling:

| Question Pattern | Action |
|---|---|
| "How do I use X in agent sdk?" | Filter search to agent-sdk paths, read all matches, synthesize |
| "What's the difference between X and Y?" | Search for both terms, read docs for each, present comparison |
| "Show me all docs about X" | Run path search, present grouped by product category |
| "hooks" (ambiguous — CLI hooks vs Agent SDK hooks) | Search content, check categories — if split across products, ask user |
| Direct topic name (e.g., "mcp", "memory") | Try direct file read first: `~/.claude-code-docs/docs/docs__en__<topic>.md` |
| Freshness check (`-t`) | Run: `~/.claude-code-docs/claude-docs-helper.sh -t` |
| "what's new" | Run: `~/.claude-code-docs/claude-docs-helper.sh "what's new"` |
| "update the docs" / "pull latest docs" | Run the **Step 1** sync block above (or tell the user to run the `/docs-update` command, which does the same thing). |

## Keeping Docs Current

There is no background hook — syncing is explicit and always visible. The mirror is
refreshed by the mandatory **Step 1** sync block at the start of this workflow, so
every docs request pulls the latest content and rebuilds the index when it changed.
The **`/docs-update`** command runs the same sync on demand without a search.

## Key Commands Quick Reference

```bash
# Content search (returns JSON with product context)
~/.claude-code-docs/claude-docs-helper.sh --search-content "extended thinking"

# Path search (returns ranked path matches)
~/.claude-code-docs/claude-docs-helper.sh --search "hooks"

# Direct topic lookup
~/.claude-code-docs/claude-docs-helper.sh hooks

# List all available docs
ls ~/.claude-code-docs/docs/*.md | sed 's/.*\///' | sed 's/\.md$//'

# Check freshness and sync
~/.claude-code-docs/claude-docs-helper.sh -t

# What's new
~/.claude-code-docs/claude-docs-helper.sh "what's new"

# Installation status
~/.claude-code-docs/claude-docs-helper.sh --status

# Fallback search (no helper script)
grep -ril "keyword" ~/.claude-code-docs/docs/ | head -20
```

## Important Caveats

- **Documentation is a mirror, not the source.** Always note that content comes from Anthropic's official documentation. Include official URLs when citing.
- **Two base URLs:** Claude Code CLI pages are at `code.claude.com/docs/en/<page>`. Everything else is at `platform.claude.com/<path>`.
- **Search index required for content search.** If `~/.claude-code-docs/docs/.search_index.json` is missing, content search won't work. Rebuild with: `cd ~/.claude-code-docs && python3 scripts/build_search_index.py`
- **Helper script requires Python 3.9+ for enhanced features.** Basic topic lookup and freshness checks work without Python. Content and path search need Python.
- **~1,530 files, ~1,702 manifest paths.** The manifest tracks more paths than there are files; some are tracked but not downloadable (expected). Exact counts grow as Anthropic publishes docs — run `~/.claude-code-docs/claude-docs-helper.sh --status` for live numbers.
