---
name: weekly-review
description: >-
  Generate a weekly digest of vault activity, surface connections, and flag
  items needing attention. Use when the user asks for a weekly review, wants
  to see recent activity, asks "what happened this week in my vault", or wants
  a summary of recent notes and pending items. Only runs when explicitly
  requested.
disable-model-invocation: true
---

# Weekly Review

Produce a digest of the past 7 days of vault activity to help the user stay on top of their knowledge base.

The value of this review isn't just listing what's new — it's surfacing connections between notes that the user might not have noticed, and flagging things that need attention before they go stale.

## What to include

1. **New notes**: Notes with `created` date in the past 7 days. Show title, type, and tags.

2. **Modified notes**: Notes changed in the past 7 days (by file mtime) that aren't newly created. These indicate active thinking on a topic.

3. **Inbox status**: If any files are pending in `Inbox/`, flag them and suggest `/process-inbox`.

4. **Suggested connections**: This is the most valuable part. Look at this week's notes and find:
   - Pairs that share tags but don't wikilink to each other
   - Notes on related topics that would benefit from cross-references
   - Suggest specific `[[wikilinks]]` to add and why

5. **Stale drafts**: Notes with `status: draft` older than 30 days. These are decisions waiting to be made — finish or archive.

6. **Tag activity**: Which tags saw the most new or modified notes this week. Reveals where the user's focus has been.

Present as a clean, scannable report with tables.
