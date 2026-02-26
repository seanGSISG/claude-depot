---
name: rules-auditor
description: "Audit Claude Code rules and CLAUDE.md files for staleness, quality, and drift. Use when asked to audit rules, check stale CLAUDE.md, review rules freshness, assess rules quality, improve my rules, find dead globs in rules, check if rules are up to date, review progressive disclosure setup, find contradictory rules, or optimize Claude Code memory files."
---

## Overview

This skill audits and improves Claude Code memory files — `.claude/rules/*.md`, `CLAUDE.md`, and `CLAUDE.local.md`. It detects staleness (dead globs, references to deleted files, outdated conventions), quality issues (bloat, contradictions, redundancy), and provides actionable recommendations.

Use this skill when asked to:
- Audit or review rules quality and freshness
- Find stale or broken rules
- Improve progressive disclosure setup
- Check if CLAUDE.md files are up to date
- Optimize Claude Code context loading

## Discovery Workflow

Before auditing, discover all memory files in the project:

### 1. Find all rules files

```bash
find .claude/rules -name "*.md" -type f 2>/dev/null | sort
```

### 2. Find all CLAUDE.md files

```bash
find . -name "CLAUDE.md" -o -name "CLAUDE.local.md" | grep -v node_modules | grep -v .git | sort
```

### 3. Parse scoping from each rule

For each rule file, extract the `paths:` frontmatter to determine scope:

```bash
# Extract paths from YAML frontmatter
sed -n '/^---$/,/^---$/p' "$rule_file" | grep -A 50 '^paths:' | grep '^ *- ' | sed 's/^ *- *//'
```

- **Global rules**: No `paths:` frontmatter — loaded on every session
- **Scoped rules**: Have `paths:` with glob patterns — loaded only when Claude reads matching files

### 4. Build the inventory

Classify each file:
- Rule files with `paths:` → scoped rules (note the globs)
- Rule files without `paths:` → global rules
- Root `CLAUDE.md` → always loaded (ancestor of cwd)
- Nested `CLAUDE.md` files → loaded lazily when Claude reads files in that subtree

## Audit Workflow

For each discovered memory file, perform these checks:

### Step 1: Dead Glob Detection (scoped rules only)

For each glob pattern in `paths:`, verify files actually match:

```bash
# Test if a glob matches any files
shopt -s globstar nullglob
files=( $glob_pattern )
if [ ${#files[@]} -eq 0 ]; then
  echo "STALE: glob '$glob_pattern' matches no files"
fi
```

Common causes: directories renamed, file extensions changed, code moved to a different location.

### Step 2: Referenced File Verification

Extract file paths mentioned in rule content and verify they exist:

```bash
# Find file references in rule content (paths like src/foo/bar.ts, ./config/x.json)
grep -oE '`[a-zA-Z0-9_./-]+\.[a-zA-Z]{1,5}`' "$rule_file" | tr -d '`' | while read -r ref; do
  [ ! -e "$ref" ] && echo "BROKEN REF: $ref in $rule_file"
done
```

### Step 3: Code Pattern Verification

For key identifiers mentioned in rules (function names, class names, type names, command names):

1. Extract quoted identifiers and code-fenced terms from the rule
2. Search the codebase for their existence using `grep` or `Grep` tool
3. Flag rules that reference patterns no longer present in matching files

### Step 4: Convention Drift Detection

For rules describing code conventions or patterns:

1. Identify the convention described (e.g., "all services use a `configure()` method")
2. Sample files matching the rule's scope
3. Check if the described pattern appears in a majority of matching files
4. Flag if <50% of files follow the described convention

### Step 5: Structural Verification (nested CLAUDE.md)

For nested CLAUDE.md files, verify:
- The directory structure they describe still exists
- Commands they reference (build, test, lint) still work
- Technology/framework references match actual dependencies

### Step 6: Freshness Scoring

Assign each file a score:

| Score | Criteria |
|---|---|
| **fresh** | All globs match files, referenced files exist, described patterns verified in code |
| **needs-review** | File not modified in 60+ days, or described patterns appear in <50% of matching files, or minor drift detected |
| **stale** | Dead globs, references to deleted files, instructions contradicted by current code |

### Step 7: Report Generation

Produce a structured report with:
- Summary table of all files with their freshness score
- Specific findings per file (what's broken, what drifted)
- Actionable recommendations (update glob, remove reference, rewrite section)
- Priority ranking (stale items first)

## Reference Navigation

| Topic | Reference File | Key Contents |
|---|---|---|
| What makes effective rules and CLAUDE.md | `references/quality-patterns.md` | Root CLAUDE.md guidelines, scoped rules best practices, progressive disclosure tiers, emphasis patterns |
| Common mistakes to avoid | `references/anti-patterns.md` | Kitchen sink files, volatile imports, negative-only constraints, linter duplication, redundancy |
| Detecting drift and staleness | `references/staleness-detection.md` | Dead globs, referenced file drift, API pattern drift, version pinning, convention drift, scoring |
| CI integration with GitHub Actions | `references/github-workflow-guide.md` | Workflow architecture, setup instructions, cost optimization, claude-code-action configuration |

## CI Integration

For automated freshness checks on every PR, see `references/github-workflow-guide.md`. The workflow uses `claude-code-action` to review affected rules when code changes and posts findings as PR comments.

To install the CI workflow automatically, use the `/install-rules-audit` command.
