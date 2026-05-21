---
name: research-add-fields
description: Add more field definitions to an existing fields.yaml. Source new fields from user input or from a web-search subagent suggesting common fields in the domain.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, WebFetch, Task, AskUserQuestion, mcp__exa_websearch__web_search_exa, mcp__exa_websearch__web_fetch_exa
---

# Research Add Fields — Extend Field Definitions

## Trigger

`/ultra-research:research-add-fields`

Manual-only via `disable-model-invocation: true`. Run between `/ultra-research:research` and `/ultra-research:research-deep` to enrich the schema the deep-research subagents will populate.

## Pipeline Context

Phase 2b of 5 (optional). Edits `fields.yaml` in place. When finished, Step 4 uses AskUserQuestion to route the user into the next phase (re-run this skill, `/ultra-research:research-add-items`, or `/ultra-research:research-deep`) with `(Recommended)` annotations based on coverage of the two YAML files.

## Workflow

### Step 1 — Locate Fields File

Glob `*/fields.yaml` in the current working directory and read it. If multiple match, ask which.

### Step 2 — Pick Supplement Source

Use AskUserQuestion with two options:

- **A. User input** — user lists field names + descriptions directly
- **B. Web search** — see dispatch rule below

**⛔ Dispatch-only.** If the user picks B (web search), the orchestrator MUST NOT call `WebSearch`, `WebFetch`, or `mcp__exa_websearch__*` directly. Instead, launch one `web-search-agent` subagent (background, via the harness's `Agent`/`Task` tool) with a prompt asking it to propose common fields used in this domain (e.g. for "AI coding tools", fields like `context_window`, `benchmark_scores`, `pricing_tiers`). The orchestrator's job is dispatch + read the subagent's structured return, nothing else.

### Step 3 — Confirm, Categorize, Save

- Show the proposed new fields to the user
- For each confirmed field, ask the user which `category` it belongs to (offer existing categories from `fields.yaml` plus "create new") and which `detail_level` (`brief`, `moderate`, `detailed`)
- Append to `fields.yaml` under the chosen category, preserving existing entries

### Step 4 — Inspect Coverage and Route to Next Phase

After saving, Read the updated `fields.yaml` and the sibling `outline.yaml`. Apply the **thinness rubric**:

| Check | Trigger for `(Recommended)` |
|---|---|
| `fields.yaml` total fields | Still < 6 fields, OR only one `field_categories` entry, OR no field with `detail_level: detailed` → recommend **Add more fields** (run this skill again) |
| `outline.yaml` items count | < 8 items, OR no `category` field used → recommend **Add more items** |

If neither file is thin, recommend **Start deep research** instead.

Use AskUserQuestion with `header: "Next step"` and these options (append ` (Recommended)` to the label when the rubric flags it):

- **Add more items** — run `/ultra-research:research-add-items`
- **Add more fields** — run `/ultra-research:research-add-fields` again
- **Start deep research** — run `/ultra-research:research-deep`
- **Done for now** — stop here

In the question body, briefly state *why* each recommendation was made. Invoke the picked skill **immediately** via the Skill tool.

## Output

`{topic}/fields.yaml` updated in place, with the appended fields echoed back to the user.
