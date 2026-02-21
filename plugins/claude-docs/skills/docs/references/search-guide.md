> Sources: scripts/lookup/search.py, scripts/lookup/manifest.py, scripts/lookup/config.py, scripts/lookup/formatting.py, scripts/build_search_index.py

# Search Guide

This reference explains how to use the documentation search tools, interpret results, and handle edge cases.

## Table of Contents

- [Content Search](#content-search)
- [Path Search](#path-search)
- [Direct Document Reading](#direct-document-reading)
- [Filename Conventions](#filename-conventions)
- [Search Output Formats](#search-output-formats)
- [Graceful Degradation](#graceful-degradation)
- [Rebuilding the Search Index](#rebuilding-the-search-index)

## Content Search

Content search looks inside document text (titles, keywords, previews) to find relevant pages. Best for questions and concept lookups.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --search-content "<query>"
```

**How scoring works:**
- Title match: +100 points
- Keyword match: +10 per matching word
- Preview match: +20 points
- Exact word in keywords: +5 bonus per word

**Output format:** JSON with product context:
```json
{
  "query": "hooks",
  "total_results": 5,
  "results": [
    {
      "path": "/docs/en/hooks",
      "title": "Hooks",
      "category": "claude_code",
      "product": "Claude Code CLI",
      "score": 115,
      "preview": "Hooks allow you to...",
      "keywords": ["hooks", "pretooluse", "posttooluse"],
      "file": "docs/docs__en__hooks.md"
    }
  ],
  "product_summary": {"Claude Code CLI": 3, "Claude Agent SDK": 2},
  "unique_products": 2
}
```

**Key fields for AI routing:**
- `product_summary` — quickly see which product contexts are represented
- `unique_products` — if 1, synthesize directly; if >1, consider asking the user
- `file` — use this path to read the actual document content

## Path Search

Path search uses fuzzy matching against the 573 documented paths. Best for finding specific documents by topic name.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/search-docs.py --search "<query>"
```

**How scoring works:**
- Exact match: 100%
- Substring at path start: 80%
- Substring in last path segment: 70%
- Substring elsewhere: 60%
- Word matches: 40% scaled by match ratio
- Character similarity fallback: up to 30%

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

## Direct Document Reading

For known topics, skip search and read directly:

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
| `/en/resources/prompt-library/code-clarifier` | `en__resources__prompt-library__code-clarifier.md` |

**Rules:**
- All lowercase
- Double underscores for path separators
- Hyphens preserved from original URLs
- `.md` extension
- All files in the flat `docs/` directory (no subdirectories)

## Search Output Formats

### Content search (--search-content)

Returns JSON to stdout. Parse the `results` array for document paths and scores. The `product_summary` object shows how results distribute across products — use this to decide whether to synthesize or ask for disambiguation.

### Path search (--search)

Returns human-readable text to stdout. Each result includes the path, product label, relevance score, and official URL.

### List (--list)

Returns a simple text list of all documentation file stems (filenames without `.md`).

### Status (--status)

Returns installation diagnostics: location, file counts, manifest stats, index status.

## Graceful Degradation

When Python 3.9+ is not available:

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

## Rebuilding the Search Index

The search index powers `--search-content`. If it's missing or stale:

```bash
cd ~/.claude-code-docs && python3 scripts/build_search_index.py
```

This reads all markdown files in `docs/`, extracts titles, keywords, and previews, and writes `docs/.search_index.json`. The SessionStart hook rebuilds this automatically after pulling updates.
