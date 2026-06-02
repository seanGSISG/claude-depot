> Sources: claude-docs-helper.sh, scripts/lookup/manifest.py, scripts/lookup/config.py, scripts/lookup/formatting.py

# Search Guide

This reference explains how to locate documentation, interpret results, and handle edge cases.

**Primary tools (preferred):** Claude Code's built-in **Grep** and **Glob** tools, which
use bundled ripgrep. They run over the live files in `~/.claude-code-docs/docs`, return
compact results, and need no index — so search is always current and token-light.

**Helper script (standalone / fallback):** `~/.claude-code-docs/claude-docs-helper.sh`
provides path search, direct topic reads, and a `--search-content` (ripgrep, with `grep`
fallback) for use outside the agent.

## Table of Contents

- [Content Search](#content-search)
- [Path Search](#path-search)
- [Direct Topic Lookup](#direct-topic-lookup)
- [Direct Document Reading](#direct-document-reading)
- [Filename Conventions](#filename-conventions)
- [Freshness and Updates](#freshness-and-updates)
- [Listing All Docs](#listing-all-docs)
- [Installation Status](#installation-status)
- [Graceful Degradation](#graceful-degradation)

## Content Search

Content search looks inside document text to find relevant pages. Best for questions
and concept lookups. Use the **Grep** tool over `~/.claude-code-docs/docs` (it uses
bundled ripgrep):

- **Candidate files:** `Grep(pattern: "<query>", path: "<docs dir>", output_mode: "files_with_matches")`
- **Rank by relevance:** `output_mode: "count"` — prefer files with more matches.
- **Snippet to disambiguate without opening files:** `output_mode: "content"`, `-C: 2`,
  small `head_limit` (e.g. 20).
- Case-insensitive: `-i: true`. Filter to markdown with `glob: "*.md"` (the mirror is
  all `.md`, so usually unnecessary).

Filenames encode the doc path (see [Filename Conventions](#filename-conventions)), so a
matched filename usually identifies the right doc and its product context directly —
`docs__en__*` / `claude-code__*` are Claude Code CLI; `en__api__*` are the API;
`en__docs__agent-sdk__*` are the Agent SDK. If matches span multiple products, consider
asking the user which they mean (see the category map).

**Standalone fallback (outside the agent):**
```bash
~/.claude-code-docs/claude-docs-helper.sh --search-content "<query>"   # ripgrep, grep fallback
```
This prints the matching doc filenames (most-relevant first), which you then read.

## Path Search

Best for finding specific documents by topic name. Since filenames encode the path, the
fastest approach is the **Glob** tool over `~/.claude-code-docs/docs`:

```
Glob(pattern: "**/*<topic>*.md", path: "<docs dir>")
# e.g. hooks -> claude-code__hooks.md, docs__en__hooks.md
```

**Standalone fallback** — the helper's fuzzy path search over all documented paths (~1,700):

```bash
~/.claude-code-docs/claude-docs-helper.sh --search "<query>"
```

**Output format:** Human-readable with product context:
```
Found 5 results for: 'hooks'

 1. [***] /docs/en/hooks
    Product: Claude Code CLI  |  Score: 70.0
    URL: https://code.claude.com/docs/en/hooks

 2. [***] /docs/en/hooks-guide
    Product: Claude Code CLI  |  Score: 70.0
    URL: https://code.claude.com/docs/en/hooks-guide
```

## Direct Topic Lookup

For known topics, use the helper script's direct topic lookup — the fastest way to read a specific doc:

```bash
# Reads the doc directly and outputs its content
~/.claude-code-docs/claude-docs-helper.sh hooks
~/.claude-code-docs/claude-docs-helper.sh mcp
~/.claude-code-docs/claude-docs-helper.sh skills
```

You can also combine a freshness check with a topic lookup:
```bash
~/.claude-code-docs/claude-docs-helper.sh -t hooks
```

## Direct Document Reading

You can also read documentation files directly by path:

```bash
# Claude Code CLI docs (most common)
cat ~/.claude-code-docs/docs/docs__en__<topic>.md

# Examples
cat ~/.claude-code-docs/docs/docs__en__hooks.md
cat ~/.claude-code-docs/docs/docs__en__mcp.md
cat ~/.claude-code-docs/docs/docs__en__skills.md
cat ~/.claude-code-docs/docs/docs__en__memory.md
```

For platform documentation:
```bash
# API reference
cat ~/.claude-code-docs/docs/en__api__messages__create.md

# Agent SDK
cat ~/.claude-code-docs/docs/en__docs__agent-sdk__overview.md

# Core docs
cat ~/.claude-code-docs/docs/en__docs__build-with-claude__extended-thinking.md

# Prompt engineering
cat ~/.claude-code-docs/docs/en__docs__build-with-claude__prompt-engineering__overview.md
```

## Filename Conventions

Documentation files use double underscores (`__`) to represent path separators:

| URL Path | Filename |
|---|---|
| `/docs/en/hooks` | `docs__en__hooks.md` |
| `/docs/en/sdk/migration-guide` | `docs__en__sdk__migration-guide.md` |
| `/en/api/messages/create` | `en__api__messages__create.md` |
| `/en/docs/agent-sdk/python` | `en__docs__agent-sdk__python.md` |
| `/en/docs/build-with-claude/vision` | `en__docs__build-with-claude__vision.md` |
| `/docs/en/build-with-claude/prompt-engineering/overview` | `docs__en__build-with-claude__prompt-engineering__overview.md` |

**Rules:**
- All lowercase
- Double underscores for path separators
- Hyphens preserved from original URLs
- `.md` extension
- All files in the flat `docs/` directory (no subdirectories)

## Freshness and Updates

```bash
# Check if docs are up-to-date and sync if needed
~/.claude-code-docs/claude-docs-helper.sh -t

# Show recent documentation changes
~/.claude-code-docs/claude-docs-helper.sh "what's new"

# Show Claude Code release notes
~/.claude-code-docs/claude-docs-helper.sh changelog
```

## Listing All Docs

The helper script doesn't have a dedicated `--list` command. Use this fallback:

```bash
ls ~/.claude-code-docs/docs/*.md | sed 's/.*\///' | sed 's/\.md$//'
```

## Installation Status

```bash
~/.claude-code-docs/claude-docs-helper.sh --status
```

Returns installation diagnostics: location, file counts, manifest stats, and whether enhanced features (Python 3.9+, used for path search) are available.

## Graceful Degradation

When the helper script is unavailable:

1. **Direct file reading** always works — use `cat` or the Read tool
2. **Basic search** via grep:
   ```bash
   # Find files mentioning a keyword
   grep -ril "hooks" ~/.claude-code-docs/docs/ | head -20

   # Search within a specific file
   grep -i "configuration" ~/.claude-code-docs/docs/docs__en__hooks.md
   ```
3. **List all docs:**
   ```bash
   ls ~/.claude-code-docs/docs/*.md | sed 's|.*/||; s|\.md$||' | sort
   ```
4. **Check if docs are installed:**
   ```bash
   ls -la ~/.claude-code-docs/docs/ | head -5
   ```
