# Anti-Patterns in Claude Code Rules and CLAUDE.md

> Sources: Claude Code documentation, community observations, production codebase audits.

## Table of Contents

- [The Kitchen Sink](#the-kitchen-sink)
- [Importing Volatile Source Files](#importing-volatile-source-files)
- [Negative-Only Constraints](#negative-only-constraints)
- [Linter Rules in CLAUDE.md](#linter-rules-in-claudemd)
- [MCP Tool Bloat](#mcp-tool-bloat)
- [Redundant Rules](#redundant-rules)
- [Contradictory Rules](#contradictory-rules)
- [Overly Broad Globs](#overly-broad-globs)
- [Copy-Paste Rules](#copy-paste-rules)
- [Stale Version Pins](#stale-version-pins)

## The Kitchen Sink

**Symptom**: CLAUDE.md or a rules file that grew via incremental accumulation to 500+ lines.

**Problem**: Important rules get lost in noise. Claude's attention is finite — when everything is "important," nothing is. Long files cause Claude to start ignoring instructions because they compete with each other for relevance.

**How to detect**: Check line count of each memory file. Files over 200 lines (for root CLAUDE.md) or 100 lines (for scoped rules) are candidates for splitting.

**Fix**: Apply the litmus test to every line: "Would removing this cause Claude to make mistakes?" Split large files into scoped rules with `paths:` frontmatter. Move reference material into dedicated reference files loaded on demand.

## Importing Volatile Source Files

**Symptom**: CLAUDE.md contains `@src/api/routes.ts` or similar imports pointing at actual codebase files.

**Problem**: Rules should be concise steering documents, not mirrors of code Claude can already read. Source files change frequently, creating constant drift between the import and reality. The imported content wastes context tokens on information Claude would get anyway when it reads the file.

**How to detect**: Look for `@` imports that point to files under `src/`, `lib/`, `app/`, or other source directories. Check if imported files have been modified more recently than the CLAUDE.md that imports them.

**Fix**: Remove volatile imports. Instead, describe the *pattern* or *convention* in the rule itself. Claude can read the actual source code when it needs the details.

**Exception**: Importing stable configuration files (`package.json`, `pyproject.toml`, `tsconfig.json`) is fine — they change infrequently and provide useful context.

## Negative-Only Constraints

**Symptom**: Rules that say "Never use X" or "Don't do Y" without providing an alternative.

**Problem**: Claude gets stuck. It knows what not to do but has no guidance on what to do instead. This often leads to Claude asking the user for clarification or making a random choice.

**How to detect**: Search rules for "never", "don't", "do not", "avoid", "prohibited" and check if each prohibition includes an alternative.

**Fix**: Always pair prohibitions with preferred alternatives:

Bad:
```
Never use the --foo-bar flag.
```

Good:
```
Never use the --foo-bar flag; use --baz-qux instead, which provides the same functionality without the side effects.
```

## Linter Rules in CLAUDE.md

**Symptom**: Rules files specifying code style — indentation width, semicolons vs. no semicolons, import ordering, bracket placement.

**Problem**: Code style enforcement belongs in linter/formatter configs (`.eslintrc`, `.prettierrc`, `ruff.toml`). Putting these in CLAUDE.md means: (1) they compete for attention with important architectural rules, (2) they can drift from the actual linter config, (3) Claude may follow the rule but the linter rejects the output anyway.

**How to detect**: Look for rules mentioning indentation, tabs, spaces, semicolons, trailing commas, import order, bracket style, line length, or other purely stylistic concerns.

**Fix**: Configure linters properly and use hooks to run formatters automatically. The `PostToolUse` hook with `Write`/`Edit` events can auto-format on every file change.

## MCP Tool Bloat

**Symptom**: Dozens of MCP tools configured, each with full JSON Schema definitions that consume 30k+ tokens before the user types anything.

**Problem**: MCP tool schemas load into context at session start. Each tool with a complex schema adds hundreds to thousands of tokens. With many tools, this leaves less room for actual instructions and conversation.

**How to detect**: Count configured MCP tools. Check total schema token usage. Look for tools that are rarely or never used.

**Fix**: Remove unused MCP tools. Consolidate tools where possible. For tools used only in specific workflows, consider loading them conditionally via skills rather than globally.

## Redundant Rules

**Symptom**: Instructions for things Claude already does correctly from training data.

**Problem**: Every redundant rule is noise that competes for attention with rules that actually matter. Telling Claude to "write clean code" or "use descriptive variable names" wastes context on behavior Claude already exhibits.

**How to detect**: Temporarily remove the rule and test if Claude's behavior changes. If behavior is identical, the rule is redundant.

**Common redundancies**:
- "Write clean, readable code" — Claude already does this
- "Add error handling" — Claude already adds appropriate error handling
- "Use TypeScript types" — Claude uses types naturally in TypeScript projects
- "Follow the existing code style" — Claude already mimics existing patterns
- Standard language idioms for the project's language

**Fix**: Delete the rule. Only keep rules that encode project-specific knowledge Claude can't infer from the code.

## Contradictory Rules

**Symptom**: Rules accumulated over time that give conflicting instructions, especially across different scope levels.

**Problem**: Claude receives contradictory instructions and has to guess which one takes precedence. This leads to inconsistent behavior across sessions.

**How to detect**: Compare instructions across all memory files. Look for:
- Global rule says one thing, scoped rule says the opposite
- Root CLAUDE.md conflicts with nested CLAUDE.md
- Different scoped rules give different instructions for overlapping file patterns

**Common contradictions**:
- Parent says "use CommonJS", child says "use ESM"
- One rule says "always use interfaces", another says "prefer type aliases"
- Test rules say "mock external calls", API rules say "use real HTTP in tests"

**Fix**: Establish a clear precedence (more specific scope wins) and remove the contradicted instruction from the broader scope. Or, make the broader rule explicitly defer: "See `rules/testing.md` for test-specific patterns."

## Overly Broad Globs

**Symptom**: Scoped rules with `paths: ["**/*"]` or `paths: ["src/**/*"]` that effectively match everything.

**Problem**: An overly broad glob defeats the purpose of scoping. The rule loads on nearly every file interaction, making it functionally a global rule but without being clearly identified as one.

**How to detect**: Check if a rule's glob pattern matches more than 50% of the project's files. If so, it's either too broad or should be a global rule.

**Fix**: Either narrow the glob to the specific files that need the rule, or remove the `paths:` frontmatter entirely and accept it as a global rule.

## Copy-Paste Rules

**Symptom**: The same instructions repeated across multiple scoped rules or CLAUDE.md files.

**Problem**: Duplicated rules create maintenance burden — when the convention changes, you need to update it in multiple places. Forgotten duplicates become contradictory over time.

**How to detect**: Look for identical or near-identical paragraphs across different memory files.

**Fix**: Move shared conventions to a global rule or root CLAUDE.md. Scoped rules should contain only what's unique to their scope.

## Stale Version Pins

**Symptom**: Rules reference specific version numbers that have since changed (e.g., "keep the Docker image at Python 3.11" when the project now uses 3.12).

**Problem**: Claude follows the stale pin and produces output with the wrong version.

**How to detect**: Extract version references from rules, cross-check against `package.json`, `pyproject.toml`, `Dockerfile`, and other version-defining files.

**Fix**: Either update the version pin or, better, reference the source of truth: "Keep the Docker image Python version aligned with the version in `pyproject.toml`."
