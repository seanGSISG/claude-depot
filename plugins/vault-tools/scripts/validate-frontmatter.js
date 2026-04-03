#!/usr/bin/env node
// PostToolUse hook: validates YAML frontmatter for files written to Notes/
// Cross-platform (Linux, macOS, Windows) — pure Node.js stdlib, no dependencies

const fs = require("fs");
const path = require("path");

const VALID_TYPES = [
  "reference", "guide", "config", "agent", "prompt",
  "list", "project", "plan", "diagram", "note",
];
const VALID_STATUSES = ["active", "draft", "archived"];

function readStdin() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    setTimeout(() => resolve(data), 2000);
  });
}

function extractFrontmatter(content) {
  const lines = content.split(/\r?\n/);
  if (lines[0] !== "---") return null;

  const endIdx = lines.indexOf("---", 1);
  if (endIdx === -1) return null;

  return lines.slice(1, endIdx).join("\n");
}

function parseFrontmatterField(frontmatter, field) {
  const match = frontmatter.match(new RegExp(`^${field}:\\s*(.*)$`, "m"));
  return match ? match[1].trim().replace(/^["']|["']$/g, "") : null;
}

function parseTags(frontmatter) {
  const lines = frontmatter.split(/\r?\n/);
  const tagsIdx = lines.findIndex((l) => /^tags:\s*$/.test(l) || /^tags:\s*\[/.test(l));
  if (tagsIdx === -1) return [];

  // Inline array: tags: [foo, bar]
  const inlineMatch = lines[tagsIdx].match(/^tags:\s*\[(.+)\]/);
  if (inlineMatch) {
    return inlineMatch[1].split(",").map((t) => t.trim().replace(/^["']|["']$/g, ""));
  }

  // YAML list: tags:\n  - foo\n  - bar
  const tags = [];
  for (let i = tagsIdx + 1; i < lines.length; i++) {
    const tagMatch = lines[i].match(/^\s+-\s+(.+)$/);
    if (tagMatch) {
      tags.push(tagMatch[1].trim().replace(/^["']|["']$/g, ""));
    } else if (/^\S/.test(lines[i])) {
      break;
    }
  }
  return tags;
}

async function main() {
  const vaultPath = process.env.CLAUDE_PLUGIN_OPTION_VAULT_PATH;
  if (!vaultPath) {
    process.exit(0);
  }

  const input = await readStdin();
  let payload;
  try {
    payload = JSON.parse(input);
  } catch {
    process.exit(0);
  }

  const filePath = (payload.tool_input && payload.tool_input.file_path) || "";
  if (!filePath) {
    process.exit(0);
  }

  // Only validate .md files inside the vault's Notes/ directory
  const notesDir = path.join(vaultPath, "Notes");
  const normalizedFile = path.normalize(filePath);
  const normalizedNotes = path.normalize(notesDir);

  if (!normalizedFile.startsWith(normalizedNotes + path.sep)) {
    process.exit(0);
  }
  if (!normalizedFile.endsWith(".md")) {
    process.exit(0);
  }
  if (!fs.existsSync(normalizedFile)) {
    process.exit(0);
  }

  const content = fs.readFileSync(normalizedFile, "utf8");
  const frontmatter = extractFrontmatter(content);

  if (!frontmatter) {
    const msg = {
      additionalContext:
        "FRONTMATTER VALIDATION FAILED: No YAML frontmatter found. " +
        "Every note in Notes/ must have frontmatter between --- delimiters with: " +
        "title, type, tags, created (YYYY-MM-DD), status (active|draft|archived).",
    };
    process.stdout.write(JSON.stringify(msg));
    process.exit(0);
  }

  const errors = [];

  // Check type
  const typeValue = parseFrontmatterField(frontmatter, "type");
  if (!typeValue) {
    errors.push(`Missing 'type' field. Valid types: ${VALID_TYPES.join(", ")}.`);
  } else if (!VALID_TYPES.includes(typeValue)) {
    errors.push(`Invalid type '${typeValue}'. Valid types: ${VALID_TYPES.join(", ")}.`);
  }

  // Check tags
  const tags = parseTags(frontmatter);
  if (tags.length === 0) {
    errors.push("Missing or empty 'tags' field (need at least 1 tag).");
  }

  // Check created
  if (!parseFrontmatterField(frontmatter, "created")) {
    errors.push("Missing 'created' field (YYYY-MM-DD).");
  }

  // Check status
  const statusValue = parseFrontmatterField(frontmatter, "status");
  if (!statusValue) {
    errors.push("Missing 'status' field.");
  } else if (!VALID_STATUSES.includes(statusValue)) {
    errors.push(`Invalid status '${statusValue}'. Must be: active, draft, or archived.`);
  }

  // Check title
  if (!parseFrontmatterField(frontmatter, "title")) {
    errors.push("Missing 'title' field.");
  }

  if (errors.length > 0) {
    const filename = path.basename(normalizedFile);
    const msg = {
      additionalContext:
        `FRONTMATTER VALIDATION FAILED for ${filename}: ${errors.join(" ")} ` +
        "Fix the frontmatter to match the schema in CLAUDE.md.",
    };
    process.stdout.write(JSON.stringify(msg));
  }

  process.exit(0);
}

main();
