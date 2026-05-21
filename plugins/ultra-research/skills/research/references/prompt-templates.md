# Prompt Templates — `/ultra-research:research` (Step 2 Web Search Supplement)

This file holds the verbatim prompt template and one-shot example used by Step 2 of the `research` skill. It is loaded as a reference so SKILL.md can stay focused on workflow control. The template is a hard constraint — only substitute the `{variable}` placeholders; do not modify structure or wording.

## Template

```python
prompt = f"""## Task
Research topic: {topic}
Current date: {YYYY-MM-DD}

Based on the following initial framework, supplement latest items and recommended research fields.

## Existing Framework
{step1_output}

## Goals
1. Verify if existing items are missing important objects
2. Supplement items based on missing objects
3. Continue searching for {topic} related items within {time_range} and supplement
4. Supplement new fields

## Output Requirements
Return structured results directly (do not write files):

### Supplementary Items
- item_name: Brief explanation (why it should be added)
...

### Recommended Supplementary Fields
- field_name: Field description (why this dimension is needed)
...

### Sources
- [Source1](url1)
- [Source2](url2)
"""
```

## Variable Reference

| Variable | Source |
|---|---|
| `{topic}` | User input research topic |
| `{YYYY-MM-DD}` | Current date — get via `date +%Y-%m-%d` |
| `{step1_output}` | Complete output from Step 1 (model-knowledge framework) |
| `{time_range}` | User-specified time range from AskUserQuestion (e.g. "last 6 months", "since 2024", "unlimited") |

## One-Shot Example

Assuming the user is researching "AI Coding History" and chose `since 2024` as the time range, the rendered prompt should look like:

```
## Task
Research topic: AI Coding History
Current date: 2025-12-30

Based on the following initial framework, supplement latest items and recommended research fields.

## Existing Framework
### Items List
1. GitHub Copilot: Developed by Microsoft/GitHub, first mainstream AI coding assistant
2. Cursor: AI-first IDE, based on VSCode
...

### Field Framework
- Basic Info: name, release_date, company
- Technical Features: underlying_model, context_window
...

## Goals
1. Verify if existing items are missing important objects
2. Supplement items based on missing objects
3. Continue searching for AI Coding History related items within since 2024 and supplement
4. Supplement new fields

## Output Requirements
Return structured results directly (do not write files):

### Supplementary Items
- item_name: Brief explanation (why it should be added)
...

### Recommended Supplementary Fields
- field_name: Field description (why this dimension is needed)
...

### Sources
- [Source1](url1)
- [Source2](url2)
```
