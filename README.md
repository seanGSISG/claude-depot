# claude-depot

A curated depot of Claude Code plugins — skills, tools, and extensions.

## Installation

### Via Claude Code Plugin Marketplace

Add the marketplace, then install any plugin:

```
/plugin marketplace add seanGSISG/claude-depot
/plugin install trmm-expert@claude-depot
```

### Direct Download (.skill files)

For use in **Claude.ai** or **Claude Desktop**, download pre-built `.skill` files from [GitHub Releases](https://github.com/seanGSISG/claude-depot/releases):

1. Go to the [latest release](https://github.com/seanGSISG/claude-depot/releases/latest)
2. Download the `.skill` file for the plugin you want
3. Upload it to Claude.ai (Settings > Skills) or Claude Desktop

`.skill` files are validated ZIP archives containing the skill and all its reference files. They work identically to plugin-installed skills.

## Available Plugins

### trmm-expert

Tactical RMM documentation expert — answers questions about architecture, agents, scripting, checks/tasks, alerting, API, settings, reporting, SSO, integrations, and troubleshooting.

**What it provides:**
- Expert-level answers from the complete TRMM documentation (46 source files)
- 9 consolidated reference files organized by topic domain
- Intelligent routing that loads only the relevant reference(s) per question
- Quick-reference syntax guide for script variables, custom fields, data queries

**Triggers when you ask about:**
- TRMM architecture, installation, agent deployment
- Scripting (PowerShell/Python/Bash/Deno), script variables, custom fields
- Checks, tasks, automation policies, alerting, webhooks
- REST API, global settings, permissions, management commands
- Reporting and SSO (Enterprise Edition)
- Third-party integrations (Bitdefender, Zammad), SNMP, troubleshooting

### claude-docs

AI-powered search and access to 573 Anthropic documentation paths — Claude Code CLI, API, Agent SDK, prompt library, and more.

**What it provides:**
- Full-text content search and fuzzy path search across 571 locally mirrored documentation files
- Automatic sync via SessionStart hook (clones/pulls from seanGSISG/claude-code-docs)
- Category-aware results with product context (Claude Code CLI, Claude API, Agent SDK, etc.)
- Graceful degradation — works with or without Python 3.9+

**Triggers when you ask about:**
- Claude Code CLI features (hooks, skills, MCP, memory, plugins, settings)
- Claude API (messages, batches, files, models, admin, multi-language SDKs)
- Agent SDK (Python/TypeScript, sessions, subagents, custom tools)
- Prompt engineering, tool use, streaming, extended thinking, vision
- Any Anthropic platform documentation

```
/plugin install claude-docs@claude-depot
```

### skill-creator-enhanced

Guide for creating effective Claude Code skills with templates, validators, and packaging tools.

**What it provides:**
- 6-step skill creation workflow (understand > plan > init > edit > package > iterate)
- Python scripts for initializing, validating, and packaging skills
- Reference docs on workflow patterns and output patterns
- Progressive disclosure design principles

**Triggers when you:**
- Ask to create a new skill
- Want to update or improve an existing skill
- Need help structuring a skill's resources

## Contributing

To add a new plugin, create a subdirectory under `plugins/` with a `.claude-plugin/plugin.json` manifest and add an entry to the root `marketplace.json`.

See `CLAUDE.md` for development conventions and the release workflow.

## License

MIT
