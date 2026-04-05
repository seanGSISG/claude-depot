---
name: process-inbox
description: >-
  Process and classify files in the Obsidian vault Inbox, moving them to Notes/
  with proper frontmatter. Triggers: "process inbox", "check inbox", "classify
  these", "file my notes", "anything in my inbox?", "triage my captures".
---

# Process Inbox

Classify unprocessed files from `Inbox/` and move them to `Notes/<type>/` with proper YAML frontmatter.

## Workflow

1. **List** all files in `Inbox/`. If empty, tell the user and stop.

2. **Load schema** from `CLAUDE.md` — valid types, frontmatter requirements. This is the source of truth.

3. **Classify each file** — read only the first ~20 lines (title, headings, opening content) to determine the best type and tags. Do NOT read the entire file.

4. **Present one batch table** for approval:

   | File | Proposed Title | Type | Tags |
   |------|---------------|------|------|
   | article.md | Some Article | reference | web-dev, react |
   | setup.md | Docker Setup | config | docker, homelab |

   The user adjusts any rows, then approves the whole batch at once.

5. **Execute each approved file** using these exact operations:

   a. **Rename + move** with Bash `mv`:
      ```
      mv "Inbox/<filename>" "Notes/<type>/<kebab-case-title>.md"
      ```

   b. **Add frontmatter** with the Edit tool — prepend the YAML block to the file. If the file already has frontmatter (`---` on line 1), use Edit to fill missing fields only.

6. **Summarize** what was processed: count moved, destination subfolders used.

## Critical efficiency rules

- **NEVER use Write** to rewrite an existing file. Write sends the entire file content through the API — for long articles this is extremely slow.
- **Use Bash `mv`** to relocate files. One command, instant.
- **Use Edit** to add or update frontmatter. Edit sends only the diff.
- Read only enough of each file to classify it (~20 lines). Do not read full content unless classification is ambiguous.

## Frontmatter to add

```yaml
---
title: "Derived from filename or first heading"
type: <chosen-type>
tags:
  - <tag-1>
  - <tag-2>
created: YYYY-MM-DD
status: active
---
```

Preserve any existing non-schema properties. Set `created` to today's date.
