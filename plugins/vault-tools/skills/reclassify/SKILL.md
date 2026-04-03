---
name: reclassify
description: >-
  Re-evaluate and update a note's type and tags based on its content. Use when
  the user wants to reclassify, recategorize, re-tag, or update the metadata of
  an existing note. Triggers include "reclassify", "recategorize", "this note
  is in the wrong type", "update the tags on", "re-tag", or "this should be a
  config not a reference". Only runs when explicitly requested.
disable-model-invocation: true
argument-hint: "<note name>"
---

# Reclassify Note

Analyze a note's actual content and suggest a better type and tags than what it currently has.

Notes sometimes get classified quickly during inbox processing and the initial classification doesn't hold up over time — content evolves, or the original categorization was a rough guess. This skill provides a second opinion grounded in the content itself.

## Workflow

1. **Find the note**: Search `Notes/` for a file matching `$ARGUMENTS` (case-insensitive, partial match). If multiple matches, list them and let the user pick.

2. **Analyze**: Read the full note, then read `CLAUDE.md` for type definitions. Compare what the note actually contains against what its metadata claims.

3. **Present a comparison**: Show current vs. suggested classification with reasoning for each change. The reasoning is important — "this is mostly deployment steps" is more useful than just "config."

4. **Apply if approved**: Update only `type` and `tags` in the frontmatter. Preserve everything else unchanged.
