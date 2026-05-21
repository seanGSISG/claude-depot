---
name: research-deep
description: Run deep research on each item in outline.yaml by fanning out parallel web-search subagents. Writes one validated JSON per item to results/. Resumable — skips items that already have a complete JSON.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Deep — Fan-Out Per-Item Research

## Trigger

`/research-deep`

Manual-only via `disable-model-invocation: true`. Heavy phase — it spawns many parallel subagents and writes many files, so explicit user start is required.

## Pipeline Context

Phase 3 of 5 (the heavy one). Consumes `outline.yaml` + `fields.yaml`. Produces one JSON per item in `results/`. At the end, offers to chain into `/research-report`.

## Execution Notes

- **Background subagents.** Each `web-search-agent` is launched as a background subagent (`Task` tool with background execution). Task output is suppressed because each subagent's *real* output is the JSON file it writes — surfacing the subagent's chat transcript would be noisy.
- **Resumable.** On re-invocation, the skill scans `output_dir` for existing `<item_slug>.json` files and skips those items. Safe to interrupt and restart.

## Workflow

### Step 1 — Locate Outline and Discover the Validator

Glob `*/outline.yaml` in the current working directory and read it. Capture `topic`, `items`, and `execution` (batch_size, items_per_agent, output_dir).

Locate the `validate_json.py` script. When this skill ships as the `ultra-research` plugin, the script lives at `${CLAUDE_PLUGIN_ROOT}/skills/research/scripts/validate_json.py`. Fall back to legacy install paths only if `${CLAUDE_PLUGIN_ROOT}` is unset:

```bash
VALIDATOR="${CLAUDE_PLUGIN_ROOT}/skills/research/scripts/validate_json.py"
[ -f "$VALIDATOR" ] || VALIDATOR=$(ls ~/.claude/skills/research/scripts/validate_json.py 2>/dev/null \
          || find ~/.claude -name validate_json.py -path '*/research/scripts/*' 2>/dev/null | head -1)
```

If `$VALIDATOR` is empty, stop and tell the user the `/research` skill must be installed alongside `/research-deep`. Otherwise bind it to the `{validator_path}` placeholder used by the per-item prompt template.

### Step 2 — Resume Check

List existing `<output_dir>/*.json` files. For each, if it parses as JSON and contains the expected fields, mark its item as **done** and skip it in Step 3.

### Step 3 — Batched Fan-Out

Bucket the remaining items by `items_per_agent`. Process buckets in waves of `batch_size`:

- Before each wave, ask the user (AskUserQuestion) to confirm starting the next batch.
- Launch one `web-search-agent` per bucket in the wave, in parallel, using the verbatim per-item prompt template from `references/prompt-templates.md`. The template is a hard constraint — only substitute placeholders.
- Each subagent's prompt includes `{validator_path}` from Step 1, so the subagent runs validation as its final step.

See `references/prompt-templates.md` for:
- The full prompt template
- The variable table (`{item_related_info}`, `{output_path}`, `{fields_path}`, `{validator_path}`)
- The slugify rule for `{item_name_slug}`
- A one-shot rendered example
- Why the template is hard-constrained

### Step 4 — Wait, Monitor, Iterate

After each wave, check which `<item_slug>.json` files appeared in `output_dir`. Display progress (X of Y complete). Continue with the next wave until all items are processed.

### Step 5 — Summarize and Offer the Report

Print a summary:

- Items completed (count + names)
- Items that failed validation or have `uncertain` arrays (count + names)
- `output_dir` path

Then use AskUserQuestion to ask **"Deep research complete — N items in `./{output_dir}/`. Generate the report now?"** with these options:

- **Yes, default TOC** → invoke `/research-report` (it will use its own AskUserQuestion to pick TOC fields, but with sensible defaults if you skip)
- **Yes, let me pick TOC fields** → invoke `/research-report` (its Step 2 already handles TOC field selection)
- **Not now — I'll run /research-report later** → end here

## Output

```
{topic}/
├── outline.yaml
├── fields.yaml
└── results/
    ├── <item_slug_1>.json
    ├── <item_slug_2>.json
    └── ...
```

## References

- `references/prompt-templates.md` — verbatim per-item prompt template + variable reference + one-shot example. Read it before launching subagents.
