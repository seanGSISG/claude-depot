# rules-auditor

Audit Claude Code rules and CLAUDE.md/AGENTS.md files for staleness, quality, and drift against the actual codebase.

## What It Does

Scans a repository's Claude Code configuration files (CLAUDE.md, AGENTS.md, `.claude/rules/`) and identifies:

- **Stale rules** — references to renamed/deleted files, functions, or endpoints
- **Quality issues** — vague instructions, duplicated guidance, missing context
- **Anti-patterns** — overly long rules, rules that conflict with each other
- **Drift** — rules that no longer match the current codebase state

## Setup

```
/plugin install rules-auditor@claude-depot
```

No configuration required.

## Usage

Run the audit skill:
```
/rules-auditor:rules-auditor
```

## CI Integration

The plugin includes a GitHub Actions workflow for automated freshness auditing on pull requests. Install it with:

```
/rules-auditor:install-rules-audit
```

This adds a workflow that runs on PRs touching rules files and comments with a staleness report.

## Components

| Component | Description |
|-----------|-------------|
| `skills/rules-auditor` | Main audit skill with 4 reference guides |
| `commands/install-rules-audit.md` | CI workflow installer command |
| `scripts/match-affected-rules.sh` | PR diff analyzer for CI |
| `workflows/rules-freshness-audit.yml` | GitHub Actions workflow template |
