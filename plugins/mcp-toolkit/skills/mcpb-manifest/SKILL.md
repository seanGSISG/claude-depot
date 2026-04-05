---
name: mcpb-manifest
description: This skill should be used when the user asks to "configure manifest.json", "mcpb manifest spec", "manifest.json fields", "user_config in mcpb", "mcpb icon configuration", "set up manifest for desktop extension", "mcpb compatibility settings", "mcpb server types", "mcp_config variables", or needs detailed reference for the manifest.json file used in MCPB desktop extensions. Provides the complete field reference, user_config schema, server type examples, and variable substitution patterns.
---

## Table of Contents

- [Minimal manifest.json](#minimal-manifestjson)
- [Required Fields](#required-fields)
- [Server Configuration](#server-configuration)
  - [Server Types](#server-types)
  - [mcp_config](#mcp_config)
  - [Variable Substitution in mcp_config](#variable-substitution-in-mcp_config)
  - [Platform-Specific Overrides](#platform-specific-overrides)
- [User Configuration](#user-configuration)
  - [Configuration Field Schema](#configuration-field-schema)
  - [All Config Types Example](#all-config-types-example)
  - [Referencing user_config Values](#referencing-user_config-values)
- [Optional Metadata Fields](#optional-metadata-fields)
- [Icons](#icons)
- [Compatibility](#compatibility)
- [Full Example manifest.json](#full-example-manifestjson)
- [Validate Your Manifest](#validate-your-manifest)
- [Localization](#localization)

# MCPB manifest.json Reference

The `manifest.json` file is the required metadata descriptor for every MCPB bundle. It tells Claude Desktop what the extension does, how to run it, what tools it provides, and what configuration it needs.

Current spec version: **0.3** (use `"manifest_version": "0.3"`)

## Minimal manifest.json

The five required fields:

```json
{
  "manifest_version": "0.3",
  "name": "my-extension",
  "version": "1.0.0",
  "description": "A brief description of what this extension does",
  "author": {
    "name": "Your Name"
  },
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"]
    }
  }
}
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `manifest_version` | string | Always `"0.3"` (current spec version) |
| `name` | string | Machine-readable identifier (used in CLI and APIs) |
| `version` | string | Semantic version (e.g., `"1.0.0"`) |
| `description` | string | Brief description shown in installation UI |
| `author.name` | string | Author's name (required within author object) |
| `server` | object | How to run the MCP server (see Server Configuration) |

## Server Configuration

### Server Types

| Type | Description |
|------|-------------|
| `"node"` | Node.js server; bundle `node_modules/` with the extension |
| `"python"` | Python server; bundle deps in `server/lib/` or `server/venv/` |
| `"binary"` | Pre-compiled executable, fully self-contained |
| `"uv"` | Python with UV runtime — experimental (v0.4+), small bundles |

### mcp_config

Defines the command Claude Desktop runs to start the server:

```json
"server": {
  "type": "node",
  "entry_point": "server/index.js",
  "mcp_config": {
    "command": "node",
    "args": ["${__dirname}/server/index.js"],
    "env": {
      "API_KEY": "${user_config.api_key}"
    }
  }
}
```

**Python example:**
```json
"server": {
  "type": "python",
  "entry_point": "server/main.py",
  "mcp_config": {
    "command": "python",
    "args": ["${__dirname}/server/main.py"],
    "env": {
      "PYTHONPATH": "${__dirname}/server/lib"
    }
  }
}
```

**UV example (v0.4+):**
```json
"server": {
  "type": "uv",
  "entry_point": "src/server.py"
}
```
UV type: `mcp_config` is optional — host manages execution via `pyproject.toml`.

### Variable Substitution in mcp_config

| Variable | Replaced with |
|----------|---------------|
| `${__dirname}` | Absolute path to the extension's install directory |
| `${HOME}` | User's home directory |
| `${DESKTOP}` | User's desktop directory |
| `${DOCUMENTS}` | User's documents directory |
| `${DOWNLOADS}` | User's downloads directory |
| `${pathSeparator}` or `${/}` | Platform path separator |
| `${user_config.KEY}` | User-provided value for config key KEY |

### Platform-Specific Overrides

```json
"mcp_config": {
  "command": "server/my-server",
  "args": ["--config", "server/config.json"],
  "env": {},
  "platform_overrides": {
    "win32": {
      "command": "server/my-server.exe",
      "args": ["--config", "server/config-windows.json"]
    },
    "darwin": {
      "env": {
        "DYLD_LIBRARY_PATH": "server/lib"
      }
    }
  }
}
```

Note: For binary type, Claude Desktop automatically appends `.exe` on Windows.

## User Configuration

`user_config` defines settings that Claude Desktop collects from the user via an auto-generated settings UI, then passes to your server at runtime.

### Configuration Field Schema

Each key in `user_config` supports:

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | `"string"`, `"boolean"`, `"number"`, `"file"`, `"directory"` |
| `title` | string | Label shown in the UI |
| `description` | string | Help text shown in the UI |
| `required` | boolean | Whether user must provide a value (default: `false`) |
| `default` | any | Default value (supports `${HOME}`, `${DESKTOP}`, `${DOCUMENTS}`) |
| `sensitive` | boolean | Mask input and store securely — for API keys/passwords (string only) |
| `multiple` | boolean | Allow multiple selections — for file/directory types (default: `false`) |
| `min` / `max` | number | Validation bounds — for number type only |

### All Config Types Example

```json
"user_config": {
  "api_key": {
    "type": "string",
    "title": "API Key",
    "description": "Your authentication key",
    "sensitive": true,
    "required": true
  },
  "verbose_logging": {
    "type": "boolean",
    "title": "Verbose Logging",
    "description": "Enable detailed logging",
    "default": false
  },
  "max_results": {
    "type": "number",
    "title": "Maximum Results",
    "description": "Max items to return",
    "default": 10,
    "min": 1,
    "max": 100
  },
  "config_file": {
    "type": "file",
    "title": "Configuration File",
    "description": "Path to a JSON config file",
    "required": false
  },
  "allowed_directories": {
    "type": "directory",
    "title": "Allowed Directories",
    "description": "Directories the server can access",
    "multiple": true,
    "required": true,
    "default": ["${HOME}/Desktop", "${HOME}/Documents"]
  }
}
```

### Referencing user_config Values

In `mcp_config.args`:
```json
"args": [
  "${__dirname}/server/index.js",
  "--max=${user_config.max_results}",
  "${user_config.allowed_directories}"
]
```

In `mcp_config.env`:
```json
"env": {
  "API_KEY": "${user_config.api_key}",
  "DEBUG": "${user_config.verbose_logging}"
}
```

**Array expansion**: When `multiple: true`, `"${user_config.allowed_directories}"` expands to separate args: `["/home/user/docs", "/home/user/projects"]`.

## Optional Metadata Fields

| Field | Description |
|-------|-------------|
| `display_name` | Human-friendly name for UI (vs. machine `name`) |
| `long_description` | Detailed description (markdown supported) |
| `author.email` | Author's email |
| `author.url` | Author's website |
| `repository` | `{ "type": "git", "url": "..." }` |
| `homepage` | Extension homepage URL |
| `documentation` | Documentation URL |
| `support` | Issues/support URL |
| `keywords` | Array of search keywords |
| `license` | License identifier (e.g., `"MIT"`) |
| `privacy_policies` | Array of privacy policy URLs — required when connecting to external services |
| `tools` | Array of `{ "name": "...", "description": "..." }` — declares tools for directory listing |
| `tools_generated` | `true` if server generates additional tools at runtime |
| `prompts` | Array of prompt declarations |
| `screenshots` | Array of screenshot paths |

## Icons

**Simple (single icon):**
```json
"icon": "icon.png"
```

**Multiple variants (light/dark, multiple sizes):**
```json
"icons": [
  { "src": "assets/icon-16-light.png", "size": "16x16", "theme": "light" },
  { "src": "assets/icon-16-dark.png",  "size": "16x16", "theme": "dark" },
  { "src": "assets/icon-128.png",      "size": "128x128" }
]
```

Icon requirements: PNG format, transparency supported. Recommended: 512×512 main icon.

## Compatibility

All fields optional — omit to support all platforms/runtimes:

```json
"compatibility": {
  "claude_desktop": ">=1.0.0",
  "platforms": ["darwin", "win32"],
  "runtimes": {
    "node": ">=16.0.0"
  }
}
```

| Field | Values |
|-------|--------|
| `claude_desktop` | Semver constraint (e.g., `">=0.10.0"`) |
| `platforms` | `"darwin"` (macOS), `"win32"` (Windows), `"linux"` |
| `runtimes.node` | Semver constraint for Node.js version |
| `runtimes.python` | Semver constraint for Python version |

Binary extensions don't need `runtimes`. If `platforms` is omitted, all platforms are supported.

## Full Example manifest.json

```json
{
  "manifest_version": "0.3",
  "name": "my-extension",
  "display_name": "My Awesome Extension",
  "version": "1.0.0",
  "description": "Does amazing things with your data",
  "long_description": "A detailed description supporting **markdown**.",
  "author": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://your-site.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/you/my-extension.git"
  },
  "homepage": "https://your-site.com/my-extension",
  "documentation": "https://docs.your-site.com/my-extension",
  "support": "https://github.com/you/my-extension/issues",
  "icon": "icon.png",
  "keywords": ["productivity", "api", "automation"],
  "license": "MIT",
  "privacy_policies": ["https://your-site.com/privacy"],
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": [
        "${__dirname}/server/index.js",
        "--workspace=${user_config.workspace_directory}"
      ],
      "env": {
        "API_KEY": "${user_config.api_key}"
      }
    }
  },
  "tools": [
    { "name": "search", "description": "Search your data" },
    { "name": "create_item", "description": "Create a new item" }
  ],
  "user_config": {
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key",
      "sensitive": true,
      "required": true
    },
    "workspace_directory": {
      "type": "directory",
      "title": "Workspace",
      "description": "Working directory",
      "default": "${HOME}/Documents",
      "required": false
    }
  },
  "compatibility": {
    "claude_desktop": ">=0.10.0",
    "platforms": ["darwin", "win32"],
    "runtimes": {
      "node": ">=16.0.0"
    }
  }
}
```

## Validate Your Manifest

```bash
mcpb validate manifest.json
# or
mcpb validate .
```

Always validate before packing. The validator checks against the official JSON schema.

## Localization

For multi-language support, point to locale files:

```json
"localization": {
  "resources": "mcpb-resources/${locale}.json",
  "default_locale": "en-US"
}
```

Localizable fields: `description`, `display_name`, `long_description`, `author`, `tools`, `keywords`. Values for the default locale stay in `manifest.json`; locale files only need overrides.
