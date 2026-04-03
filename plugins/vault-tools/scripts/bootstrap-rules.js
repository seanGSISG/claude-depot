#!/usr/bin/env node
// SessionStart hook: copies bundled rule files to .claude/rules/ in the vault
// Cross-platform (Linux, macOS, Windows) — pure Node.js stdlib, no dependencies

const fs = require("fs");
const path = require("path");

function readStdin() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    setTimeout(() => resolve(data), 2000);
  });
}

async function main() {
  const vaultPath = process.env.CLAUDE_PLUGIN_OPTION_VAULT_PATH;
  if (!vaultPath) {
    const msg = {
      additionalContext:
        "[vault-tools] Vault path not configured. " +
        "Run /vault-tools:setup-vault-tools to configure, or go to /plugin \u2192 vault-tools \u2192 Configure options.",
    };
    process.stdout.write(JSON.stringify(msg));
    process.exit(0);
  }

  const input = await readStdin();
  let payload;
  try {
    payload = JSON.parse(input);
  } catch {
    process.exit(0);
  }

  const cwd = (payload && payload.cwd) || "";
  const normalizedCwd = path.normalize(cwd);
  const normalizedVault = path.normalize(vaultPath);

  // Only bootstrap rules when working inside the vault
  if (!normalizedCwd.startsWith(normalizedVault)) {
    process.exit(0);
  }

  const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT;
  if (!pluginRoot) {
    process.exit(0);
  }

  const bundledRulesDir = path.join(pluginRoot, "rules");
  const targetRulesDir = path.join(vaultPath, ".claude", "rules");

  if (!fs.existsSync(bundledRulesDir)) {
    process.exit(0);
  }

  // Ensure target directory exists
  fs.mkdirSync(targetRulesDir, { recursive: true });

  const ruleFiles = fs.readdirSync(bundledRulesDir).filter((f) => f.endsWith(".md"));
  const updated = [];

  for (const file of ruleFiles) {
    const sourcePath = path.join(bundledRulesDir, file);
    const targetPath = path.join(targetRulesDir, file);

    const sourceContent = fs.readFileSync(sourcePath, "utf8");

    // Skip if identical (idempotent)
    if (fs.existsSync(targetPath)) {
      const targetContent = fs.readFileSync(targetPath, "utf8");
      if (sourceContent === targetContent) {
        continue;
      }
    }

    fs.writeFileSync(targetPath, sourceContent, "utf8");
    updated.push(file);
  }

  if (updated.length > 0) {
    const msg = {
      additionalContext: `[vault-tools] Bootstrapped ${updated.length} rule(s): ${updated.join(", ")}`,
    };
    process.stdout.write(JSON.stringify(msg));
  }

  process.exit(0);
}

main();
