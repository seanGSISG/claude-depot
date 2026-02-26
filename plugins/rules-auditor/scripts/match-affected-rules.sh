#!/usr/bin/env bash
# match-affected-rules.sh — Determine which rules/CLAUDE.md files are affected by changed files
#
# Usage:
#   git diff --name-only origin/main...HEAD | bash match-affected-rules.sh
#   bash match-affected-rules.sh file1.ts file2.ts
#
# Outputs (GitHub Actions):
#   needs_audit=true|false
#   affected_rules=<newline-delimited list of affected rule files>
#
# Exit codes:
#   0 — always (results in outputs, not exit code)

set -euo pipefail

# --- Read changed files ---
changed_files=()
if [ $# -gt 0 ]; then
  # Arguments provided
  changed_files=("$@")
else
  # Read from stdin
  while IFS= read -r line; do
    [ -n "$line" ] && changed_files+=("$line")
  done
fi

if [ ${#changed_files[@]} -eq 0 ]; then
  echo "No changed files provided."
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "needs_audit=false" >> "$GITHUB_OUTPUT"
    echo "affected_rules=" >> "$GITHUB_OUTPUT"
  fi
  exit 0
fi

# --- Detect deletions/renames (always significant) ---
has_deletions=false
for f in "${changed_files[@]}"; do
  if [ ! -e "$f" ]; then
    has_deletions=true
    break
  fi
done

# --- Find all rules files ---
rules_files=()
if [ -d ".claude/rules" ]; then
  while IFS= read -r -d '' rf; do
    rules_files+=("$rf")
  done < <(find .claude/rules -name "*.md" -type f -print0 2>/dev/null)
fi

# --- Find all CLAUDE.md files ---
claude_md_files=()
while IFS= read -r -d '' cf; do
  claude_md_files+=("$cf")
done < <(find . \( -name "CLAUDE.md" -o -name "CLAUDE.local.md" \) -not -path "./.git/*" -not -path "*/node_modules/*" -print0 2>/dev/null)

# --- Extract paths from YAML frontmatter ---
# Reads a rules .md file and outputs its paths: globs, one per line
extract_paths() {
  local file="$1"
  local in_frontmatter=false
  local in_paths=false
  local found_frontmatter=false

  while IFS= read -r line; do
    if [ "$found_frontmatter" = false ] && [ "$line" = "---" ]; then
      found_frontmatter=true
      in_frontmatter=true
      continue
    fi

    if [ "$in_frontmatter" = true ] && [ "$line" = "---" ]; then
      break
    fi

    if [ "$in_frontmatter" = true ]; then
      # Check for paths: key
      if echo "$line" | grep -qE '^paths:'; then
        in_paths=true
        # Check for inline list: paths: ["glob1", "glob2"]
        if echo "$line" | grep -qE '\['; then
          echo "$line" | grep -oE '"[^"]*"' | tr -d '"'
          in_paths=false
        fi
        continue
      fi

      if [ "$in_paths" = true ]; then
        # List items under paths:
        if echo "$line" | grep -qE '^ *- '; then
          echo "$line" | sed 's/^ *- *//;s/^"//;s/"$///;s/^'"'"'//;s/'"'"'$//'
        else
          # No longer in paths list
          in_paths=false
        fi
      fi
    fi
  done < "$file"
}

# --- Match a file against a glob pattern ---
# Uses bash extended globbing
match_glob() {
  local pattern="$1"
  local filepath="$2"

  # Enable extended globbing
  shopt -s extglob globstar nullglob 2>/dev/null

  # Normalize: remove leading ./
  filepath="${filepath#./}"
  pattern="${pattern#./}"

  # Use bash pattern matching
  if [[ "$filepath" == $pattern ]]; then
    return 0
  fi
  return 1
}

# --- Check which rules are affected ---
affected=()

for rule_file in "${rules_files[@]}"; do
  rule_affected=false

  # Check if the rule file itself changed
  rule_normalized="${rule_file#./}"
  for cf in "${changed_files[@]}"; do
    cf_normalized="${cf#./}"
    if [ "$rule_normalized" = "$cf_normalized" ]; then
      rule_affected=true
      break
    fi
  done

  if [ "$rule_affected" = true ]; then
    affected+=("$rule_file")
    continue
  fi

  # Extract paths globs
  globs=()
  while IFS= read -r g; do
    [ -n "$g" ] && globs+=("$g")
  done < <(extract_paths "$rule_file")

  # Global rule (no paths:) — affected by any deletion/rename
  if [ ${#globs[@]} -eq 0 ]; then
    if [ "$has_deletions" = true ]; then
      affected+=("$rule_file")
    fi
    continue
  fi

  # Scoped rule — check if any changed file matches any glob
  for glob in "${globs[@]}"; do
    for cf in "${changed_files[@]}"; do
      if match_glob "$glob" "$cf"; then
        rule_affected=true
        break 2
      fi
    done
  done

  if [ "$rule_affected" = true ]; then
    affected+=("$rule_file")
  fi
done

# --- Check CLAUDE.md files ---
for claude_file in "${claude_md_files[@]}"; do
  claude_dir=$(dirname "$claude_file")
  claude_dir="${claude_dir#./}"

  # Check if CLAUDE.md itself changed
  claude_normalized="${claude_file#./}"
  for cf in "${changed_files[@]}"; do
    cf_normalized="${cf#./}"
    if [ "$claude_normalized" = "$cf_normalized" ]; then
      affected+=("$claude_file")
      continue 2
    fi
  done

  # Check if any changed file is in the CLAUDE.md's directory subtree
  for cf in "${changed_files[@]}"; do
    cf_normalized="${cf#./}"
    if [ "$claude_dir" = "." ]; then
      # Root CLAUDE.md — affected by any source file change
      # (let the audit job decide if it's relevant)
      affected+=("$claude_file")
      break
    elif [[ "$cf_normalized" == "$claude_dir"/* ]]; then
      affected+=("$claude_file")
      break
    fi
  done
done

# --- Deduplicate ---
IFS=$'\n' unique_affected=($(printf '%s\n' "${affected[@]}" | sort -u))
unset IFS

# --- Output ---
if [ ${#unique_affected[@]} -eq 0 ]; then
  echo "No rules or CLAUDE.md files affected by changes."
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "needs_audit=false" >> "$GITHUB_OUTPUT"
    echo "affected_rules=" >> "$GITHUB_OUTPUT"
  fi
else
  echo "Affected rules/memory files:"
  printf '  %s\n' "${unique_affected[@]}"

  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "needs_audit=true" >> "$GITHUB_OUTPUT"
    # Use delimiter for multiline output
    echo "affected_rules<<EOF" >> "$GITHUB_OUTPUT"
    printf '%s\n' "${unique_affected[@]}" >> "$GITHUB_OUTPUT"
    echo "EOF" >> "$GITHUB_OUTPUT"
  fi
fi
