---
name: vault-maintenance
description: >-
  Run comprehensive health checks on the Obsidian vault — orphan notes, stale
  drafts, broken links, type mismatches. Triggers: "vault maintenance", "check
  vault health", "find orphan notes", "audit my vault", "what needs fixing".
  Only runs when explicitly requested.
disable-model-invocation: true
---

# Vault Maintenance

Scan the vault for structural issues and report findings with actionable fixes. Use Grep and Glob for efficiency — avoid reading files fully when a frontmatter scan suffices.

## Checks

### 1. Orphan notes
Notes in `Notes/*/` missing `type` or `tags` frontmatter. These won't appear in Bases views.

### 2. Stale drafts
Notes with `status: draft` where `created` is 30+ days old. Finish or archive.

### 3. Duplicate detection
Notes with very similar titles (case-insensitive). Flag pairs for review.

### 4. Invalid types
Notes with a `type` value not in CLAUDE.md's valid types.

### 5. Subfolder mismatch
Notes where the subfolder name doesn't match the `type` frontmatter field (e.g., file in `Notes/config/` with `type: reference`). Fix by moving the file or updating the type.

### 6. Broken wikilinks
`[[...]]` links that don't resolve to any vault file.

### 7. Inbox status
Count unprocessed files in `Inbox/`.

## Report format

Structured report with counts per check, specific items found, summary. After report, offer to fix: use Edit for frontmatter fixes, Bash `mv` to relocate misplaced files.
