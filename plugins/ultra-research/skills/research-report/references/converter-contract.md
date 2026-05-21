# Converter Contract — `scripts/generate_report.py`

This file documents what the bundled converter does. The script is the single source of truth for report formatting — when in doubt about behavior, run the script and inspect its output instead of re-deriving the logic inline.

## Why the script is bundled

Earlier versions of `/research-report` asked Claude to regenerate this converter from a long spec on every run. That wasted tokens and drifted between invocations (different runs produced different markdown for the same JSON). Bundling fixes both.

If the converter needs a new feature, edit the script and re-package the skill. **Do not** prompt the model to write a one-off variant inline.

## CLI

```
python generate_report.py \
  --topic-dir <path>             # directory containing fields.yaml + results/
  [--results-dir <name>]         # default: results
  [--fields <name>]              # default: fields.yaml
  [--toc-fields <a,b,c>]         # comma-separated field names for TOC summary
  [--output <name>]              # default: report.md (relative to topic-dir)
  [--title <text>]               # default: derived from topic-dir name
```

Exit 0 on success, 1 on missing fields.yaml / results-dir / empty results-dir.

## Input expectations

- **`fields.yaml`** — has `field_categories: [{category: <name>, fields: [{name, description, detail_level, required}]}]`.
- **`results/*.json`** — one per item. Each JSON may be flat (`{"name": ..., "release_date": ...}`) or nested by category (`{"basic_info": {"name": ...}, ...}`). Both shapes are supported by `lookup()` and `collect_extra_fields()`.

## What the script does

1. **Loads `fields.yaml`** and builds a `field_name → category` map (preserves category ordering from the file).
2. **Reads each JSON** in `results-dir`. Captures the item's `name` (via `lookup()`, which checks flat then nested locations) and its `uncertain` array (if present).
3. **Renders a table of contents.** For each item, emits a numbered line: `1. [Name](#name-anchor) - <toc-field>: <value> | <toc-field2>: <value2>`. TOC-field values are pulled via `lookup()` and skipped when uncertain.
4. **Renders each item's section.** For each category in `fields.yaml` ordering, lists `**field**: value` for fields whose value is non-uncertain. Categories with no surviving fields are omitted.
5. **Renders "Other Info" per item.** Any JSON keys not defined in `fields.yaml` (and not in the skip set or category-nesting keys) appear here, in JSON-order.
6. **Renders the per-item "Uncertain Fields" list** if the JSON had a non-empty `uncertain` array.
7. **Writes the markdown** to `<topic-dir>/<output>`.

## Filtering rules (intentional)

A field-value is **uncertain** (and silently skipped from the body but listed at the end) when any of:

- The field name appears in the JSON's `uncertain` array
- The value is `None` or an empty string
- The value is a string containing the marker `[uncertain]`

Always-skipped keys at the JSON top level: `_source_file`, `uncertain`. These are internal/metadata and don't belong in the report body.

Category-nesting keys are recognized via `CATEGORY_MAPPING`, so a nested JSON like `{"basic_info": {...}}` doesn't get `basic_info` listed as a stray "Other Info" field.

## Value formatting rules

- **List of dicts** (e.g. `key_events: [{date: ..., description: ...}]`): one rendered line per dict, fields joined with ` | `, lines joined with `<br>`.
- **Plain list**: comma-joined if total length ≤ 100 chars, otherwise one bullet per item using `<br>`.
- **Nested dict**: `**key**: value` pairs joined with `; ` (or `<br>` if total length > 100 chars).
- **Long string** (> 100 chars): preserved with newlines replaced by `<br>` for markdown readability.
- **Scalar**: as-is.

## `CATEGORY_MAPPING` lives in two places

`generate_report.py` and `../research/scripts/validate_json.py` both define `CATEGORY_MAPPING`. They must stay in sync — when adding a new category alias (e.g. for a new domain's nested key naming), update both files. The mapping is small and audit-friendly; a future refactor could lift it to a shared module if the skills ever ship as a single Python package.

## When to edit the script

Edit `scripts/generate_report.py` directly when:

- A new field-value shape appears that the existing formatters mangle (e.g. a deeply nested or domain-specific structure).
- A new top-level metadata key needs to be filtered out of "Other Info".
- The TOC/section ordering or anchor convention should change.

After editing, re-package the skill with `python -m scripts.package_skill skills/research-en/research-report`.
