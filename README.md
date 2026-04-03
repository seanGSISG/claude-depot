# claude-depot

A curated depot of Claude Code plugins — skills, tools, and extensions.

## Install

### Claude Code (recommended)

```
/plugin marketplace add seanGSISG/claude-depot
/plugin install <plugin-name>@claude-depot
```

### Claude.ai / Claude Desktop

Download a `.skill` file from the table below, then upload via **Settings > Features > Skills**.

## Plugins

### With .skill downloads (work in Claude.ai)

| Plugin | Description | .skill Download |
|---|---|---|
| **trmm-expert** | Tactical RMM documentation expert | [trmm-expert.skill][trmm-expert] |
| **claude-docs** | Anthropic docs search (573 paths) | [docs.skill][docs] |
| **skill-creator-enhanced** | Skill creation guide with validators | [skill-creator-enhanced.skill][skill-creator] |
| **rules-auditor** | Audit rules for staleness and quality | [rules-auditor.skill][rules-auditor] |
| **obsidian** | Markdown, Bases, CLI, Web Clipper | [obsidian.skill][obsidian] |

[trmm-expert]: https://github.com/seanGSISG/claude-depot/releases/download/latest/trmm-expert.skill
[docs]: https://github.com/seanGSISG/claude-depot/releases/download/latest/docs.skill
[skill-creator]: https://github.com/seanGSISG/claude-depot/releases/download/latest/skill-creator-enhanced.skill
[rules-auditor]: https://github.com/seanGSISG/claude-depot/releases/download/latest/rules-auditor.skill
[obsidian]: https://github.com/seanGSISG/claude-depot/releases/download/latest/obsidian.skill

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

</details>

### Claude Code only (require hooks/scripts)

These plugins use hooks and scripts that only work when installed via `/plugin install`:

| Plugin | Description | Install |
|---|---|---|
| **continual-learning** | Cross-session memory via hooks | `/plugin install continual-learning@claude-depot` |
| **plan-to-vault** | Archive plans to Obsidian vault | `/plugin install plan-to-vault@claude-depot` |
| **vault-tools** | Obsidian vault management (9 skills) | `/plugin install vault-tools@claude-depot` |

## Contributing

Add plugins under `plugins/`, validate with `quick_validate.py`. See `CLAUDE.md` for conventions.

## License

MIT
