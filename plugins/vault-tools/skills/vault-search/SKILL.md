---
name: vault-search
description: >-
  Search the vault for notes matching a natural language query. Triggers: "find
  notes about", "search vault", "which notes mention", "do I have anything on",
  "look up", "where did I write about", "what do I know about X?".
argument-hint: "<natural language query>"
---

# Vault Search

Find notes across `Notes/*/` subfolders that match a natural language query.

## Approach

Interpret the query and search across multiple dimensions:

- **Type match**: If the query implies a note type (e.g., "guides about X"), grep frontmatter for type matches
- **Tag match**: If the query maps to a known tag, grep frontmatter — highest-confidence results
- **Title match**: Search filenames across all `Notes/*/` subfolders
- **Content match**: Grep note bodies for keywords

Notes matching multiple dimensions rank higher than single-dimension matches.

## Presenting results

Show top results in a table: note name (as `[[wikilink]]`), type, tags, match reason. Cap at ~15 for broad queries. If nothing matched, suggest alternative terms or tags.

Relevance over completeness.
