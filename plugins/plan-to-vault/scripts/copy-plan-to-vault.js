#!/usr/bin/env node
// PostToolUse hook: copies Claude Code plan files to Obsidian vault on ExitPlanMode
// Cross-platform (Linux, WSL2, Windows) — pure Node.js stdlib, no dependencies

const fs = require("fs");
const path = require("path");
const os = require("os");

function readStdin() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    setTimeout(() => resolve(data), 2000);
  });
}

function toKebabCase(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

async function main() {
  const input = await readStdin();
  let payload;
  try {
    payload = JSON.parse(input);
  } catch {
    process.exit(0);
  }

  if (payload.tool_name !== "ExitPlanMode") {
    process.exit(0);
  }

  const sessionId = payload.session_id || "";

  // Read vault path from plugin userConfig
  const vaultPath = process.env.CLAUDE_PLUGIN_OPTION_VAULT_PATH;
  if (!vaultPath) {
    process.exit(0);
  }

  const notesDir = path.join(vaultPath, "Notes", "plan");
  fs.mkdirSync(notesDir, { recursive: true });

  const plansDir = path.join(os.homedir(), ".claude", "plans");
  if (!fs.existsSync(plansDir)) {
    process.exit(0);
  }

  // Find most recently modified non-agent plan file
  let planFiles;
  try {
    planFiles = fs
      .readdirSync(plansDir)
      .filter((f) => f.endsWith(".md") && !f.includes("-agent-"))
      .map((f) => ({
        name: f,
        fullPath: path.join(plansDir, f),
        mtime: fs.statSync(path.join(plansDir, f)).mtime,
      }))
      .sort((a, b) => b.mtime - a.mtime);
  } catch {
    process.exit(0);
  }

  if (planFiles.length === 0) {
    process.exit(0);
  }

  const planFile = planFiles[0];
  const content = fs.readFileSync(planFile.fullPath, "utf8");
  const lines = content.split(/\r?\n/);

  // Extract H1 title from first line
  const firstLine = lines[0] || "";
  if (!firstLine.startsWith("# ")) {
    process.exit(0);
  }

  const title = firstLine.replace(/^#\s+/, "").replace(/^Plan:\s*/i, "");
  if (!title.trim()) {
    process.exit(0);
  }

  const slug = toKebabCase(title);
  if (!slug) {
    process.exit(0);
  }

  const targetPath = path.join(notesDir, `${slug}.md`);

  // Idempotent: skip if already exists
  if (fs.existsSync(targetPath)) {
    process.exit(0);
  }

  const origin = os.hostname();
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
session-id: "${sessionId}"
created: ${created}
status: active
---

# ${title}
${body}`;

  try {
    fs.writeFileSync(targetPath, note, "utf8");
    const output = {
      additionalContext: `Plan archived to vault: Notes/plan/${slug}.md (origin: ${origin})`,
    };
    process.stdout.write(JSON.stringify(output));
  } catch {
    // Silent failure — don't block Claude
  }

  process.exit(0);
}

main();
