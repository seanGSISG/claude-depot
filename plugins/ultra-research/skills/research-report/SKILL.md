---
name: research-report
description: Convert per-item JSON results from /research-deep into a single markdown report with table of contents and per-item sections. Uses a bundled converter script — no per-run script regeneration.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Research Report — Generate Markdown Report

## Trigger

`/research-report`

Manual-only via `disable-model-invocation: true`. Final phase of the pipeline; invoked directly by the user or chained from `/research-deep`'s end-prompt.

## Pipeline Context

Phase 5 of 5 (terminal). Consumes `results/*.json` + `fields.yaml`. Produces `report.md` in the topic directory. The conversion script is **bundled** at `scripts/generate_report.py` — do not regenerate it per run.

## Workflow

### Step 1 — Locate Results

Glob `*/outline.yaml` in the current working directory to find the topic directory. Read `topic`, `execution.output_dir` (default: `results`). Confirm the results directory exists and contains JSON files.

### Step 2 — Pick TOC Summary Fields

Scan all `<output_dir>/*.json` to discover which fields are present across items. Identify fields suitable for table-of-contents display — short, scalar, ideally numeric. Common examples: `github_stars`, `google_scholar_cites`, `release_date`, `user_scale`, `valuation`, `swe_bench_score`.

Use AskUserQuestion to ask:

- "Which fields should appear in the TOC alongside each item's name? (multi-select)"
- Build the option list dynamically from fields actually present in the JSON.

If the user picks none, the TOC will list item names only (still valid).

### Step 3 — Run the Bundled Converter

Resolve the script path. When this skill ships as the `ultra-research` plugin, the script lives at `${CLAUDE_PLUGIN_ROOT}/skills/research-report/scripts/generate_report.py`. Fall back to legacy install paths only if `${CLAUDE_PLUGIN_ROOT}` is unset:

```bash
GENERATOR="${CLAUDE_PLUGIN_ROOT}/skills/research-report/scripts/generate_report.py"
[ -f "$GENERATOR" ] || GENERATOR=$(ls ~/.claude/skills/research-report/scripts/generate_report.py 2>/dev/null \
          || find ~/.claude -name generate_report.py -path '*/research-report/scripts/*' 2>/dev/null | head -1)
```

Then invoke:

```bash
python "$GENERATOR" \
  --topic-dir "<topic_dir>" \
  --results-dir "<output_dir>" \
  --toc-fields "<comma-separated user selections>" \
  --output report.md
```

The script handles all of the conversion logic — see `references/converter-contract.md` for what it does (and what NOT to reimplement inline if you find yourself tempted to "fix" something on the fly).

### Step 4 — Surface the Report

Tell the user the path to the generated `report.md`. Offer to print the first ~30 lines for a quick sanity check.

## Output

- `{topic}/report.md` — the final markdown report

## References

- `references/converter-contract.md` — what `scripts/generate_report.py` does, what it filters, what its CLI accepts. Read this before "fixing" the bundled script — most of its behavior is intentional.

## Scripts

- `scripts/generate_report.py` — the bundled converter. Single source of truth for report formatting. Do not regenerate per run.
