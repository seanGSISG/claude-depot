---
name: reclassify
description: >-
  Re-evaluate and update a note's type and tags based on its content. Triggers:
  "reclassify", "recategorize", "re-tag", "this note is in the wrong type",
  "update the tags on", "this should be a config not a reference". Only runs
  when explicitly requested.
disable-model-invocation: true
argument-hint: "<note name>"
---

# Reclassify Note

Analyze a note's content and suggest a better type and tags.

## Workflow

1. **Find the note**: Search `Notes/*/` for a file matching `$ARGUMENTS` (case-insensitive, partial match). If multiple matches, list and let user pick.

2. **Analyze**: Read the full note. Read `CLAUDE.md` for type definitions. Compare actual content against current metadata.

3. **Present comparison**: Show current vs. suggested classification with reasoning (e.g., "this is mostly deployment steps" not just "config").

4. **Apply if approved**:
   - Use **Edit** to update `type` and `tags` in frontmatter. Preserve everything else.
   - If the type changed, use **Bash `mv`** to relocate from `Notes/<old-type>/` to `Notes/<new-type>/`.
