---
paths:
  - "Notes/**/*.md"
---

# Notes Frontmatter Requirements

Every file in `Notes/` MUST have valid YAML frontmatter between `---` delimiters.

## Required Schema

```yaml
---
title: "Note Title"
type: reference
tags:
  - claude-code
created: YYYY-MM-DD
status: active
---
```

## Validation Rules

- **type**: Exactly 1 plain string, must be a valid type
- **tags**: 1 or more plain kebab-case strings (no limit)
- **created**: ISO date (YYYY-MM-DD)
- **status**: One of `active`, `draft`, `archived`
- **title**: Required, non-empty string

## Valid Types

reference, guide, config, agent, prompt, list, project, plan, diagram, note

## Tags

Free-form kebab-case strings. No controlled vocabulary — any tag is valid.

## Additional Rules

- Preserve any existing non-schema properties (e.g., `name`, `description`, `source`, `author`, `project`)
- Do not invent new frontmatter fields beyond the schema unless they already exist on the note
- When editing existing notes, never remove or change frontmatter unless specifically asked
