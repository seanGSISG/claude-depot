# claude-depot

A curated depot of Claude Code plugins — skills, tools, and extensions.

## Install

### Claude Code (recommended)

```
/plugin marketplace add seanGSISG/claude-depot
/plugin install <plugin-name>@claude-depot
```

### Claude.ai / Claude Desktop

Download a `.skill` file from the table below, then upload via **Settings > Skills**.

## Plugins

| Plugin | Description | .skill Download | Install |
|---|---|---|---|
| **trmm-expert** | Tactical RMM documentation expert | [trmm-expert.skill][trmm-expert] | `/plugin install trmm-expert@claude-depot` |
| **claude-docs** | Anthropic docs search (573 paths) | [docs.skill][docs] | `/plugin install claude-docs@claude-depot` |
| **skill-creator-enhanced** | Skill creation guide with validators | [skill-creator-enhanced.skill][skill-creator] | `/plugin install skill-creator-enhanced@claude-depot` |
| **rules-auditor** | Audit rules for staleness and quality | [rules-auditor.skill][rules-auditor] | `/plugin install rules-auditor@claude-depot` |
| **continual-learning** | Cross-session memory via hooks | _(hooks only)_ | `/plugin install continual-learning@claude-depot` |
| **obsidian** | Markdown, Bases, CLI, Web Clipper | [obsidian.skill][obsidian] | `/plugin install obsidian@claude-depot` |
| **plan-to-vault** | Archive plans to Obsidian vault | [setup.skill][ptv-setup] / [import-plans.skill][ptv-import] | `/plugin install plan-to-vault@claude-depot` |

[trmm-expert]: https://github.com/seanGSISG/claude-depot/releases/download/latest/trmm-expert.skill
[docs]: https://github.com/seanGSISG/claude-depot/releases/download/latest/docs.skill
[skill-creator]: https://github.com/seanGSISG/claude-depot/releases/download/latest/skill-creator-enhanced.skill
[rules-auditor]: https://github.com/seanGSISG/claude-depot/releases/download/latest/rules-auditor.skill
[obsidian]: https://github.com/seanGSISG/claude-depot/releases/download/latest/obsidian.skill
[ptv-setup]: https://github.com/seanGSISG/claude-depot/releases/download/latest/setup.skill
[ptv-import]: https://github.com/seanGSISG/claude-depot/releases/download/latest/import-plans.skill

<details>
<summary><strong>mcp-toolkit</strong> — MCP Apps & MCPB builder (6 skills)</summary>

| Skill | Download |
|---|---|
| create-mcp-app | [create-mcp-app.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/create-mcp-app.skill) |
| add-app-to-server | [add-app-to-server.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/add-app-to-server.skill) |
| convert-web-app | [convert-web-app.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/convert-web-app.skill) |
| migrate-oai-app | [migrate-oai-app.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/migrate-oai-app.skill) |
| build-mcpb | [build-mcpb.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/build-mcpb.skill) |
| mcpb-manifest | [mcpb-manifest.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/mcpb-manifest.skill) |

`/plugin install mcp-toolkit@claude-depot`

</details>

<details>
<summary><strong>vault-tools</strong> — Obsidian vault management (8 skills)</summary>

| Skill | Download |
|---|---|
| new-note | [new-note.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/new-note.skill) |
| vault-search | [vault-search.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/vault-search.skill) |
| process-inbox | [process-inbox.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/process-inbox.skill) |
| auto-categorize | [auto-categorize.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/auto-categorize.skill) |
| vault-stats | [vault-stats.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/vault-stats.skill) |
| vault-maintenance | [vault-maintenance.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/vault-maintenance.skill) |
| reclassify | [reclassify.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/reclassify.skill) |
| weekly-review | [weekly-review.skill](https://github.com/seanGSISG/claude-depot/releases/download/latest/weekly-review.skill) |

`/plugin install vault-tools@claude-depot`

</details>

## Contributing

Add plugins under `plugins/`, validate with `quick_validate.py`. See `CLAUDE.md` for conventions.

## License

MIT
