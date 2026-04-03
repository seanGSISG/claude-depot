---
name: vault-stats
description: >-
  Show statistics and overview of the Obsidian vault. Use when the user asks
  about vault size, note counts, type or tag distribution, recent activity, or
  general vault health. Triggers include "vault stats", "how many notes",
  "vault overview", "show me the vault", "what's in my vault", "note counts",
  "vault summary", or any question about the composition or size of the vault.
---

# Vault Stats

Generate a statistical overview of the vault's contents.

## What to report

Parse the frontmatter of all files in `Notes/` and produce:

- **Notes by type**: count per type, sorted by count descending
- **Notes by tag**: count per tag, sorted by count descending (top 20)
- **Notes by status**: count for active, draft, archived
- **Recently created**: the 10 newest notes by `created` date, with their type
- **Recently modified**: the 10 most recently changed files by filesystem mtime
- **Inbox**: number of files pending processing
- **Totals**: overall note count, archive file count

Present everything as clean markdown tables. The goal is a quick pulse-check on the vault — the user should be able to glance at this and understand where their knowledge is concentrated and what's been active recently.
