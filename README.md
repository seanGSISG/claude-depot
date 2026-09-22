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
| **claude-docs** | Anthropic docs search (Claude Code, API, Agent SDK) | [docs.skill][docs] |
| **rules-auditor** | Audit rules for staleness and quality | [rules-auditor.skill][rules-auditor] |

[trmm-expert]: https://github.com/seanGSISG/claude-depot/releases/download/latest/trmm-expert.skill
[docs]: https://github.com/seanGSISG/claude-depot/releases/download/latest/docs.skill
[rules-auditor]: https://github.com/seanGSISG/claude-depot/releases/download/latest/rules-auditor.skill

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
| **cache-cleanup** | Prune old cached plugin versions | `/plugin install cache-cleanup@claude-depot` |
| **ultra-research** | Human-in-the-loop deep research pipeline (5 skills + web-search agent) | `/plugin install ultra-research@claude-depot` |
| **pre-pr-review** | Pre-PR review of the current branch by a second model family, via the [deep-review](https://github.com/seanGSISG/deep-review) CLI | `/plugin install pre-pr-review@claude-depot` |

## Contributing

Add plugins under `plugins/`, validate with `quick_validate.py`. See `CLAUDE.md` for conventions.

## License

MIT
