---
name: weekly-review
description: >-
  Generate a weekly digest of vault activity, surface connections, and flag
  items needing attention. Triggers: "weekly review", "weekly report", "vault
  digest", "what happened this week", "what did I write this week". Only runs
  when explicitly requested.
disable-model-invocation: true
---

# Weekly Review

Produce a 7-day digest of vault activity across all `Notes/*/` subfolders.

## What to include

1. **New notes**: `created` date in past 7 days. Show title, type, tags.

2. **Modified notes**: Changed in past 7 days (file mtime) that aren't newly created. Indicates active thinking.

3. **Inbox status**: Flag pending files, suggest `/process-inbox`.

4. **Suggested connections**: Most valuable section. Look at this week's notes for:
   - Pairs sharing tags but no `[[wikilinks]]` to each other
   - Related topics that would benefit from cross-references
   - Suggest specific wikilinks and why

5. **Stale drafts**: `status: draft` older than 30 days. Finish or archive.

6. **Tag activity**: Which tags saw the most new/modified notes. Reveals focus areas.

Present as clean, scannable tables.
