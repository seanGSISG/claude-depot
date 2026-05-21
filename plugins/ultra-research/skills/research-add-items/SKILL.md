---
name: research-add-items
description: Add more items (research objects) to an existing outline.yaml. Optionally launches a web-search subagent to suggest items in the topic's domain.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Add Items — Extend Item List

## Trigger

`/research-add-items`

Manual-only via `disable-model-invocation: true`. Run between `/research` and `/research-deep` whenever the initial item list missed something.

## Pipeline Context

Phase 2a of 5 (optional). Edits `outline.yaml` in place. Does not chain — when finished, the user decides whether to iterate further (`/research-add-fields`) or move on (`/research-deep`).

## Workflow

### Step 1 — Locate Outline

Glob `*/outline.yaml` in the current working directory and read it. If multiple match, ask which.

### Step 2 — Gather Candidate Items (Two Sources in Parallel)

Use AskUserQuestion to ask both:

- "Which items do you want to add? (free-form list)"
- "Run a web search to suggest more items in this domain? (yes/no)"

If web search is requested, launch one `web-search-agent` subagent with a prompt asking for additional items in the topic's domain, returning each as `name: short description`.

### Step 3 — Merge, Deduplicate, Confirm, Save

- Combine user-named items + web-search suggestions
- Deduplicate by `name` (case-insensitive)
- Show the proposed additions to the user for confirmation
- Append the confirmed items to `outline.yaml` (preserve existing entries) and save

## Output

`{topic}/outline.yaml` updated in place, with the appended items echoed back to the user.
