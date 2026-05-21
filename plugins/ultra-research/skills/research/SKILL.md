---
name: research
description: Build a structured research outline (items + field definitions) on a topic, mixing model knowledge with a single web-search supplement pass. Writes outline.yaml and fields.yaml to a topic-named subdirectory. Entry point of the 5-phase research pipeline.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research — Build Outline

## Trigger

`/research <topic>`

Manual-only. `disable-model-invocation: true` is set in frontmatter so Claude never auto-runs this skill from description matching — it only fires when the user types the slash command.

## Pipeline Context

This is phase 1 of 5. The full flow is:

1. `/research <topic>` — **(this skill)** builds `outline.yaml` + `fields.yaml`
2. `/research-add-items` *(optional)* — extend the item list
3. `/research-add-fields` *(optional)* — extend the field list
4. `/research-deep` — fan out parallel web-search subagents, one per item, write per-item JSON to `results/`
5. `/research-report` — consume `results/*.json` and emit a single markdown `report.md`

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

Launch one `web-search-agent` subagent (background) with the verbatim prompt template documented in `references/prompt-templates.md`. The template is a hard constraint — only substitute the `{variable}` placeholders; do not rewrite the structure or wording. See that file for the template, the variable table, and a one-shot example.

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
uncertain: []   # reserved — populated by /research-deep
```

The `detail_level` ladder (`brief` → `moderate` → `detailed`) hints to the deep-research subagents how thorough to be per field.

### Step 5 — Confirm and Route to Next Phase

Show the user the two written files. Then use AskUserQuestion to ask **what's next?** with these options:

- **Add more items** → invoke `/research-add-items`
- **Add more fields** → invoke `/research-add-fields`
- **Start deep research** → invoke `/research-deep`
- **Done — I'll continue later** → end with the directory path summary

If the user picks one of the first three, invoke the corresponding skill immediately. If "Done," print the directory path and stop.

## Output

```
{cwd}/{topic_slug}/
├── outline.yaml    # items list + execution config
└── fields.yaml     # field definitions
```

## References

- `references/prompt-templates.md` — verbatim Step 2 prompt template, variable table, one-shot example. Read it before launching the web-search subagent.
