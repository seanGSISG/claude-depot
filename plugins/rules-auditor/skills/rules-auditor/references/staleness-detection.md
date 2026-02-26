# Staleness Detection for Claude Code Rules

> Sources: Claude Code documentation, claude-rules-doctor project, production codebase audit patterns.

## Table of Contents

- [Overview](#overview)
- [Dead Glob Patterns](#dead-glob-patterns)
- [Referenced File Drift](#referenced-file-drift)
- [Outdated API Patterns](#outdated-api-patterns)
- [Version Pinning Drift](#version-pinning-drift)
- [Convention Drift](#convention-drift)
- [Command and Path References](#command-and-path-references)
- [Staleness Scoring](#staleness-scoring)
- [Automated Detection Tools](#automated-detection-tools)

## Overview

Staleness in rules and CLAUDE.md files means the instructions no longer match reality. This happens naturally as codebases evolve — directories get renamed, APIs change, conventions shift. Stale rules are worse than no rules because they actively mislead Claude.

Detection follows a hierarchy: structural checks (globs, file references) are fast and definitive, while semantic checks (convention drift, API pattern changes) require sampling and judgment.

## Dead Glob Patterns

**What**: A rule has `paths: ["src/utils/**/*.ts"]` but `src/utils/` was renamed to `src/lib/`.

**Detection method**:

```bash
# For each glob in a rule's paths: frontmatter
shopt -s globstar nullglob
files=( $glob_pattern )
if [ ${#files[@]} -eq 0 ]; then
  echo "DEAD GLOB: '$glob_pattern' matches no files"
fi
```

**Common causes**:
- Directory renamed or moved
- File extension changed (`.js` to `.ts`, `.jsx` to `.tsx`)
- Codebase restructured (monorepo split, directory consolidation)
- Feature deleted entirely

**Severity**: Always **stale** — a dead glob means the rule never loads, so its instructions are completely ignored.

**Fix**: Update the glob to match the current directory structure, or delete the rule if the code it covered no longer exists.

## Referenced File Drift

**What**: Rule content says "See `.agent/context/deployment/docker.md`" or references `src/config/database.ts` but the file was moved or deleted.

**Detection method**:

```bash
# Extract file path references from rule content
# Matches backtick-wrapped paths and bare paths with extensions
grep -oE '`[a-zA-Z0-9_./-]+\.[a-zA-Z]{1,5}`' "$rule_file" | tr -d '`' | while read -r ref; do
  if [ ! -e "$ref" ]; then
    echo "BROKEN REF: '$ref' referenced in $rule_file does not exist"
  fi
done

# Also check for paths in prose (without backticks)
grep -oE '\b[a-zA-Z0-9_-]+(/[a-zA-Z0-9_.-]+)+\.[a-zA-Z]{1,5}\b' "$rule_file" | while read -r ref; do
  if [ ! -e "$ref" ]; then
    echo "POSSIBLE BROKEN REF: '$ref' referenced in $rule_file"
  fi
done
```

**Severity**: **stale** if the referenced file is central to the rule's instructions, **needs-review** if it's a supplementary reference.

**Fix**: Update the path to the file's current location, or remove the reference if the file was deleted.

## Outdated API Patterns

**What**: Rule instructs using `ActionResult` return type but the service layer now uses a different pattern. Rule says "all handlers must call `validateInput()`" but that function was renamed or replaced.

**Detection method**:

```bash
# Extract code identifiers from rules (function names, class names, type names)
# Look for backtick-wrapped identifiers
grep -oE '`[A-Za-z][A-Za-z0-9_]*(\(\))?`' "$rule_file" | tr -d '`()' | sort -u | while read -r ident; do
  # Search for the identifier in files matching the rule's globs
  count=$(grep -r --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" -l "$ident" . 2>/dev/null | wc -l)
  if [ "$count" -eq 0 ]; then
    echo "MISSING IDENT: '$ident' referenced in rule but not found in codebase"
  fi
done
```

**Severity**: **stale** if the identifier is central to the rule's instruction (e.g., a required return type), **needs-review** if it's mentioned in passing.

**Fix**: Find the current API pattern and update the rule. If the convention was replaced entirely, rewrite the rule to describe the new pattern.

## Version Pinning Drift

**What**: Rule says "keep Prefect image aligned with pyproject.toml version" but versions have diverged. Or rule says "use React 18 patterns" but project upgraded to React 19.

**Detection method**:

```bash
# Extract version references from rules
grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' "$rule_file" | while read -r version; do
  echo "VERSION REF: $version in $rule_file — verify against package manifests"
done

# Cross-check against common version sources
for manifest in package.json pyproject.toml Cargo.toml go.mod Dockerfile; do
  if [ -f "$manifest" ]; then
    echo "Check versions in $manifest"
  fi
done
```

**Severity**: **needs-review** — version drift may be intentional (rule describes minimum version) or may indicate staleness.

**Fix**: Update version references to match current reality, or phrase rules to reference the source of truth rather than hard-coding versions.

## Convention Drift

**What**: Rule describes a `configure()` pattern for services but newer services use a different initialization approach. The convention evolved but the rule didn't.

**Detection method**:

1. Identify the convention described in the rule (e.g., "all services export a `configure()` function")
2. Find files matching the rule's scope
3. Check what percentage of files follow the described convention

```bash
# Example: check if files matching a glob follow a described pattern
matching_files=$(find src/services -name "*.ts" | wc -l)
files_with_pattern=$(grep -rl "export.*configure" src/services --include="*.ts" | wc -l)
percentage=$((files_with_pattern * 100 / matching_files))
echo "Convention compliance: $percentage% ($files_with_pattern/$matching_files files)"
```

**Thresholds**:
- 80%+ compliance: Convention is alive, rule is **fresh**
- 50-79% compliance: Convention may be in transition, rule **needs-review**
- <50% compliance: Convention likely abandoned, rule is **stale**

**Severity**: Depends on compliance percentage and whether non-compliant files are newer (suggesting the convention changed).

**Fix**: If the convention evolved, update the rule to describe the new pattern. If it's in transition, note both patterns and the migration direction.

## Command and Path References

**What**: Rule references `npm test` but project switched to `pnpm test`. Rule says "config lives in `config/`" but it moved to `settings/`.

**Detection method**:

```bash
# Extract shell commands from rules
grep -oE '`(npm|yarn|pnpm|npx|pip|poetry|cargo|go|make|docker) [^`]+`' "$rule_file" | tr -d '`' | while read -r cmd; do
  tool=$(echo "$cmd" | cut -d' ' -f1)
  # Check if the referenced tool matches what the project actually uses
  if [ -f "package.json" ]; then
    if echo "$cmd" | grep -q "^npm " && [ -f "pnpm-lock.yaml" ]; then
      echo "DRIFT: Rule uses 'npm' but project uses pnpm"
    fi
    if echo "$cmd" | grep -q "^yarn " && [ -f "package-lock.json" ]; then
      echo "DRIFT: Rule uses 'yarn' but project uses npm"
    fi
  fi
done

# Check directory references
grep -oE '`[a-zA-Z0-9_-]+/`' "$rule_file" | tr -d '`' | while read -r dir; do
  if [ ! -d "$dir" ]; then
    echo "MISSING DIR: '$dir' referenced in rule but directory does not exist"
  fi
done
```

**Severity**: **stale** for commands that won't work, **needs-review** for directory references that may have been renamed.

**Fix**: Update commands to use the project's actual package manager and tools. Update directory references to current structure.

## Staleness Scoring

Each memory file receives one of three scores based on the most severe finding:

### stale

The file actively misleads Claude. Immediate action needed.

Triggers:
- Dead glob patterns (rule never loads)
- References to deleted files that are central to the rule
- Instructions that directly contradict current code patterns
- Commands that will fail

### needs-review

The file may be drifting. Should be checked but isn't urgently broken.

Triggers:
- File not modified in 60+ days while matching code changed significantly
- Described patterns appear in less than 50% of matching files
- Version references that may be outdated
- Minor reference drift (supplementary files moved)

### fresh

The file accurately describes the current codebase.

Criteria:
- All globs match existing files
- Referenced files exist
- Described patterns verified in majority of matching files
- Recently maintained or verified

## Automated Detection Tools

### claude-rules-doctor

Open-source tool for detecting dead globs and structural issues: https://github.com/nulone/claude-rules-doctor

Capabilities:
- Validates `paths:` glob patterns against the actual file system
- Reports rules that never match any files
- Checks for syntax issues in frontmatter

### Manual audit script

The `match-affected-rules.sh` script in this plugin can be used for basic structural validation. For a full audit, use the interactive skill workflow which combines structural checks with semantic analysis.
