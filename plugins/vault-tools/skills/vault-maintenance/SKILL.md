---
name: vault-maintenance
description: >-
  Run comprehensive health checks on the Obsidian vault. Use when the user asks
  to check vault health, find problems, run maintenance, audit notes, or clean
  up the vault. Triggers include "vault maintenance", "check vault health",
  "find orphan notes", "any broken links", "audit my vault", "clean up", or
  "what needs fixing". This is an expensive operation that scans all notes, so
  it only runs when explicitly requested — never auto-triggered.
disable-model-invocation: true
---

# Vault Maintenance

Scan the entire vault for structural issues and report findings with actionable fixes.

This is the comprehensive health check. Use Grep and Glob for efficiency — avoid reading every file fully when a frontmatter scan suffices.

## Checks to run

### 1. Orphan notes
Notes in `Notes/` missing `type` or `tags` frontmatter. These notes won't appear correctly in Bases views, which means they're effectively invisible in the vault's organization system.

### 2. Stale drafts
Notes with `status: draft` where `created` is more than 30 days ago. Drafts that sit too long usually need to be either finished or archived.

### 3. Duplicate detection
Notes with very similar titles (case-insensitive comparison after stripping common words). Flag pairs for the user to review — they may be intentional or accidental.

### 4. Invalid types
Notes with a `type` value that doesn't match the valid types in CLAUDE.md. These need to be reclassified.

### 5. Broken wikilinks
Scan note content for `[[...]]` links that don't resolve to any file in the vault.

### 6. Inbox status
Count unprocessed files in `Inbox/`.

## Report format

Present a structured report with counts per check, specific items found, and a summary line. After the report, offer to fix issues — adding missing frontmatter, updating stale drafts, or processing inbox items.
