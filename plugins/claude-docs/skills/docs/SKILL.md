---
name: docs
description: "Search and access 573 Anthropic documentation paths covering Claude Code CLI, API, Agent SDK, prompt library, and more. Supports natural language queries, content search, and direct topic lookup. Trigger on: /docs, documentation questions about Claude Code, Claude API, Agent SDK, prompt engineering, MCP, hooks, skills, tool use, streaming, batch processing, extended thinking, or any Anthropic platform feature."
allowed-tools: Bash Read Glob Grep AskUserQuestion
---

## Overview

This skill provides AI-powered search and access to a locally mirrored copy of Anthropic's official documentation. The documentation lives at `~/.claude-code-docs` and covers 573 paths across 6 categories, totaling 571 markdown files.

When a user asks about Anthropic documentation, use the search tools and reference files described below to find the relevant content, read it, and synthesize an answer. Do not guess — always read the actual documentation before answering.

## Domain Concept Map

**Documentation sources:** Two Anthropic domains are mirrored:
- `code.claude.com` — Claude Code CLI documentation (46 pages)
- `platform.claude.com` — Everything else: API, Agent SDK, guides, prompt library (527 pages)

**Six categories** organize all 573 paths:

| Category | User Label | Paths | Covers |
|---|---|---|---|
| `claude_code` | Claude Code CLI | 46 | CLI setup, hooks, skills, MCP, memory, plugins, settings, sub-agents |
| `api_reference` | Claude API | 377 | Messages API, models, batches, files, admin, multi-language SDKs (Python/TS/Go/Java/Kotlin/Ruby) |
| `core_documentation` | Claude Documentation | 82 | Prompt engineering, tool use, vision, streaming, extended thinking, evaluation |
| `prompt_library` | Prompt Library | 65 | Ready-to-use prompt templates |
| `release_notes` | Release Notes | 2 | Version history and system prompts |
| `resources` | Resources | 1 | Additional resources |

**Agent SDK** paths live within `api_reference` but are labeled "Claude Agent SDK" for users. They cover: overview, Python/TypeScript SDKs, sessions, skills, subagents, MCP, plugins, structured outputs, and more.

**File naming convention:** Documentation files use double underscores for path separators:
- `docs__en__hooks.md` — Claude Code CLI page `/docs/en/hooks`
- `en__docs__claude-code__hooks.md` — Alternate format for the same page
- `en__api__messages__create.md` — API reference page `/en/api/messages/create`

## How to Search

Follow this workflow when handling documentation queries:

### Step 1: Analyze Intent

Extract from the user's query:
- **Keywords** — the specific concepts they want (e.g., "hooks", "extended thinking", "batch API")
- **Product context** — if they specify one (e.g., "in the agent sdk", "cli hooks", "api rate limits")
- **Query type** — how-to, reference lookup, comparison, discovery

### Step 2: Run Search

Use the search script at `${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py`:

```bash
# Content search (best for questions and concepts)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --search-content "<keywords>"

# Path search (best for finding specific docs)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --search "<keywords>"
```

If Python 3.9+ is unavailable, fall back to Grep:
```bash
grep -ril "<keyword>" ~/.claude-code-docs/docs/ | head -20
```

See `references/search-guide.md` for detailed search tool usage.

### Step 3: Decide — Synthesize or Ask

Check which product categories the results span:

- **Same category** (e.g., all Claude Code CLI) → **Read all matching docs silently, synthesize a unified answer.** Never ask "which doc do you want?" when results are in the same product context.
- **Multiple categories** (e.g., CLI + API + Agent SDK) → **Ask the user which product context** using AskUserQuestion with user-friendly product labels.

See `references/category-map.md` for the full category-to-label mapping and disambiguation rules.

### Step 4: Read and Present

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
| Freshness check (`-t`) | Run: `cd ~/.claude-code-docs && git fetch --quiet origin main && git rev-list HEAD..origin/main --count` |
| "what's new" | Run: `cd ~/.claude-code-docs && git log --oneline -10 -- docs/*.md` |

## Key Commands Quick Reference

```bash
# Content search (returns JSON with product context)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --search-content "extended thinking"

# Path search (returns ranked path matches)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --search "hooks"

# Direct doc read (fastest for known topics)
cat ~/.claude-code-docs/docs/docs__en__hooks.md

# List all available docs
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --list

# Installation status
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --status

# Check for updates
cd ~/.claude-code-docs && git fetch --quiet origin main && git rev-list HEAD..origin/main --count

# Pull updates
cd ~/.claude-code-docs && git pull --quiet origin main

# Fallback search (no Python)
grep -ril "keyword" ~/.claude-code-docs/docs/ | head -20
```

## Important Caveats

- **Documentation is a mirror, not the source.** Always note that content comes from Anthropic's official documentation. Include official URLs when citing.
- **Two base URLs:** Claude Code CLI pages are at `code.claude.com/docs/en/<page>`. Everything else is at `platform.claude.com/<path>`.
- **Search index required for content search.** If `~/.claude-code-docs/docs/.search_index.json` is missing, content search won't work. Rebuild with: `cd ~/.claude-code-docs && python3 scripts/build_search_index.py`
- **Python 3.9+ is optional.** The search script requires it, but documentation can still be read directly or searched with grep.
- **571 files, 573 manifest paths.** Two paths in the manifest may not have corresponding files (expected — they are tracked but not downloadable).
