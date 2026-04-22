#!/usr/bin/env node
// One-time migration: move Notes/*.md files into Notes/<type>/ subfolders
// Reads YAML frontmatter to determine type, falls back to "note" if missing/invalid

const fs = require("fs");
const path = require("path");

const VALID_TYPES = [
  "reference", "guide", "config", "agent", "prompt",
  "list", "project", "plan", "diagram", "note", "journal", "journal-session",
];

const vaultPath = process.argv[2] || process.env.CLAUDE_PLUGIN_OPTION_VAULT_PATH;
if (!vaultPath) {
  console.error("Usage: node migrate-to-subfolders.js <vault-path>");
  process.exit(1);
}

const notesDir = path.join(vaultPath, "Notes");
if (!fs.existsSync(notesDir)) {
  console.error(`Notes directory not found: ${notesDir}`);
  process.exit(1);
}

function extractType(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const lines = content.split(/\r?\n/);
  if (lines[0] !== "---") return null;

  const endIdx = lines.indexOf("---", 1);
  if (endIdx === -1) return null;

  const frontmatter = lines.slice(1, endIdx).join("\n");
  const match = frontmatter.match(/^type:\s*(.+)$/m);
  return match ? match[1].trim().replace(/^["']|["']$/g, "") : null;
}

// Read only top-level .md files (not in subfolders)
const files = fs.readdirSync(notesDir).filter((f) => {
  const fullPath = path.join(notesDir, f);
  return f.endsWith(".md") && fs.statSync(fullPath).isFile();
});

if (files.length === 0) {
  console.log("No top-level .md files in Notes/ — nothing to migrate.");
  process.exit(0);
}

const counts = {};
const warnings = [];

for (const file of files) {
  const srcPath = path.join(notesDir, file);
  let type = extractType(srcPath);

  if (!type || !VALID_TYPES.includes(type)) {
    warnings.push(`${file}: type "${type || "(missing)"}" invalid — moving to note/`);
    type = "note";
  }

  const destDir = path.join(notesDir, type);
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }

  const destPath = path.join(destDir, file);
  if (fs.existsSync(destPath)) {
    warnings.push(`${file}: already exists in ${type}/ — skipping`);
    continue;
  }

  fs.renameSync(srcPath, destPath);
  counts[type] = (counts[type] || 0) + 1;
}

console.log("\n=== Migration Summary ===\n");
const total = Object.values(counts).reduce((a, b) => a + b, 0);
console.log(`Moved ${total} files:\n`);
for (const [type, count] of Object.entries(counts).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${type}/: ${count}`);
}

if (warnings.length > 0) {
  console.log(`\nWarnings (${warnings.length}):\n`);
  for (const w of warnings) {
    console.log(`  ⚠ ${w}`);
  }
}

console.log("\nMigration complete.");
