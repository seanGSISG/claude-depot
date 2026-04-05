---
name: auto-categorize
description: >-
  Quick-capture raw text, a URL, or conversational content into a classified
  vault note — no interactive prompts. Triggers: "save this as a note", "clip
  this", "add this to the vault", "categorize this", "turn this into a note",
  "I found this useful, save it".
---

# Auto-Categorize

Convert raw input into a classified vault note — the fast path for capturing knowledge.

Unlike `/new-note` (interactive selection), this skill analyzes content and proposes classification automatically.

## Workflow

1. **Identify input**: raw text pasted in conversation, a URL (fetch with WebFetch), or a topic the user described.

2. **Classify**: Read `CLAUDE.md` for the schema. Determine best type and tags (kebab-case). Consider content kind (code? tutorial? reference?) for type, and topics for tags.

3. **Present**: Show proposed title, type, and tags. Ask the user to confirm or adjust — quick confirmation, not interactive menu.

4. **Generate**: Read the matching template from `Templates/<Type>.md`. Format content appropriately for the type.

5. **Write** to `Notes/<type>/<kebab-case-title>.md` and confirm.

## Tool guidance

- **New content** (URL captures, user-provided text): Use Write to create the file.
- **Existing file** being re-categorized: Use Edit for frontmatter changes, Bash `mv` to relocate.
