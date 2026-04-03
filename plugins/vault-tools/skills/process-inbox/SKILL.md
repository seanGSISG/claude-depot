---
name: process-inbox
description: >-
  Process and classify files in the Obsidian vault Inbox. Use whenever the user
  mentions their inbox, asks what needs filing, wants to organize new captures,
  or says things like "process inbox", "check inbox", "what's new", "classify
  these", or "file my notes". Also trigger when the user drops content into
  Inbox/ and wants it moved to Notes/ with proper metadata. Even casual
  references like "anything in my inbox?" or "triage my captures" should invoke
  this skill.
---

# Process Inbox

Classify unprocessed files from `Inbox/` and move them to `Notes/` with proper YAML frontmatter.

The vault uses a flat organization system — every note lives in `Notes/` and is organized through frontmatter metadata, not folders. Inbox is the landing zone for raw captures that haven't been classified yet. This skill bridges that gap.

## Workflow

1. List all files in `Inbox/`. If empty, tell the user and stop.

2. Read `CLAUDE.md` to load the current valid types and frontmatter schema. This is the source of truth — never rely on hardcoded values.

3. For each file:
   - Read the full content
   - Determine the best **type** (exactly 1) and **tags** (1 or more, kebab-case) based on content
   - Pick the matching template from `Templates/<Type>.md` (e.g., `Templates/Guide.md` for guides, `Templates/Agent.md` for agents — every type has its own template)
   - Build frontmatter: derive a title from the filename or first heading, set `created` to today, `status` to `active`
   - If the file already has frontmatter, preserve existing properties and only fill gaps
   - Present the proposed classification for user approval before doing anything

4. After the user approves (or adjusts), write the classified file to `Notes/<kebab-case-title>.md` and remove it from `Inbox/`.

5. Summarize what was processed.

## Why user approval matters

Classification is subjective — a note about "setting up an MCP server for Claude" could be a guide, a config, or a reference depending on the author's intent. Always show the proposed classification and let the user adjust before moving files. If you're genuinely uncertain between two types, present both options with your reasoning.
