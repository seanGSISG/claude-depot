---
name: research-add-fields
description: Add more field definitions to an existing fields.yaml. Source new fields from user input or from a web-search subagent suggesting common fields in the domain.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Add Fields — Extend Field Definitions

## Trigger

`/research-add-fields`

Manual-only via `disable-model-invocation: true`. Run between `/research` and `/research-deep` to enrich the schema the deep-research subagents will populate.

## Pipeline Context

Phase 2b of 5 (optional). Edits `fields.yaml` in place. Does not chain — when finished, the user decides whether to iterate further (`/research-add-items`) or move on (`/research-deep`).

## Workflow

### Step 1 — Locate Fields File

Glob `*/fields.yaml` in the current working directory and read it. If multiple match, ask which.

### Step 2 — Pick Supplement Source

Use AskUserQuestion with two options:

- **A. User input** — user lists field names + descriptions directly
- **B. Web search** — launch a `web-search-agent` subagent to propose common fields used in this domain (e.g. for "AI coding tools", fields like `context_window`, `benchmark_scores`, `pricing_tiers`)

### Step 3 — Confirm, Categorize, Save

- Show the proposed new fields to the user
- For each confirmed field, ask the user which `category` it belongs to (offer existing categories from `fields.yaml` plus "create new") and which `detail_level` (`brief`, `moderate`, `detailed`)
- Append to `fields.yaml` under the chosen category, preserving existing entries

## Output

`{topic}/fields.yaml` updated in place, with the appended fields echoed back to the user.
