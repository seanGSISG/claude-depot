---
name: auto-categorize
description: >-
  Automatically turn raw text, a URL, or conversational content into a properly
  formatted vault note. Use when the user pastes content and wants it saved,
  shares a URL to capture, says "save this as a note", "clip this", "add this
  to the vault", "categorize this", "turn this into a note", or wants to
  quickly capture something without going through the interactive /new-note
  flow. Also trigger if the user says "I found this useful, save it" or
  describes information they want persisted to the vault.
---

# Auto-Categorize

Convert raw input into a classified vault note — the fast path for capturing knowledge without interactive selection.

Unlike `/new-note` (which asks the user to pick type and tags), this skill analyzes the content and proposes a classification automatically. It's ideal for quick captures where the user doesn't want to think about metadata.

## Workflow

1. **Identify input**: raw text pasted in conversation, a URL (fetch with WebFetch), or a topic the user described.

2. **Classify**: Read `CLAUDE.md` for the schema. Analyze the content to determine the best type and tags (kebab-case). Consider the *kind* of content (code snippet? tutorial? reference doc?) for type, and the *topics* covered for tags.

3. **Present**: Show the proposed title, type, and tags. Ask the user to confirm or adjust — this is a quick confirmation, not an interactive menu.

4. **Generate**: Read the matching template from `Templates/<Type>.md` (every type has its own template). Format the content appropriately for the type (e.g., code blocks for configs, step-by-step structure for guides, structured sections for references).

5. **Write** to `Notes/<kebab-case-title>.md` and confirm.
