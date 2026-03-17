---
name: obsidian
description: >-
  Use this skill whenever the user wants to work with Obsidian in any capacity.
  This is the ONLY skill for Obsidian vaults, .base files, Obsidian Markdown,
  Obsidian plugins, and Obsidian Web Clipper. Trigger for: creating or editing
  notes with wikilinks, callouts, embeds, or frontmatter; building or debugging
  .base files (formulas, filters, views, YAML quoting); Obsidian plugin
  development or hot-reload; Web Clipper JSON templates or AI Interpreter
  prompts; vault structure, daily notes, or the obsidian CLI. Also trigger when
  the user describes Obsidian-specific problems without naming Obsidian — like
  .base YAML errors, foldable callout syntax, base formula for tasks due this
  week, or clipper template for arxiv. Do NOT trigger for Logseq, Notion,
  Dataview plugin queries, generic markdown processing scripts, or
  general-purpose Chrome extensions.
---

# Obsidian Skill

Comprehensive skill for working with Obsidian vaults. Covers four domains:

| Domain | When to use | Key references |
|--------|------------|----------------|
| **Markdown** | Creating/editing .md notes with wikilinks, callouts, embeds, properties, tags | [callouts](references/markdown-callouts.md), [embeds](references/markdown-embeds.md), [properties](references/markdown-properties.md) |
| **Bases** | Creating/editing .base files with views, filters, formulas | [functions](references/bases-functions.md) |
| **CLI** | Interacting with vaults via `obsidian` command, plugin dev | (inline below) |
| **Web Clipper** | Creating importable JSON templates for the Obsidian Web Clipper | [variables](references/clipper-variables.md), [filters](references/clipper-filters.md), [json-schema](references/clipper-json-schema.md), [logic](references/clipper-logic.md), [analysis](references/clipper-analysis-workflow.md), [bases-workflow](references/clipper-bases-workflow.md) |

**Official docs**: For edge cases or details beyond this skill, consult the [Official Documentation Index](references/official/INDEX.md) — curated from help.obsidian.md covering Bases, Editing, Web Clipper, CLI, and Linking.

---

## Obsidian Flavored Markdown

Create and edit valid Obsidian Flavored Markdown. Obsidian extends CommonMark and GFM with wikilinks, embeds, callouts, properties, comments, and other syntax. Standard Markdown (headings, bold, italic, lists, quotes, code blocks, tables) is assumed knowledge.

### Workflow: Creating an Obsidian Note

1. **Add frontmatter** with properties (title, tags, aliases) at the top of the file. See [references/markdown-properties.md](references/markdown-properties.md) for all property types.
2. **Write content** using standard Markdown for structure, plus Obsidian-specific syntax below.
3. **Link related notes** using wikilinks (`[[Note]]`) for internal vault connections, or standard Markdown links for external URLs.
4. **Embed content** from other notes, images, or PDFs using the `![[embed]]` syntax. See [references/markdown-embeds.md](references/markdown-embeds.md) for all embed types.
5. **Add callouts** for highlighted information using `> [!type]` syntax. See [references/markdown-callouts.md](references/markdown-callouts.md) for all callout types.
6. **Verify** the note renders correctly in Obsidian's reading view.

> When choosing between wikilinks and Markdown links: use `[[wikilinks]]` for notes within the vault (Obsidian tracks renames automatically) and `[text](url)` for external URLs only.

### Internal Links (Wikilinks)

```markdown
[[Note Name]]                          Link to note
[[Note Name|Display Text]]             Custom display text
[[Note Name#Heading]]                  Link to heading
[[Note Name#^block-id]]                Link to block
[[#Heading in same note]]              Same-note heading link
```

Define a block ID by appending `^block-id` to any paragraph. For lists and quotes, place the block ID on a separate line after the block.

### Embeds

Prefix any wikilink with `!` to embed its content inline:

```markdown
![[Note Name]]                         Embed full note
![[Note Name#Heading]]                 Embed section
![[image.png]]                         Embed image
![[image.png|300]]                     Embed image with width
![[document.pdf#page=3]]               Embed PDF page
```

See [references/markdown-embeds.md](references/markdown-embeds.md) for audio, video, search embeds, and external images.

### Callouts

```markdown
> [!note]
> Basic callout.

> [!warning] Custom Title
> Callout with a custom title.

> [!faq]- Collapsed by default
> Foldable callout (- collapsed, + expanded).
```

Common types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`.

See [references/markdown-callouts.md](references/markdown-callouts.md) for the full list with aliases, nesting, and custom CSS callouts.

### Properties (Frontmatter)

```yaml
---
title: My Note
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - Alternative Name
cssclasses:
  - custom-class
---
```

Default properties: `tags` (searchable labels), `aliases` (alternative note names for link suggestions), `cssclasses` (CSS classes for styling).

See [references/markdown-properties.md](references/markdown-properties.md) for all property types, tag syntax rules, and advanced usage.

### Tags

```markdown
#tag                    Inline tag
#nested/tag             Nested tag with hierarchy
```

Tags can contain letters, numbers (not first character), underscores, hyphens, and forward slashes. Tags can also be defined in frontmatter under the `tags` property.

### Other Obsidian Syntax

- **Comments**: `%%hidden text%%` (inline) or `%%\nblock\n%%` (block, hidden in reading view)
- **Highlighting**: `==highlighted text==`
- **Math (LaTeX)**: Inline `$e^{i\pi} + 1 = 0$`, block `$$\frac{a}{b} = c$$`
- **Mermaid diagrams**: Use ` ```mermaid ` code blocks. Link nodes to notes with `class NodeName internal-link;`
- **Footnotes**: `Text[^1]` with `[^1]: Content.` or inline `^[This is inline.]`

### Complete Example

````markdown
---
title: Project Alpha
date: 2024-01-15
tags: [project, active]
status: in-progress
---
# Project Alpha
This project aims to [[improve workflow]] using modern techniques.

> [!important] Key Deadline
> The first milestone is due on ==January 30th==.

- [x] Initial planning
- [ ] Development phase

The algorithm uses $O(n \log n)$ sorting. See [[Algorithm Notes#Sorting]] for details.
![[Architecture Diagram.png|600]]
````

Official docs: [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown), [Links](https://help.obsidian.md/links), [Embeds](https://help.obsidian.md/embeds), [Callouts](https://help.obsidian.md/callouts), [Properties](https://help.obsidian.md/properties)

---

## Obsidian Bases

### Workflow

1. **Create the file**: Create a `.base` file in the vault with valid YAML content
2. **Define scope**: Add `filters` to select which notes appear (by tag, folder, property, or date)
3. **Add formulas** (optional): Define computed properties in the `formulas` section
4. **Configure views**: Add one or more views (`table`, `cards`, `list`, or `map`) with `order` specifying which properties to display
5. **Validate**: Verify the file is valid YAML with no syntax errors. Check that all referenced properties and formulas exist. Common issues: unquoted strings containing special YAML characters, mismatched quotes in formula expressions, referencing `formula.X` without defining `X` in `formulas`
6. **Test in Obsidian**: Open the `.base` file in Obsidian to confirm the view renders correctly. If it shows a YAML error, check quoting rules below

### Schema

Base files use the `.base` extension and contain valid YAML.

```yaml
# Global filters apply to ALL views in the base
filters:
  and: []
  or: []
  not: []

# Define formula properties that can be used across all views
formulas:
  formula_name: 'expression'

# Configure display names and settings for properties
properties:
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"
  file.ext:
    displayName: "Extension"

# Define custom summary formulas
summaries:
  custom_summary_name: 'values.mean().round(3)'

# Define one or more views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10                    # Optional: limit results
    groupBy:                     # Optional: group results
      property: property_name
      direction: ASC | DESC
    filters:                     # View-specific filters
      and: []
    order:                       # Properties to display in order
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # Map properties to summary formulas
      property_name: Average
```

### Filter Syntax

Filters narrow down results. They can be applied globally or per-view.

```yaml
# Single filter
filters: 'status == "done"'

# AND - all conditions must be true
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

# OR - any condition can be true
filters:
  or:
    - 'file.hasTag("book")'
    - 'file.hasTag("article")'

# NOT - exclude matching items
filters:
  not:
    - 'file.hasTag("archived")'

# Nested: combine and/or/not
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
```

**Filter Operators:** `==` (equals), `!=` (not equal), `>`, `<`, `>=`, `<=`, `&&` (logical and), `||` (logical or), `!` (logical not)

### Properties

**Three types:**
1. **Note properties** - From frontmatter: `note.author` or just `author`
2. **File properties** - File metadata: `file.name`, `file.mtime`, etc.
3. **Formula properties** - Computed values: `formula.my_formula`

**File Properties Reference:**

| Property | Type | Description |
|----------|------|-------------|
| `file.name` | String | File name |
| `file.basename` | String | File name without extension |
| `file.path` | String | Full path to file |
| `file.folder` | String | Parent folder path |
| `file.ext` | String | File extension |
| `file.size` | Number | File size in bytes |
| `file.ctime` | Date | Created time |
| `file.mtime` | Date | Modified time |
| `file.tags` | List | All tags in file |
| `file.links` | List | Internal links in file |
| `file.backlinks` | List | Files linking to this file |
| `file.embeds` | List | Embeds in the note |
| `file.properties` | Object | All frontmatter properties |

**The `this` Keyword:** In main content area refers to the base file itself. When embedded, refers to the embedding file. In sidebar, refers to the active file.

### Formula Syntax

Formulas compute values from properties. Defined in the `formulas` section.

```yaml
formulas:
  total: "price * quantity"
  status_icon: 'if(done, "✅", "⏳")'
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'
  created: 'file.ctime.format("YYYY-MM-DD")'
  days_old: '(now() - file.ctime).days'
  days_until_due: 'if(due_date, (date(due_date) - today()).days, "")'
```

### Key Functions

Most commonly used functions. For the complete reference of all types (Date, String, Number, List, File, Link, Object, RegExp), see [references/bases-functions.md](references/bases-functions.md).

| Function | Signature | Description |
|----------|-----------|-------------|
| `date()` | `date(string): date` | Parse string to date (`YYYY-MM-DD HH:mm:ss`) |
| `now()` | `now(): date` | Current date and time |
| `today()` | `today(): date` | Current date (time = 00:00:00) |
| `if()` | `if(condition, trueResult, falseResult?)` | Conditional |
| `duration()` | `duration(string): duration` | Parse duration string |
| `file()` | `file(path): file` | Get file object |
| `link()` | `link(path, display?): Link` | Create a link |

**Duration Type:** When subtracting two dates, the result is a **Duration** type (not a number). Fields: `.days`, `.hours`, `.minutes`, `.seconds`, `.milliseconds`. Duration does NOT support `.round()`, `.floor()`, `.ceil()` directly — access a numeric field first, then apply number functions.

```yaml
# CORRECT
"(date(due_date) - today()).days"                    # Returns number of days
"(now() - file.ctime).days.round(0)"                # Rounded days

# WRONG - will cause error:
# "((date(due) - today()) / 86400000).round(0)"      # Duration doesn't support division
```

**Date Arithmetic:** Duration units: `y/year/years`, `M/month/months`, `d/day/days`, `w/week/weeks`, `h/hour/hours`, `m/minute/minutes`, `s/second/seconds`.

### View Types

**Table** is the most common view type:

```yaml
views:
  - type: table
    name: "My Table"
    order:
      - file.name
      - status
      - due_date
    summaries:
      price: Sum
      count: Average
```

Other view types: **Cards** (gallery/card layout), **List** (simple list), **Map** (requires lat/lng properties and Maps community plugin). All use the same `order`, `filters`, `groupBy`, and `summaries` options.

### Default Summary Formulas

| Name | Input Type | Description |
|------|------------|-------------|
| `Average` | Number | Mathematical mean |
| `Min` / `Max` / `Sum` / `Range` / `Median` / `Stddev` | Number | Standard aggregations |
| `Earliest` / `Latest` | Date | Date range |
| `Checked` / `Unchecked` | Boolean | Count of true/false values |
| `Empty` / `Filled` / `Unique` | Any | Count of empty, non-empty, or unique values |

For complete examples (Task Tracker, Reading List, Daily Notes Index), see [references/bases-examples.md](references/bases-examples.md).

### Embedding Bases

```markdown
![[MyBase.base]]
![[MyBase.base#View Name]]
```

### YAML Quoting Rules

- Use single quotes for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Use double quotes for simple strings: `"My View Name"`
- Escape nested quotes properly in complex expressions

### Troubleshooting

- **Unquoted special chars**: Strings with `:`, `{`, `}`, `[`, `]`, etc. must be quoted. E.g. `displayName: "Status: Active"`
- **Mismatched quotes**: Formulas with double quotes must be wrapped in single quotes
- **Duration math**: Subtracting dates returns Duration, not a number — always access `.days`, `.hours`, etc. first
- **Missing null checks**: Use `if()` to guard: `'if(due_date, (date(due_date) - today()).days, "")'`
- **Undefined formulas**: Every `formula.X` in `order`/`properties` needs a matching `formulas` entry

Official docs: [Bases Syntax](https://help.obsidian.md/bases/syntax), [Functions](https://help.obsidian.md/bases/functions), [Views](https://help.obsidian.md/bases/views). Full function reference: [references/bases-functions.md](references/bases-functions.md).

---

## Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

### Command reference

Run `obsidian help` to see all available commands. This is always up to date. Full docs: https://help.obsidian.md/cli

### Syntax

**Parameters** use `=`: `obsidian create name="My Note" content="Hello world"`. Quote values with spaces.
**Flags** are boolean switches: `obsidian create name="My Note" silent overwrite`. Use `\n` for newlines, `\t` for tabs.

### Targeting

- **File**: `file=<name>` (resolves like wikilink) or `path=<path>` (exact vault-root path). Without either, targets the active file.
- **Vault**: `vault=<name>` as first parameter targets a specific vault (defaults to most recently focused).

### Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

### Plugin development

After making code changes to a plugin or theme:

```bash
obsidian plugin:reload id=my-plugin          # 1. Reload plugin
obsidian dev:errors                          # 2. Check for errors
obsidian dev:screenshot path=screenshot.png  # 3. Verify visually
obsidian dev:dom selector=".workspace-leaf" text
obsidian dev:console level=error             # 4. Check console output
```

Additional developer commands:

```bash
obsidian eval code="app.vault.getFiles().length"       # Run JavaScript
obsidian dev:css selector=".workspace-leaf" prop=background-color  # Inspect CSS
obsidian dev:mobile on                                  # Toggle mobile emulation
```

Run `obsidian help` for additional developer commands including CDP and debugger controls.

---

## Web Clipper Templates

This section helps you create importable JSON templates for the Obsidian Web Clipper.

### Workflow

1. **Identify User Intent:** specific site (YouTube), specific type (Recipe), or general clipping?
2. **Check Existing Bases:** Read `Bases/*.base` to find a matching category and use its properties to structure the template. See [references/clipper-bases-workflow.md](references/clipper-bases-workflow.md).
3. **Fetch & Analyze Reference URL:** **(REQUIRED)** Use **WebFetch** to retrieve page content. Analyze HTML for Schema.org JSON-LD, Meta tags, and CSS selectors. Verify each selector against the fetched content — never guess selectors. See [references/clipper-analysis-workflow.md](references/clipper-analysis-workflow.md).
4. **Draft the JSON:** Create a valid JSON object per [references/clipper-json-schema.md](references/clipper-json-schema.md).
5. **Consider template logic:** Conditionals, loops, variable assignment, and fallbacks. Keep simple templates simple. See [references/clipper-logic.md](references/clipper-logic.md).
6. **Verify Variables:** Ensure chosen variables (Preset, Schema, Selector) exist in your analysis. If a selector cannot be verified, state that explicitly and ask for another URL. See [references/clipper-variables.md](references/clipper-variables.md).

### Selector Verification Rules

- **Always verify selectors** against live page content before responding.
- **Never guess selectors.** If the DOM cannot be accessed or the element is missing, ask for another URL or a screenshot.
- **Prefer stable selectors** (data attributes, semantic roles, unique IDs) over fragile class chains.
- **Document the target element** in your reasoning (e.g., "About sidebar paragraph") to reduce mismatch.

### Output Format

**ALWAYS** output the final result as a JSON code block that the user can copy and import.

The Clipper template editor validates template syntax.
If you use template logic (conditionals, loops, variable assignment), ensure it follows the syntax in [references/clipper-logic.md](references/clipper-logic.md) and the official [Logic](https://help.obsidian.md/web-clipper/logic) docs so the template passes validation.

```json
{
  "schemaVersion": "0.1.0",
  "name": "My Template",
  ...
}
```

### Clipper Resources

References: [variables](references/clipper-variables.md), [filters](references/clipper-filters.md), [json-schema](references/clipper-json-schema.md), [logic](references/clipper-logic.md), [bases-workflow](references/clipper-bases-workflow.md), [analysis-workflow](references/clipper-analysis-workflow.md). Example templates: [assets/](assets/).

Official docs: [Variables](https://help.obsidian.md/web-clipper/variables), [Filters](https://help.obsidian.md/web-clipper/filters), [Logic](https://help.obsidian.md/web-clipper/logic), [Templates](https://help.obsidian.md/web-clipper/templates)
