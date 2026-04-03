---
name: new-note
description: >-
  Create a new note in the Obsidian vault with proper frontmatter and template.
  Use whenever the user wants to create, start, draft, or add a note — even if
  they don't say "note" explicitly. Triggers include "create a note about",
  "new note", "add a note on", "start writing about", "I want to document",
  "write up", "jot down", or when the user clearly wants to persist some
  knowledge into the vault. If someone says "I should save this" or "let me
  write this down", this is the right skill.
argument-hint: "<title>"
---

# New Note

Interactively create a new note with the correct template and frontmatter.

Every note in this vault requires exactly 1 type (what kind of note it is) and 1 or more tags (what topics it covers). This skill walks the user through that selection rather than guessing — the user knows their intent better than content analysis alone.

## Workflow

1. **Title**: Use `$ARGUMENTS` if provided, otherwise ask.

2. **Load schema**: Read `CLAUDE.md` to get the current valid types (with descriptions). Present them to the user for selection — don't hardcode the lists here since they may change.

3. **Type**: Ask the user to pick one type. Show the type name and its "Use When" description so they can make an informed choice.

4. **Tags**: Ask the user for tags (free-form, kebab-case). Show common tags as suggestions but accept any value.

5. **Generate**: Read the matching template from `Templates/<Type>.md` (e.g., `Templates/Guide.md` for type guide). Every type has its own template. Fill in the frontmatter (`title`, `type`, `tags`, `created` as today's date, `status: active`). If the user provided content context in the conversation, use it to generate the note body.

6. **Write** to `Notes/<kebab-case-title>.md` and confirm with the final frontmatter.

## Template Selection

Each type maps directly to its template:

| Type | Template |
|------|----------|
| reference | `Templates/Reference.md` |
| guide | `Templates/Guide.md` |
| config | `Templates/Config.md` |
| agent | `Templates/Agent.md` |
| prompt | `Templates/Prompt.md` |
| list | `Templates/List.md` |
| project | `Templates/Project.md` |
| plan | `Templates/Plan.md` |
| diagram | `Templates/Diagram.md` |
| note | `Templates/Note.md` |

## Efficiency shortcut

If the user provides enough context upfront (e.g., "/new-note MCP Server Setup — it's a config guide about MCP"), skip the interactive selection and infer the type and tags. Confirm your choices with the user rather than making them re-select.
