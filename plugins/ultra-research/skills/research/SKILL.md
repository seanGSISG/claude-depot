---
name: research
description: Build a structured research outline (items + field definitions) on a topic, mixing model knowledge with a single web-search supplement pass. Writes outline.yaml and fields.yaml to a topic-named subdirectory. Entry point of the 5-phase research pipeline.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, WebFetch, Task, AskUserQuestion, mcp__exa_websearch__web_search_exa, mcp__exa_websearch__web_fetch_exa
---

# Research — Build Outline

## Trigger

`/ultra-research:research <topic>`

Manual-only. `disable-model-invocation: true` is set in frontmatter so Claude never auto-runs this skill from description matching — it only fires when the user types the slash command.

## Pipeline Context

This is phase 1 of 5. The full flow is:

1. `/ultra-research:research <topic>` — **(this skill)** builds `outline.yaml` + `fields.yaml`
2. `/ultra-research:research-add-items` *(optional)* — extend the item list
3. `/ultra-research:research-add-fields` *(optional)* — extend the field list
4. `/ultra-research:research-deep` — fan out parallel web-search subagents, one per item, write per-item JSON to `results/`
5. `/ultra-research:research-report` — consume `results/*.json` and emit a single markdown `report.md`

At the end of this skill, ask the user which phase to enter next (see Step 5).

## Workflow

### Step 1 — Generate Initial Framework from Model Knowledge

Use the model's existing knowledge of `{topic}` to draft:

- A main **items list** (research objects in this domain)
- A suggested **field framework** (categories + fields to capture per item)

Print the draft as `{step1_output}`. Use AskUserQuestion to confirm:

- "Add or remove any items?"
- "Does the field framework cover what you need?"

### Step 2 — Web Search Supplement (Single Pass)

Ask the user for a time range via AskUserQuestion (offer "last 6 months", "since 2024", "unlimited", or custom).

Get the current date once with `date +%Y-%m-%d` and bind it to `{YYYY-MM-DD}`.

**⛔ Dispatch-only.** The orchestrator MUST NOT call `WebSearch`, `WebFetch`, or `mcp__exa_websearch__*` directly. Instead, launch one `web-search-agent` subagent (background, via the harness's `Agent`/`Task` tool) with the verbatim prompt template documented in `references/prompt-templates.md`. The template is a hard constraint — only substitute the `{variable}` placeholders; do not rewrite the structure or wording. See that file for the template, the variable table, and a one-shot example.

The subagent returns supplementary items, recommended fields, and source links — capture this as `{step2_output}`.

### Step 3 — Merge with User's Existing Fields (Optional)

Use AskUserQuestion to ask if the user has an existing field-definition file to merge in. If yes, read it and union the definitions.

### Step 4 — Write `outline.yaml` and `fields.yaml`

Merge `{step1_output}`, `{step2_output}`, and any imported user fields. Write two files into `./{topic_slug}/`:

**`outline.yaml`** — items list and execution config:

```yaml
topic: <Research topic>
items:
  - name: <item name>
    category: <optional grouping>
    description: <one-line description>
execution:
  batch_size: <parallel-agent count, confirm with AskUserQuestion>
  items_per_agent: <items per agent, confirm with AskUserQuestion>
  output_dir: results
```

**`fields.yaml`** — field definitions:

```yaml
field_categories:
  - category: Basic Info
    fields:
      - name: <field name>
        description: <what to capture>
        detail_level: brief | moderate | detailed
        required: true | false
uncertain: []   # reserved — populated by /ultra-research:research-deep
```

The `detail_level` ladder (`brief` → `moderate` → `detailed`) hints to the deep-research subagents how thorough to be per field.

### Step 5 — Inspect Coverage and Route to Next Phase

**Before asking**, Read the two files you just wrote and apply this **thinness rubric** to decide which next-step options to mark `(Recommended)`:

| Check | Trigger for `(Recommended)` |
|---|---|
| `outline.yaml` items count | < 8 items, OR no `category` field used, OR clearly missing well-known entrants in the domain → recommend **Add more items** |
| `fields.yaml` total fields | < 6 fields, OR only one `field_categories` entry, OR no field with `detail_level: detailed` → recommend **Add more fields** |

Both checks are independent — mark either, both, or neither.

Then use AskUserQuestion with `header: "Next step"` and these options (append ` (Recommended)` to the label when the rubric flags it):

- **Add more items** — extend `outline.yaml` (description: "Run `/ultra-research:research-add-items` to grow the item list.")
- **Add more fields** — extend `fields.yaml` (description: "Run `/ultra-research:research-add-fields` to enrich the field schema.")
- **Start deep research** — kick off the heavy phase (description: "Run `/ultra-research:research-deep` to fan out parallel subagents.")
- **Done for now** — stop here (description: "Print the directory path and exit. You can resume from any phase later.")

In the question body, briefly tell the user *why* each recommendation was made (e.g., "Only 5 items so far; add more before deep research"). Be one sentence per reason.

If the user picks one of the first three, invoke the corresponding skill **immediately** via the Skill tool (no need for them to type the slash command). If "Done for now," print the directory path and stop.

## Output

```
{cwd}/{topic_slug}/
├── outline.yaml    # items list + execution config
└── fields.yaml     # field definitions
```

## References

- `references/prompt-templates.md` — verbatim Step 2 prompt template, variable table, one-shot example. Read it before launching the web-search subagent.
