# mcp-toolkit

Claude Code skills for building **MCP Apps** (interactive UIs for MCP tools) and packaging **MCPB** desktop extensions (single-click installation in Claude Desktop).

## Skills

### MCP Apps — Interactive UIs

| Skill | Use when... |
|-------|-------------|
| `create-mcp-app` | Building a new MCP server with an interactive UI from scratch |
| `add-app-to-server` | Adding a UI to tools on an existing MCP server |
| `convert-web-app` | Making an existing web app work as both a standalone site and an MCP App |
| `migrate-oai-app` | Migrating from the OpenAI Apps SDK to the MCP Apps SDK |

### MCPB — Desktop Extensions

| Skill | Use when... |
|-------|-------------|
| `build-mcpb` | Packaging a local MCP server as a `.mcpb` bundle for single-click install |
| `mcpb-manifest` | Configuring `manifest.json` — field reference, `user_config`, server types, variables |

## Capability Domains

**MCP Apps** (`@modelcontextprotocol/ext-apps`) — Add interactive HTML UIs to MCP tools. The UI renders inline in Claude Desktop when the tool is called. Requires a build step (Vite + vite-plugin-singlefile).

**MCPB** (`.mcpb` bundles) — Package a local MCP server and all its dependencies into a zip archive for single-click installation. Uses the `@anthropic-ai/mcpb` CLI.

These are complementary: you can build an MCP server with interactive UIs and then package it as an MCPB for distribution.
