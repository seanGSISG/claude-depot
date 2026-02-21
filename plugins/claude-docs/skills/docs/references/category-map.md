> Sources: scripts/lookup/manifest.py, scripts/lookup/config.py, paths_manifest.json, CLAUDE.md

# Category Map

This reference defines the product categories, user-facing labels, path patterns, and disambiguation rules for routing documentation queries.

## Table of Contents

- [Category-to-Label Mapping](#category-to-label-mapping)
- [Path Patterns by Category](#path-patterns-by-category)
- [Base URLs](#base-urls)
- [Disambiguation Strategy](#disambiguation-strategy)
- [Common Ambiguous Terms](#common-ambiguous-terms)

## Category-to-Label Mapping

Always use the **user-facing label** when presenting options to users. Users think in product names, not internal category identifiers.

| Internal Category | User-Facing Label | Path Count | Description |
|---|---|---|---|
| `claude_code` | Claude Code CLI | 46 | CLI installation, configuration, hooks, skills, MCP, memory, plugins |
| `api_reference` | Claude API | 377 | Messages API, admin API, models, batches, files, multi-language SDKs |
| `api_reference` (agent-sdk subset) | Claude Agent SDK | 18 | Agent SDK overview, Python/TS, sessions, skills, subagents, MCP, plugins |
| `core_documentation` | Claude Documentation | 82 | Prompt engineering, tool use, vision, streaming, evaluation, guides |
| `prompt_library` | Prompt Library | 65 | Ready-to-use prompt templates for various tasks |
| `release_notes` | Release Notes | 2 | Version history and system prompts |
| `resources` | Resources | 1 | Additional resources overview |

**Special case:** Agent SDK paths (`/docs/en/agent-sdk/*`) are stored under `api_reference` but should be labeled "Claude Agent SDK" for users. The `get_product_label()` function handles this automatically.

## Path Patterns by Category

### Claude Code CLI (`claude_code`)

Pattern: `/docs/en/<page-name>`

All 46 pages are single-segment paths under `/docs/en/`:
```
/docs/en/hooks          /docs/en/mcp            /docs/en/memory
/docs/en/skills         /docs/en/plugins        /docs/en/settings
/docs/en/sub-agents     /docs/en/hooks-guide    /docs/en/cli-reference
/docs/en/setup          /docs/en/quickstart     /docs/en/overview
/docs/en/sandboxing     /docs/en/security       /docs/en/costs
```

Exception: `/docs/en/sdk/migration-guide` (nested path).

### Claude API (`api_reference`)

Pattern: `/docs/en/api/<section>/<action>` and `/docs/en/api/<language>/<section>/<action>`

Includes multi-language SDK docs:
```
/docs/en/api/messages/create          (default/curl)
/docs/en/api/python/messages/create   (Python SDK)
/docs/en/api/typescript/messages/create
/docs/en/api/go/messages/create
/docs/en/api/java/messages/create
/docs/en/api/kotlin/messages/create
/docs/en/api/ruby/messages/create
```

### Claude Agent SDK (subset of `api_reference`)

Pattern: `/docs/en/agent-sdk/<topic>`

```
/docs/en/agent-sdk/overview       /docs/en/agent-sdk/python
/docs/en/agent-sdk/typescript     /docs/en/agent-sdk/sessions
/docs/en/agent-sdk/skills         /docs/en/agent-sdk/subagents
/docs/en/agent-sdk/mcp            /docs/en/agent-sdk/plugins
/docs/en/agent-sdk/structured-outputs
/docs/en/agent-sdk/custom-tools
/docs/en/agent-sdk/permissions
/docs/en/agent-sdk/hosting
/docs/en/agent-sdk/cost-tracking
/docs/en/agent-sdk/streaming-vs-single-mode
/docs/en/agent-sdk/modifying-system-prompts
/docs/en/agent-sdk/slash-commands
/docs/en/agent-sdk/todo-tracking
/docs/en/agent-sdk/migration-guide
```

### Claude Documentation (`core_documentation`)

Pattern: `/docs/en/<section>/<topic>` (multi-segment paths)

Sections include:
- `/docs/en/build-with-claude/*` — Guides on streaming, caching, vision, files, etc.
- `/docs/en/build-with-claude/prompt-engineering/*` — Prompt engineering techniques
- `/docs/en/about-claude/*` — Models, pricing, use case guides
- `/docs/en/agents-and-tools/*` — Tool use, MCP, computer use, agent skills
- `/docs/en/test-and-evaluate/*` — Testing, guardrails, evaluation
- `/docs/en/get-started`, `/docs/en/intro` — Getting started guides

### Prompt Library (`prompt_library`)

Pattern: `/docs/en/resources/prompt-library/<template-name>`

65 prompt templates (e.g., `code-clarifier`, `sql-sorcerer`, `python-bug-buster`).

### Release Notes (`release_notes`)

Pattern: `/docs/en/release-notes/<topic>`

Two paths: `overview` and `system-prompts`.

## Base URLs

Documentation is split across two domains. The correct base URL depends on the page:

| Domain | Base URL | Pages |
|---|---|---|
| Claude Code CLI | `https://code.claude.com` | 46 known CLI pages + `sdk/migration-guide` |
| Everything else | `https://platform.claude.com` | All other 527 paths |

To construct an official link:
- CLI page `/docs/en/hooks` → `https://code.claude.com/docs/en/hooks`
- API page `/docs/en/api/messages/create` → `https://platform.claude.com/docs/en/api/messages/create`
- Agent SDK page `/docs/en/agent-sdk/python` → `https://platform.claude.com/docs/en/agent-sdk/python`

## Disambiguation Strategy

### When to Synthesize (default)

**Synthesize** when all search results fall within the same product context:

- All results are Claude Code CLI → Read all, synthesize unified answer
- All results are Claude API → Read all, synthesize
- All results are Claude Agent SDK → Read all, synthesize
- All results are Claude Documentation → Read all, synthesize

This is the most common case. Never ask "which document do you want?" when results are in the same product.

### When to Ask

**Ask** only when results span fundamentally different product contexts with incompatible workflows:

Example: User asks about "skills"
- Claude Code CLI has `/docs/en/skills` (installing/running skills locally)
- Claude Agent SDK has `/docs/en/agent-sdk/skills` (building agent capabilities)
- Claude API has `/docs/en/api/beta/skills/*` (API endpoints for skill management)

These are different products with different workflows. Ask:

```
Skills exist in different Claude products:

1. Claude Code CLI — Install and run pre-built skills locally
2. Claude Agent SDK — Build custom agent capabilities in Python/TypeScript
3. Claude API — Programmatic skill management endpoints

Which are you working with?
```

### Context Clues

Before asking, check if the query contains context clues that resolve ambiguity:

| Clue in Query | Route To |
|---|---|
| "cli", "command line", "terminal" | Claude Code CLI |
| "agent sdk", "agent framework" | Claude Agent SDK |
| "api", "endpoint", "request", "curl" | Claude API |
| "prompt engineering", "best practices" | Claude Documentation |
| "in my project", "in my code" | Likely Claude Code CLI |
| Language-specific ("python sdk", "typescript") | Check both Agent SDK and API SDK docs |

## Common Ambiguous Terms

These terms appear in multiple product contexts. Use context clues or ask:

| Term | CLI | Agent SDK | API | Documentation |
|---|---|---|---|---|
| hooks | `/docs/en/hooks` | — | — | — |
| skills | `/docs/en/skills` | `/docs/en/agent-sdk/skills` | `/docs/en/api/beta/skills/*` | `/docs/en/build-with-claude/skills-guide` |
| mcp | `/docs/en/mcp` | `/docs/en/agent-sdk/mcp` | — | `/docs/en/agents-and-tools/mcp-connector` |
| plugins | `/docs/en/plugins` | `/docs/en/agent-sdk/plugins` | — | — |
| memory | `/docs/en/memory` | — | — | `/docs/en/agents-and-tools/tool-use/memory-tool` |
| sub-agents | `/docs/en/sub-agents` | `/docs/en/agent-sdk/subagents` | — | — |
| slash-commands | `/docs/en/slash-commands` | `/docs/en/agent-sdk/slash-commands` | — | — |
| streaming | — | `/docs/en/agent-sdk/streaming-vs-single-mode` | — | `/docs/en/build-with-claude/streaming` |
| structured-outputs | — | `/docs/en/agent-sdk/structured-outputs` | — | `/docs/en/build-with-claude/structured-outputs` |
| tool use | — | `/docs/en/agent-sdk/custom-tools` | — | `/docs/en/agents-and-tools/tool-use/overview` |
