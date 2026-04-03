---
name: vault-search
description: >-
  Search the Obsidian vault for notes matching a natural language query. Use
  whenever the user wants to find, locate, or look up notes — even if they
  don't say "search". Triggers include "find notes about", "search vault",
  "which notes mention", "do I have anything on", "look up", "find anything
  about", "where did I write about", or questions like "what do I know about
  React performance?". If the user is trying to recall or locate something
  they previously saved, this is the right skill.
argument-hint: "<natural language query>"
---

# Vault Search

Find notes in `Notes/` that match a natural language query by searching across metadata and content.

## Approach

Interpret the user's query and search across multiple dimensions:

- **Type match**: If the query implies a note type (e.g., "guides about X"), grep frontmatter for type matches
- **Tag match**: If the query maps to a known tag, grep frontmatter for exact matches — these are the highest-confidence results
- **Title match**: Search filenames for query terms
- **Content match**: Grep note bodies for keywords from the query

Combine results across all dimensions. Notes that match on multiple dimensions (e.g., both tag and content) are more relevant than single-dimension matches.

## Presenting results

Show the top results in a table with: note name (as `[[wikilink]]`), type, tags, and a brief note on why it matched. If the query was broad, cap at ~15 results. If nothing matched, suggest alternative search terms or related tags the user might try.

The goal is to help the user quickly find what they're looking for, not to be exhaustive. Relevance over completeness.
