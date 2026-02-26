---
description: "Install the rules freshness audit GitHub Actions workflow into your repository"
allowed-tools: ["Bash", "Read", "Write", "Glob", "AskUserQuestion"]
---

## Install Rules Freshness Audit Workflow

You are installing the rules freshness audit GitHub Actions workflow into the user's repository. Follow these steps carefully.

### Step 1: Check Claude GitHub App Installation

Check if the Claude GitHub App is already set up by looking for existing workflows that use `anthropics/claude-code-action`:

```bash
find .github/workflows -name "*.yml" -exec grep -l "anthropics/claude-code-action" {} \; 2>/dev/null
```

Also check for a `claude.yml` workflow:

```bash
ls .github/workflows/claude.yml 2>/dev/null
```

If no evidence of the Claude GitHub App is found, inform the user:

> The rules freshness audit requires the Claude GitHub App for authentication. Please run `/install-github-app` first to set it up. The app authenticates through your Anthropic subscription — no separate API key is needed.

Then stop. Do not proceed without the Claude GitHub App.

### Step 2: Check Project Prerequisites

1. Verify `.github/workflows/` directory exists. Create it if needed:
   ```bash
   mkdir -p .github/workflows
   ```

2. Check if `rules-freshness-audit.yml` already exists:
   ```bash
   ls .github/workflows/rules-freshness-audit.yml 2>/dev/null
   ```
   If it exists, ask the user if they want to update it.

3. Check for rules and CLAUDE.md files:
   ```bash
   find .claude/rules -name "*.md" -type f 2>/dev/null | head -20
   find . -name "CLAUDE.md" -o -name "CLAUDE.local.md" 2>/dev/null | grep -v node_modules | grep -v .git | head -20
   ```
   If no rules or CLAUDE.md files exist, warn the user that there's nothing to audit yet. Suggest they create some rules first, then install the workflow.

4. Discover the project's directory structure for smart path defaults:
   ```bash
   ls -d */ 2>/dev/null | head -20
   ```

### Step 3: Ask User for Configuration

Use AskUserQuestion to ask which source code paths should trigger the audit. Offer sensible defaults based on the project's actual directory structure.

Suggested defaults (only include directories that actually exist):
- `src/**` — if `src/` exists
- `lib/**` — if `lib/` exists
- `app/**` — if `app/` exists
- `packages/**` — if `packages/` exists

Always include these (they affect rules directly):
- `.claude/**`
- `CLAUDE.md`
- `**/CLAUDE.md`
- Config files: `*.config.*`, `package.json`, `tsconfig*.json`, `pyproject.toml`

Exclude from triggers (these rarely affect rules):
- `docs/**`, `*.md` (except CLAUDE.md)
- `tests/**`, `test/**`, `__tests__/**`
- `.github/**` (except the audit workflow itself)

### Step 4: Write the Workflow File

Read the template workflow from `${CLAUDE_PLUGIN_ROOT}/workflows/rules-freshness-audit.yml`.

Customize the `paths:` trigger filter based on the user's answers from Step 3.

The workflow uses the Claude GitHub App for authentication — no `ANTHROPIC_API_KEY` secret is needed.

Write the customized workflow to `.github/workflows/rules-freshness-audit.yml`.

### Step 5: Write the Pre-Check Script

```bash
mkdir -p .github/scripts
```

Copy the pre-check script from `${CLAUDE_PLUGIN_ROOT}/scripts/match-affected-rules.sh` to `.github/scripts/match-affected-rules.sh`.

Make it executable:
```bash
chmod +x .github/scripts/match-affected-rules.sh
```

### Step 6: Provide Next Steps

After successful installation, tell the user:

1. The workflow was installed at `.github/workflows/rules-freshness-audit.yml`
2. The pre-check script was installed at `.github/scripts/match-affected-rules.sh`
3. To test it: create a branch, make a code change in a path that an existing rule covers, and open a PR
4. The audit only runs when PRs touch files that existing rules care about — most PRs will be skipped
5. To skip the audit on a specific PR, add the `skip-rules-audit` label
6. Remind them to commit and push both files
