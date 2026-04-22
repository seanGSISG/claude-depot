#!/usr/bin/env node
// SessionStart hook: creates symlinks defined in vault-config.json
// Cross-platform (Linux, macOS, Windows) — pure Node.js stdlib, no dependencies

const fs = require("fs");
const path = require("path");
const os = require("os");

const vaultPath = process.env.CLAUDE_PLUGIN_OPTION_VAULT_PATH;
if (!vaultPath) {
  process.exit(0);
}

// Only run when cwd is inside the vault
const cwd = path.normalize(process.cwd());
const normalizedVault = path.normalize(vaultPath);
if (!cwd.startsWith(normalizedVault)) {
  process.exit(0);
}

const configPath = path.join(vaultPath, "vault-config.json");
if (!fs.existsSync(configPath)) {
  process.exit(0);
}

let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, "utf8"));
} catch {
  process.exit(0);
}

if (!config.symlinks || typeof config.symlinks !== "object") {
  process.exit(0);
}

const hostname = os.hostname();
const created = [];
const skipped = [];

for (const [linkRel, entry] of Object.entries(config.symlinks)) {
  if (!entry.targets || !entry.targets[hostname]) {
    continue;
  }

  const target = entry.targets[hostname];
  const linkPath = path.join(vaultPath, linkRel);

  // Check if target exists
  if (!fs.existsSync(target)) {
    skipped.push(`${linkRel}: target not found (${target})`);
    continue;
  }

  // Check if symlink already exists and points to correct target
  try {
    const existing = fs.readlinkSync(linkPath);
    if (path.normalize(existing) === path.normalize(target)) {
      continue; // Already correct
    }
    // Wrong target — remove and recreate
    fs.unlinkSync(linkPath);
  } catch {
    // Not a symlink or doesn't exist — check if it's a regular directory
    if (fs.existsSync(linkPath)) {
      const stat = fs.lstatSync(linkPath);
      if (stat.isDirectory()) {
        // Regular directory exists where symlink should be — skip to avoid data loss
        skipped.push(`${linkRel}: regular directory exists — remove it manually first`);
        continue;
      }
    }
  }

  // Create parent directory if needed
  const parentDir = path.dirname(linkPath);
  if (!fs.existsSync(parentDir)) {
    fs.mkdirSync(parentDir, { recursive: true });
  }

  // Create symlink — use "junction" on Windows (no admin privileges needed)
  try {
    const symlinkType = process.platform === "win32" ? "junction" : "dir";
    fs.symlinkSync(target, linkPath, symlinkType);
    created.push(`${linkRel} → ${target}`);
  } catch (err) {
    skipped.push(`${linkRel}: failed to create symlink (${err.message})`);
  }
}

if (created.length > 0 || skipped.length > 0) {
  const parts = [];
  if (created.length > 0) {
    parts.push(`Symlinks created: ${created.join(", ")}`);
  }
  if (skipped.length > 0) {
    parts.push(`Symlinks skipped: ${skipped.join(", ")}`);
  }
  const output = { additionalContext: parts.join(". ") };
  process.stdout.write(JSON.stringify(output));
}

process.exit(0);
