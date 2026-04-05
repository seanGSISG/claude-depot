# obsidian

Comprehensive Obsidian skill covering Markdown (wikilinks, callouts, embeds, properties), Bases (`.base` files, formulas, views), CLI, and Web Clipper templates.

## What It Does

Provides Claude with deep knowledge of Obsidian's syntax and features so it can generate correct Obsidian-flavored Markdown, create `.base` files with formulas, build Web Clipper templates, and use the Obsidian CLI. The skill routes to the appropriate reference documentation based on the user's question.

## Coverage

- **Markdown** — wikilinks, callouts, embeds, properties, tags, advanced formatting
- **Bases** — `.base` file syntax, formulas, functions, views (table, list, cards, map)
- **Web Clipper** — template variables, filters, logic, JSON schema, workflows
- **CLI** — `obsidian-cli` commands, headless mode, Obsidian URI scheme
- **CSS snippets** — custom styling via `.css` files

## Setup

```
/plugin install obsidian@claude-depot
```

No configuration required. The skill is available immediately after installation.

## Reference Structure

The skill includes 44 reference files organized in two tiers:

- `references/*.md` — custom synthesized references (Bases functions, examples, Clipper workflows, Markdown guides)
- `references/official/` — official Obsidian documentation organized by category (bases, editing, linking, extending, web-clipper)

Claude loads references on demand based on the user's question topic, keeping context usage efficient.
