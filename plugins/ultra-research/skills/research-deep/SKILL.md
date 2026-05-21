---
name: research-deep
description: Run deep research on each item in outline.yaml by fanning out parallel web-search subagents. Writes one validated JSON per item to results/. Resumable — skips items that already have a complete JSON.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, WebSearch, WebFetch, Task, AskUserQuestion, mcp__exa_websearch__web_search_exa, mcp__exa_websearch__web_fetch_exa
---

# Research Deep — Fan-Out Per-Item Research

## Trigger

`/ultra-research:research-deep`

Manual-only via `disable-model-invocation: true`. Heavy phase — it spawns many parallel subagents and writes many files, so explicit user start is required.

## Pipeline Context

Phase 3 of 5 (the heavy one). Consumes `outline.yaml` + `fields.yaml`. Produces one JSON per item in `results/`. At the end, offers to chain into `/ultra-research:research-report`.

## ⛔ HARD CONSTRAINT — Orchestrator Role

The orchestrator (the agent reading this SKILL.md) **MUST NOT** perform web searches itself. Its job is **dispatch + monitor + read results**, nothing else.

| ✅ Orchestrator does | ⛔ Orchestrator MUST NOT do |
|---|---|
| Read `outline.yaml` and `fields.yaml` | Call `WebSearch`, `WebFetch`, `mcp__exa_websearch__*` directly |
| Discover the validator path | Read the contents of web pages to extract field values |
| Slugify item names | Write the per-item JSON files itself |
| Launch ONE `web-search-agent` subagent per item via the Agent/Task tool, **in parallel**, **in the background** | Compile data inline in this conversation and write the JSON itself |
| Monitor `results/<slug>.json` files appearing on disk | "Optimize" by running fewer searches in the main session because the item count is "small" |
| Read completed JSONs to summarize for the user | Skip subagent dispatch because the data "is already known" |

**Why this is a hard constraint.** Parallelism is the entire point of this phase — fanning out N items across N subagents collapses N×search-time into ~1×search-time. Inlining the work in the orchestrator session serializes everything, blows out the orchestrator's context window with raw page content, and silently regresses the pipeline to a sequential single-thread flow. A reviewer cannot tell from the final report that this happened — only the absence of per-item subagent transcripts reveals it.

**Item count is not an exemption.** Even for 2 items, dispatch 2 subagents. Even for 1 item, dispatch 1 subagent. The wave size and `batch_size` may be lowered for small item counts, but the dispatch pattern does not change.

If you (the orchestrator) catch yourself about to call `WebSearch` or `mcp__exa_websearch__*` directly in this phase, **stop** and launch a subagent instead.

## Execution Notes

- **Background subagents.** Each `web-search-agent` is launched as a background subagent (`Task` tool with background execution, or the harness's equivalent `Agent` tool with `run_in_background: true`). Task output is suppressed because each subagent's *real* output is the JSON file it writes — surfacing the subagent's chat transcript would be noisy.
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

If `$VALIDATOR` is empty, stop and tell the user the `/ultra-research:research` skill must be installed alongside `/ultra-research:research-deep`. Otherwise bind it to the `{validator_path}` placeholder used by the per-item prompt template.

### Step 2 — Resume Check

List existing `<output_dir>/*.json` files. For each, if it parses as JSON and contains the expected fields, mark its item as **done** and skip it in Step 3.

### Step 3 — Batched Fan-Out (DISPATCH-ONLY)

Bucket the remaining items by `items_per_agent`. Process buckets in waves of `batch_size`:

- Before each wave, ask the user (AskUserQuestion) to confirm starting the next batch.
- **Dispatch ONLY.** For every item in the wave, launch a `web-search-agent` subagent via the harness's `Agent`/`Task` tool with `run_in_background: true` (or equivalent). All subagents in a wave are launched in a **single message with multiple parallel Agent tool calls** so they actually run concurrently.
- Each subagent receives the verbatim per-item prompt template from `references/prompt-templates.md` — only substitute placeholders. Each subagent's prompt includes `{validator_path}` from Step 1, so the subagent runs validation as its final step.
- **The orchestrator MUST NOT call `WebSearch`, `WebFetch`, or `mcp__exa_websearch__*` itself during this step.** Re-read the Hard Constraint block above if tempted.
- The orchestrator does not read the subagent transcripts. It only watches `output_dir` for `<slug>.json` files appearing on disk.

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

Then use AskUserQuestion with `header: "Next step"` and ask **"Deep research complete — N items in `./{output_dir}/`. Generate the report now?"** with these options:

- **Generate report (Recommended)** — invoke `/ultra-research:research-report` and let its Step 2 pick TOC fields interactively
- **Generate report — default TOC** — invoke `/ultra-research:research-report` with sensible defaults (skip TOC picker)
- **Not now** — end here; the user can run `/ultra-research:research-report` later

If any items failed validation or have non-empty `uncertain` arrays, mention them in the question body so the user can decide whether to re-run problem items before reporting.

Invoke the picked skill **immediately** via the Skill tool when the user selects either Generate option.

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
