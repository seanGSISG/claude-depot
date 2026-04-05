---
name: vault-stats
description: >-
  Show statistics and overview of the Obsidian vault — note counts, type/tag
  distribution, recent activity. Triggers: "vault stats", "how many notes",
  "vault overview", "show me the vault", "what's in my vault", "note counts",
  "vault summary".
---

# Vault Stats

Generate a statistical overview of the vault's contents by scanning all `Notes/*/` subfolders.

## What to report

- **Notes by type**: count per type subfolder, sorted descending
- **Notes by tag**: count per tag from frontmatter, sorted descending (top 20)
- **Notes by status**: count for active, draft, archived
- **Recently created**: 10 newest by `created` date, with type
- **Recently modified**: 10 most recently changed by filesystem mtime
- **Inbox**: pending file count
- **Totals**: overall note count, archive count

Present as clean markdown tables. Quick pulse-check — user should glance and understand where knowledge is concentrated.
