# Prompt Templates — `/research-deep` (Per-Item Subagent Prompt)

This file holds the verbatim per-item prompt template used by the `research-deep` skill when it fans out parallel `web-search-agent` subagents. The template is a hard constraint — only substitute the `{variable}` placeholders; do not modify structure or wording.

## Template

```python
prompt = f"""## Task
Research {item_related_info}, output structured JSON to {output_path}

## Field Definitions
Read {fields_path} to get all field definitions

## Output Requirements
1. Output JSON according to fields defined in fields.yaml
2. Mark uncertain field values with [uncertain]
3. Add uncertain array at the end of JSON, listing all uncertain field names
4. All field values must be in English

## Output Path
{output_path}

## Validation
After completing JSON output, run validation script to ensure complete field coverage:
python {validator_path} -f {fields_path} -j {output_path}
Task is complete only after validation passes.
"""
```

## Variable Reference

| Variable | Source |
|---|---|
| `{item_related_info}` | Item's complete YAML record from `outline.yaml` (name + category + description) |
| `{output_path}` | Absolute path to `{output_dir}/{item_name_slug}.json` (slugify: spaces → `_`, strip specials) |
| `{fields_path}` | Absolute path to `{topic}/fields.yaml` |
| `{validator_path}` | Absolute path to `validate_json.py`, discovered at start of `/research-deep` execution (see SKILL.md Step 1) |

Slugify rule for `{item_name_slug}`: lowercase optional; replace spaces with `_`; strip characters outside `[A-Za-z0-9_-]`.

## One-Shot Example

Assuming the user is researching "AI Coding History" and the current item is "GitHub Copilot":

```
## Task
Research name: GitHub Copilot
category: International Product
description: Developed by Microsoft/GitHub, first mainstream AI coding assistant, ~40% market share, output structured JSON to /home/user/ai-coding-history/results/GitHub_Copilot.json

## Field Definitions
Read /home/user/ai-coding-history/fields.yaml to get all field definitions

## Output Requirements
1. Output JSON according to fields defined in fields.yaml
2. Mark uncertain field values with [uncertain]
3. Add uncertain array at the end of JSON, listing all uncertain field names
4. All field values must be in English

## Output Path
/home/user/ai-coding-history/results/GitHub_Copilot.json

## Validation
After completing JSON output, run validation script to ensure complete field coverage:
python /home/user/.claude/skills/research/scripts/validate_json.py -f /home/user/ai-coding-history/fields.yaml -j /home/user/ai-coding-history/results/GitHub_Copilot.json
Task is complete only after validation passes.
```

## Why this template is hard-constrained

The downstream validator (`validate_json.py`) expects a specific JSON shape: defined fields covered, `[uncertain]` markers on incomplete values, and an `uncertain` array at the end. The prompt language has been tuned so subagents reliably produce that shape. Loosening the wording risks subagents skipping the validation step or omitting the `uncertain` array, which breaks the downstream report generator.
