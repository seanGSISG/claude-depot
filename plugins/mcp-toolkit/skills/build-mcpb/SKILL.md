---
name: build-mcpb
description: This skill should be used when the user asks to "build an MCPB", "create a desktop extension", "package an MCP server", "create an mcpb file", "distribute an MCP server", "bundle my MCP server", "create a local MCP extension", "make an MCP Bundle", or needs guidance on packaging a local MCP server for single-click installation in Claude Desktop. Covers the full workflow from project setup through packing, testing, and signing.
---

# Build an MCP Bundle (MCPB)

MCP Bundles (`.mcpb`) are zip archives containing a local MCP server and a `manifest.json`. They enable single-click installation in Claude Desktop, similar to browser extensions (`.crx`, `.vsix`).

## When to Use MCPB vs. Remote Connector

**Choose MCPB (local server) for:**
- Access to systems behind your firewall (JIRA, internal wikis, private databases)
- Direct filesystem access, local tool integration (Docker, IDEs, databases)
- Seamless auth via existing SSO/browser sessions — no token management
- Works offline; no cloud infrastructure or VPN required
- Enterprise: one-click install with bundled runtime, admin-controlled allowlists

**Choose a remote connector for:**
- Cloud services and public APIs requiring centralized infrastructure
- Distribution across Claude Web, mobile, and desktop
- OAuth flows requiring server-side token management
- Public-facing integrations used by multiple organizations

## Platform Support

Claude Desktop runs on **macOS** (`darwin`) and **Windows** (`win32`). Declare supported platforms in `manifest.json`'s `compatibility` section. Best practice: test on both platforms even if you develop on one.

## Five-Step Build Process

### Step 1: Install the MCPB CLI

```bash
npm install -g @anthropic-ai/mcpb
```

### Step 2: Create Your MCP Server

Build a standard MCP server using the MCP SDK (`@modelcontextprotocol/sdk`). The server communicates via **stdio transport** — this is the only transport used in MCPB bundles.

```bash
npm install @modelcontextprotocol/sdk
```

For a Node.js server (`server/index.js`):

```javascript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "my-extension",
  version: "1.0.0",
});

server.tool("my_tool", "Description of what this tool does", {}, async () => {
  return { content: [{ type: "text", text: "Hello from MCPB!" }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

For a Python server (`server/main.py`):

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-extension")

@mcp.tool()
def my_tool() -> str:
    """Description of what this tool does"""
    return "Hello from MCPB!"

if __name__ == "__main__":
    mcp.run()
```

### Step 3: Initialize the Manifest

Run in your project directory:

```bash
mcpb init
```

The interactive wizard prompts for:
- Extension name, author, version, description
- Server type (Node.js, Python, or Binary)
- Entry point path
- Tools configuration
- Keywords, license, repository

This creates `manifest.json`. You can also create it manually — see the **mcpb-manifest** skill for the full spec.

### Step 4: Pack the Bundle

```bash
# Pack current directory (outputs <name>.mcpb)
mcpb pack .

# Pack with custom output filename
mcpb pack . my-extension-v1.0.mcpb
```

`mcpb pack` automatically:
- Validates `manifest.json`
- Excludes common dev files (`.git`, `node_modules/.cache`, `.DS_Store`, etc.)
- Creates a compressed `.mcpb` ZIP file

### Step 5: Install and Test in Claude Desktop

**Three installation methods:**
1. Double-click the `.mcpb` file
2. Drag-and-drop into the Claude Desktop window
3. File menu → Developer → Extensions → Install Extension → select `.mcpb`

All methods open an installation UI where users review details, configure settings, and grant permissions.

## Directory Structures

### Node.js Bundle

```
my-extension/
├── manifest.json         # Required: metadata and configuration
├── server/
│   └── index.js          # Main entry point
├── node_modules/         # Bundled dependencies (run npm install first)
├── package.json
└── icon.png              # Optional: 512x512 PNG
```

### Python Bundle (with bundled deps)

```
my-extension/
├── manifest.json
├── server/
│   ├── main.py
│   └── lib/              # Bundled packages (pip install --target server/lib .)
└── icon.png
```

### Python Bundle (with uv — experimental, manifest v0.4)

```
my-extension/
├── manifest.json         # server.type = "uv"
├── pyproject.toml        # Dependencies declared here
├── src/
│   └── server.py
└── .mcpbignore           # Exclude .venv, __pycache__, etc.
```

The `uv` type is experimental (v0.4+). The host manages Python installation — small bundle size (~100 KB vs 5–10 MB for bundled deps).

## CLI Command Reference

| Command | Description |
|---------|-------------|
| `mcpb init [dir]` | Interactive manifest creation wizard |
| `mcpb validate <path>` | Validate manifest.json against schema |
| `mcpb pack <dir> [output]` | Pack directory into .mcpb file |
| `mcpb sign <file>` | Sign .mcpb with X.509 certificate |
| `mcpb verify <file>` | Verify signature of signed .mcpb |
| `mcpb info <file>` | Show file size and signature details |
| `mcpb unsign <file>` | Remove signature (dev/testing) |

### Validate Before Packing

```bash
mcpb validate manifest.json
# or
mcpb validate .
```

### Signing (Optional but Recommended for Distribution)

```bash
# Self-signed (development/testing)
mcpb sign my-extension.mcpb --self-signed

# Production (with CA certificate)
mcpb sign my-extension.mcpb \
  --cert production-cert.pem \
  --key production-key.pem \
  --intermediate intermediate-ca.pem

# Verify after signing
mcpb verify my-extension.mcpb
```

## Custom Exclusions with .mcpbignore

Create `.mcpbignore` to exclude additional files from the bundle:

```
# .mcpbignore
*.test.js
src/**/*.test.ts
coverage/
docs/
.env*
temp/
```

## Development Workflow

```bash
# 1. Develop your MCP server
mkdir my-extension && cd my-extension

# 2. Initialize
mcpb init

# 3. Implement server code

# 4. For Node.js: install and bundle dependencies
npm install

# 5. Validate
mcpb validate .

# 6. Pack
mcpb pack .

# 7. Install in Claude Desktop (double-click the .mcpb file)

# 8. Test tools via Claude Desktop
```

## User Configuration

If your server needs user-provided values (API keys, directories, settings), define `user_config` in `manifest.json`. Claude Desktop auto-generates a settings UI. Reference values via `${user_config.KEY}` in `mcp_config.args` or `mcp_config.env`.

See the **mcpb-manifest** skill for full `user_config` schema and examples.

## Submitting to Anthropic Directory

To distribute via the Anthropic Connectors Directory, additional requirements apply:
- Mandatory tool annotations for all tools
- Minimum three working examples
- Testing credentials (if applicable)

See [Local MCP Server Submission Guide](https://support.claude.com/en/articles/12922832-local-mcp-server-submission-guide).
