#!/usr/bin/env node
// One-time bulk import of existing Claude Code plans into Obsidian vault
// Usage: node bulk-import-plans.js [vault-path]
// Falls back to CLAUDE_PLUGIN_OPTION_VAULT_PATH env var

const fs = require("fs");
const path = require("path");
const os = require("os");

function toKebabCase(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function main() {
  const vaultPath =
    process.argv[2] || process.env.CLAUDE_PLUGIN_OPTION_VAULT_PATH;

  if (!vaultPath) {
    console.error(
      "Usage: node bulk-import-plans.js <vault-path>\n" +
        "Or set CLAUDE_PLUGIN_OPTION_VAULT_PATH environment variable."
    );
    process.exit(1);
  }

  const notesDir = path.join(vaultPath, "Notes");
  const plansDir = path.join(os.homedir(), ".claude", "plans");
  const origin = os.hostname();

  if (!fs.existsSync(notesDir)) {
    console.error(`Notes directory not found: ${notesDir}`);
    process.exit(1);
  }

  if (!fs.existsSync(plansDir)) {
    console.error(`Plans directory not found: ${plansDir}`);
    process.exit(1);
  }

  const planFiles = fs
    .readdirSync(plansDir)
    .filter((f) => f.endsWith(".md") && !f.includes("-agent-"))
    .map((f) => ({
      name: f,
      fullPath: path.join(plansDir, f),
      mtime: fs.statSync(path.join(plansDir, f)).mtime,
    }));

  let imported = 0;
  let skipped = 0;
  let noTitle = 0;

  for (const planFile of planFiles) {
    const content = fs.readFileSync(planFile.fullPath, "utf8");
    const lines = content.split(/\r?\n/);

    const firstLine = lines[0] || "";
    if (!firstLine.startsWith("# ")) {
      noTitle++;
      continue;
    }

    const title = firstLine.replace(/^#\s+/, "").replace(/^Plan:\s*/i, "");
    if (!title.trim()) {
      noTitle++;
      continue;
    }

    const slug = toKebabCase(title);
    if (!slug) {
      noTitle++;
      continue;
    }

    const targetPath = path.join(notesDir, `${slug}.md`);

    if (fs.existsSync(targetPath)) {
      skipped++;
      continue;
    }

    const created = planFile.mtime.toLocaleDateString("en-CA", { timeZone: "America/Denver" });
    const body = lines.slice(1).join("\n");

    const note = `---
title: "${title.replace(/"/g, '\\"')}"
type: plan
tags:
  - planning
  - claude-code
origin: ${origin}
plan-file: "${planFile.name}"
created: ${created}
status: active
---

# ${title}
${body}`;

    fs.writeFileSync(targetPath, note, "utf8");
    imported++;
    console.log(`  + ${slug}.md (from ${planFile.name})`);
  }

  console.log(
    `\nDone. Imported: ${imported}, Skipped (duplicate): ${skipped}, Skipped (no title): ${noTitle}`
  );
}

main();
