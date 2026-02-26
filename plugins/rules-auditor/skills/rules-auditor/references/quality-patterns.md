# Quality Patterns for Claude Code Rules and CLAUDE.md

> Sources: Claude Code documentation on memory files, rules, and progressive disclosure; real-world examples from production codebases.

## Table of Contents

- [The Litmus Test](#the-litmus-test)
- [Root CLAUDE.md Guidelines](#root-claudemd-guidelines)
- [Path-Scoped Rules Guidelines](#path-scoped-rules-guidelines)
- [Nested CLAUDE.md Guidelines](#nested-claudemd-guidelines)
- [Emphasis and Priority](#emphasis-and-priority)
- [The Progressive Disclosure Tiers](#the-progressive-disclosure-tiers)
- [Effective @imports](#effective-imports)
- [Measuring Rule Effectiveness](#measuring-rule-effectiveness)

## The Litmus Test

For each line in any rules or CLAUDE.md file, ask:

**"Would removing this line cause Claude to make mistakes?"**

If the answer is no, cut it. Every line competes for context attention. Unnecessary instructions dilute the important ones.

A related test: **"Can Claude figure this out by reading the code?"** If yes, don't put it in rules. Rules should encode knowledge that isn't obvious from the codebase itself — architectural decisions, non-obvious conventions, workflow requirements, things that look wrong but are intentional.

## Root CLAUDE.md Guidelines

The root `CLAUDE.md` is loaded on every session. It's the most expensive file in terms of context — it's always present, always competing for attention.

### What to Include

- **Essential commands**: Build, test, lint, format commands — the ones Claude needs to verify its work
- **Stack overview**: One-paragraph summary of the tech stack (framework, language, database, key libraries)
- **Architectural decisions**: Non-obvious choices that would trip Claude up (e.g., "We use CommonJS, not ESM" or "All API responses wrap in `{data, error}` envelope")
- **Pointers to deeper docs**: `@imports` for stable reference files, links to scoped rules
- **Key file paths**: Entry points, config files, important directories — but only if the structure is non-obvious

### What to Exclude

- **Standard language conventions**: Claude already knows how to write TypeScript, Python, etc.
- **Things inferable from code**: Import patterns, variable naming, file structure — Claude can see these
- **Detailed API documentation**: This belongs in reference files loaded on demand
- **Linter/formatter rules**: These belong in `.eslintrc`, `.prettierrc`, etc. Use hooks for enforcement
- **Long lists of files**: Claude can use `find` and `glob` to discover files

### Target Length

Keep root CLAUDE.md to **60-150 lines** of universally applicable instructions. If it exceeds 200 lines, it likely contains content that should be scoped rules or reference files instead.

## Path-Scoped Rules Guidelines

Scoped rules (`.claude/rules/*.md` with `paths:` frontmatter) are the primary mechanism for progressive disclosure. They load only when Claude reads files matching their globs.

### Structure

Each rule file should cover **one domain** — a coherent set of conventions for a specific area of the codebase:

- `testing.md` — test conventions, test utilities, mocking patterns
- `api-design.md` — endpoint structure, validation, error handling
- `database.md` — migration patterns, query conventions, ORM usage
- `deployment.md` — CI/CD conventions, environment variables, Docker patterns

### Paths Frontmatter

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/routes/**/*.ts"
---
```

Supported glob patterns:
- `**/*.ts` — all TypeScript files anywhere
- `src/**/*` — everything under src/
- `src/**/*.{ts,tsx}` — TypeScript and TSX files under src/
- `{src,lib}/**/*.ts` — TypeScript files under src/ or lib/
- `tests/**/*` — everything under tests/

**Rules without `paths:`** are global — they load on every session, just like root CLAUDE.md. Use this sparingly, only for cross-cutting concerns (code review philosophy, commit conventions, quality gates).

### Organization

Group rules into subdirectories for large projects:

```
.claude/rules/
  backend/
    api-design.md
    database.md
    error-handling.md
  frontend/
    components.md
    state-management.md
    styling.md
  deployment/
    docker.md
    ci-cd.md
```

### Content Guidelines

- **Describe patterns, not lint rules**: "All API endpoints return `{data, error}` envelopes" not "use semicolons"
- **Be specific to the matched files**: If the rule scopes to `src/api/**`, every instruction should be about API code
- **Include examples**: Short code snippets showing the preferred pattern are more effective than prose descriptions
- **Explain why**: "We use repository pattern because it enables transaction testing" helps Claude make analogous decisions

## Nested CLAUDE.md Guidelines

Nested CLAUDE.md files work differently from rules:

- **Ancestor files** (upward from cwd to repo root): loaded eagerly at startup
- **Descendant files** (below cwd): loaded lazily when Claude reads files in that subtree

### When to Use

Nested CLAUDE.md is best for **monorepo component boundaries**:

```
CLAUDE.md                    # Root: universal instructions
frontend/CLAUDE.md           # Frontend-specific: React conventions, build commands
backend/CLAUDE.md            # Backend-specific: API patterns, database conventions
deploy/CLAUDE.md             # Deployment-specific: Docker, CI conventions
```

### Keep Concise

All ancestor CLAUDE.md files accumulate — they all compete for context attention together with root CLAUDE.md. A nested CLAUDE.md should be **30-60 lines** at most, covering only what's unique to that subtree.

### Avoid Duplication

Don't repeat instructions from parent CLAUDE.md files. The nested file should only contain what's different or additional for that directory subtree.

## Emphasis and Priority

When certain rules are critical:

- Use **"IMPORTANT:"** or **"MANDATORY:"** prefix for rules that must be followed
- Always provide alternatives with prohibitions: **"Never use X; prefer Y instead"**
- More specific (nested/scoped) instructions take precedence over broader ones
- If two rules conflict, the more deeply scoped one wins

Example:
```markdown
IMPORTANT: Never use `any` type in TypeScript. Use `unknown` when the type is genuinely unknown,
or define a proper interface.
```

## The Progressive Disclosure Tiers

An effective setup uses tiered context that loads progressively:

### Tier 0: Root CLAUDE.md

The gateway. Contains universal directives, `@imports` for stable references, and pointers to deeper context. Always loaded. Keep minimal.

### Tier 1: Global Rules (no `paths:`)

Cross-cutting philosophy, workflow requirements, quality gates. These load on every session but are separate files from root CLAUDE.md, allowing better organization.

Examples: code review checklist, commit message format, PR description requirements.

### Tier 2: Scoped Rules (`paths:` frontmatter)

Implementation patterns specific to directory/file subsets. Load on demand when Claude reads matching files.

Examples: API endpoint patterns, test conventions, component structure, database migration rules.

### Tier 3: Referenced Docs and Skills

Deep dives loaded explicitly on demand via reference files or skill invocation. These never load automatically — Claude reads them only when the topic arises.

Examples: Architecture decision records, API reference docs, deployment runbooks.

### Context Budget

Consider the total tokens consumed:
- Tier 0 + Tier 1: Always loaded. Budget ~2000-4000 tokens total.
- Tier 2: Loaded per-file. Each scoped rule should be ~200-800 tokens.
- Tier 3: Loaded on demand. Can be as long as needed.

## Effective @imports

The `@imports` directive in CLAUDE.md loads external files as context:

```markdown
@README.md
@package.json
```

### Good imports

- `README.md` — stable project overview
- `package.json` / `pyproject.toml` — dependency list (changes infrequently)
- Architecture decision records
- API schema files (OpenAPI, GraphQL schema)

### Bad imports

- Source code files (`@src/api/routes.ts`) — these change frequently, creating maintenance burden and duplicating what Claude can already read on demand
- Large generated files — waste context tokens
- Files that duplicate information already in CLAUDE.md

## Measuring Rule Effectiveness

To assess whether a rule is working:

1. **Temporarily remove the rule** and observe if Claude's behavior changes
2. **Check for compliance**: Do code suggestions follow the rule without being reminded?
3. **Count corrections**: If you frequently need to correct Claude on a topic, the rule may be unclear
4. **Watch for contradictions**: If Claude produces output that conflicts with a rule, the rule may be poorly worded or contradicted by another rule
