---
name: research-add-items
description: Add more items (research objects) to an existing outline.yaml. Optionally launches a web-search subagent to suggest items in the topic's domain.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, WebFetch, Task, AskUserQuestion, mcp__exa_websearch__web_search_exa, mcp__exa_websearch__web_fetch_exa
---

# Research Add Items — Extend Item List

## Trigger

`/ultra-research:research-add-items`

Manual-only via `disable-model-invocation: true`. Run between `/ultra-research:research` and `/ultra-research:research-deep` whenever the initial item list missed something.

## Pipeline Context

Phase 2a of 5 (optional). Edits `outline.yaml` in place. When finished, Step 4 uses AskUserQuestion to route the user into the next phase (re-run this skill, `/ultra-research:research-add-fields`, or `/ultra-research:research-deep`) with `(Recommended)` annotations based on coverage of the two YAML files.

## Workflow

### Step 1 — Locate Outline

Glob `*/outline.yaml` in the current working directory and read it. If multiple match, ask which.

### Step 2 — Gather Candidate Items (Two Sources in Parallel)

Use AskUserQuestion to ask both:

- "Which items do you want to add? (free-form list)"
- "Run a web search to suggest more items in this domain? (yes/no)"

**⛔ Dispatch-only.** If web search is requested, the orchestrator MUST NOT call `WebSearch`, `WebFetch`, or `mcp__exa_websearch__*` directly. Instead, launch one `web-search-agent` subagent (background, via the harness's `Agent`/`Task` tool) with a prompt asking for additional items in the topic's domain, returning each as `name: short description`. The orchestrator's job is dispatch + read the subagent's structured return, nothing else.

### Step 3 — Merge, Deduplicate, Confirm, Save

- Combine user-named items + web-search suggestions
- Deduplicate by `name` (case-insensitive)
- Show the proposed additions to the user for confirmation
- Append the confirmed items to `outline.yaml` (preserve existing entries) and save

### Step 4 — Inspect Coverage and Route to Next Phase

After saving, Read the updated `outline.yaml` and the sibling `fields.yaml`. Apply the **thinness rubric**:

| Check | Trigger for `(Recommended)` |
|---|---|
| `outline.yaml` items count | Still < 8 items, OR no `category` field used → recommend **Add more items** (run this skill again) |
| `fields.yaml` total fields | < 6 fields, OR only one `field_categories` entry, OR no field with `detail_level: detailed` → recommend **Add more fields** |

If neither file is thin, recommend **Start deep research** instead.

Use AskUserQuestion with `header: "Next step"` and these options (append ` (Recommended)` to the label when the rubric flags it):

- **Add more items** — run `/ultra-research:research-add-items` again
- **Add more fields** — run `/ultra-research:research-add-fields`
- **Start deep research** — run `/ultra-research:research-deep`
- **Done for now** — stop here

In the question body, briefly state *why* each recommendation was made. Invoke the picked skill **immediately** via the Skill tool.

## Output

`{topic}/outline.yaml` updated in place, with the appended items echoed back to the user.
