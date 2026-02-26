# GitHub Actions CI Integration for Rules Freshness Audit

> Sources: Claude Code Action documentation, GitHub Actions workflow syntax, production CI configurations.

## Table of Contents

- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Workflow Configuration](#workflow-configuration)
- [Pre-Check Script](#pre-check-script)
- [Claude Code Action Configuration](#claude-code-action-configuration)
- [Cost Optimization](#cost-optimization)
- [Setup Instructions](#setup-instructions)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

## Architecture

The CI integration uses a two-stage pipeline to minimize cost while catching staleness:

```
PR Opened/Synchronized
  -> GitHub path filter (free, skips irrelevant PRs)
  -> Pre-check job (bash, <10s, no API cost)
       -> Parse rules frontmatter, match against changed files
       -> Classify changes (deletions/renames = always significant)
  -> Audit job (conditional, claude-code-action)
       -> Inject CI-specific rules via .claude/rules/ in prior step
       -> Claude reviews affected rules against PR diff
       -> Posts findings as PR comment
```

The path filter and pre-check job together skip 80-90% of PRs before incurring any API cost.

## How It Works

### Stage 1: Path Filter (GitHub-native)

The workflow's `on.pull_request.paths` filter skips PRs that only touch files irrelevant to rules (documentation, test fixtures, CI configs). This is free — GitHub evaluates it before spinning up a runner.

### Stage 2: Pre-Check Job (Bash)

A lightweight bash job that:
1. Gets the list of changed files from `git diff`
2. Finds all `.claude/rules/*.md` files and `CLAUDE.md` files
3. Parses `paths:` frontmatter from each rule
4. Checks if any changed file matches any rule's globs
5. Also checks if any `CLAUDE.md` file's directory subtree contains changes
6. Outputs `needs_audit=true` and the list of affected rules if matches found

### Stage 3: Audit Job (Claude Code Action)

Runs only when the pre-check found affected rules. Uses `anthropics/claude-code-action@v1` in agent mode:
1. A prior step writes CI-specific auditor instructions into `.claude/rules/ci-auditor.md` so Claude loads them automatically
2. Claude receives a prompt listing the affected rules and instruction to review them
3. Claude reads each affected rule, checks it against the PR diff
4. Claude posts findings as a PR comment with per-rule assessments

## Workflow Configuration

The workflow file (`rules-freshness-audit.yml`) is installed to `.github/workflows/` in the user's repository.

Key sections:

### Trigger

```yaml
on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - 'src/**'
      - 'lib/**'
      - 'app/**'
      - 'packages/**'
      - '*.config.*'
      - 'package.json'
      - 'tsconfig*.json'
      - 'pyproject.toml'
      - 'Cargo.toml'
      - 'Dockerfile*'
      - '.claude/**'
      - 'CLAUDE.md'
      - '**/CLAUDE.md'
```

The `paths:` list should be customized per project. The `/install-rules-audit` command auto-detects the project's source directories.

### Concurrency

```yaml
concurrency:
  group: rules-audit-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

Cancels in-progress audits when new commits are pushed to the same PR, preventing duplicate runs on force-pushes.

### Skip Label

The workflow checks for a `skip-rules-audit` label to bypass the audit entirely:

```yaml
if: "!contains(github.event.pull_request.labels.*.name, 'skip-rules-audit')"
```

## Pre-Check Script

The `match-affected-rules.sh` script is installed to `.github/scripts/`. It:

1. Reads changed files from `git diff --name-only`
2. Discovers all rules files and CLAUDE.md files
3. Parses frontmatter to extract `paths:` globs
4. Matches changed files against globs using bash pattern matching
5. Outputs results as GitHub Actions outputs

The script has no dependencies beyond bash and standard Unix tools (grep, sed, find).

## Claude Code Action Configuration

The audit job uses `anthropics/claude-code-action@v1` with these settings:

### Authentication

The workflow uses the Claude GitHub App for authentication. This app is installed via Claude Code's `/install-github-app` command and authenticates through the user's Anthropic subscription — no separate `ANTHROPIC_API_KEY` secret is needed.

### Tool Restrictions

```yaml
allowed_tools: "Read,Glob,Grep,Bash(git diff:*),Bash(git log:*),Bash(find:*),Bash(gh pr comment:*)"
```

The auditor is restricted to read-only tools plus the ability to post PR comments. It cannot modify code.

### Max Turns

```yaml
max_turns: 15
```

Bounds the audit scope to prevent runaway costs. 15 turns is sufficient to review 5-10 affected rules with thorough checking.

### CI-Injected Rules

Before running the action, a prior step writes auditor instructions to `.claude/rules/ci-auditor.md`:

```yaml
- name: Inject CI auditor rules
  run: |
    mkdir -p .claude/rules
    cat > .claude/rules/ci-auditor.md << 'RULES'
    ---
    paths:
      - ".claude/**"
      - "**/CLAUDE.md"
    ---
    # CI Rules Auditor Instructions
    You are auditing rules and CLAUDE.md files for freshness...
    RULES
```

This file is created in the runner's workspace only — it's not committed to the repository.

### Prompt Template

The audit job's prompt includes:
- Repository name and PR number
- Base branch for comparison
- List of affected rules (from pre-check output)
- Instruction to review each affected rule against the PR diff
- Output format (PR comment with per-rule assessment)

## Cost Optimization

### Free tier: Path filters

GitHub evaluates `on.pull_request.paths` before starting a runner. PRs that only touch docs, tests, or CI configs are skipped entirely. This filters out 60-80% of PRs at zero cost.

### Cheap tier: Pre-check job

The bash pre-check runs in under 10 seconds on a standard runner. No API calls. Filters out another 50-70% of remaining PRs (those that touch source code but not in areas any rule covers).

### Bounded tier: Audit job

When the audit runs:
- `max_turns: 15` caps the API usage
- Tool restrictions prevent unnecessary exploration
- The prompt focuses Claude on specific affected rules, not a full codebase scan

### Concurrency cancellation

`cancel-in-progress: true` prevents duplicate runs on rapid pushes.

### Optional controls

- Add `skip-rules-audit` label to bypass on any PR
- Add `force-rules-audit` label to force audit even when pre-check says no
- Adjust `max_turns` up or down based on your rules complexity

## Setup Instructions

### Automated (recommended)

1. Install the Claude GitHub App if not already done:
   ```
   /install-github-app
   ```

2. Install the rules audit workflow:
   ```
   /install-rules-audit
   ```

3. The command will:
   - Detect your project's source directories
   - Ask which paths should trigger the audit
   - Write the workflow and pre-check script
   - Provide testing instructions

### Manual

1. Ensure the Claude GitHub App is installed (provides authentication)

2. Copy the workflow file to `.github/workflows/rules-freshness-audit.yml`

3. Copy the pre-check script to `.github/scripts/match-affected-rules.sh` and make it executable:
   ```bash
   chmod +x .github/scripts/match-affected-rules.sh
   ```

4. Customize the `paths:` trigger filter in the workflow for your project's directory structure

5. Commit and push to your default branch

## Customization

### Adjusting path triggers

Edit the `on.pull_request.paths` section in the workflow to match your project's source directories. Remove paths that don't exist, add paths for your project's unique structure.

### Changing audit depth

Increase `max_turns` for projects with many rules files, decrease for projects with few. The default of 15 handles most projects well.

### Restricting to specific branches

Add a `branches` filter to only run on PRs targeting specific branches:

```yaml
on:
  pull_request:
    branches: [main, develop]
    paths: [...]
```

### Custom skip labels

Modify the label check to use a different label name or add a force label.

## Troubleshooting

### Audit doesn't run on PRs

1. Check that the PR changes files matching the `paths:` filter
2. Verify the Claude GitHub App is installed (`/install-github-app`)
3. Check for the `skip-rules-audit` label on the PR
4. Review the pre-check job output — it may have determined no rules are affected

### Audit runs but posts no comment

1. Check the audit job logs for errors
2. Verify the GitHub App has permission to comment on PRs
3. Check that `max_turns` wasn't exhausted before Claude could post

### Pre-check reports wrong affected rules

1. Verify the `paths:` frontmatter in your rules files uses valid glob syntax
2. Check that `match-affected-rules.sh` is executable
3. Run the script locally to debug: `git diff --name-only main | bash .github/scripts/match-affected-rules.sh`
