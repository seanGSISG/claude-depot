---
name: new-note
description: >-
  Interactively create a vault note with guided type selection, tags, and
  template. Triggers: "create a note about", "new note", "add a note on",
  "start writing about", "I want to document", "write up", "jot down". For
  quick capture without prompts, use auto-categorize instead.
argument-hint: "<title>"
---

# New Note

Create a new note with the correct template and frontmatter.

## Workflow

1. **Title**: Use `$ARGUMENTS` if provided, otherwise ask.

2. **Load schema**: Read `CLAUDE.md` for current valid types with descriptions. Present them for selection — do not hardcode.

3. **Type**: Ask the user to pick one. Show type name and "Use When" description.

4. **Tags**: Ask for tags (free-form, kebab-case). Show common tags as suggestions but accept any value.

5. **Generate**: Read the matching template from `Templates/<Type>.md`. Fill frontmatter: title, type, tags, `created` as today, `status: active`. If the user provided content context in conversation, generate the body.

6. **Write** to `Notes/<type>/<kebab-case-title>.md` and confirm with final frontmatter.

## Efficiency shortcut

If the user provides enough context upfront (e.g., "/new-note MCP Server Setup — it's a config guide about MCP"), infer type and tags. Confirm choices rather than re-asking.

## Template mapping (fallback reference)

The canonical type list comes from the vault's `CLAUDE.md` (loaded in step 2). This table is a fallback if that file is unavailable. Template path pattern: `Templates/<Type>.md` (capitalized).
