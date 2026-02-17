# claude-depot

Claude Code plugin marketplace. Repo: `seanGSISG/claude-depot`.

## Repo Structure

```
.claude-plugin/marketplace.json   # Marketplace registry — lists all plugins
.github/workflows/release-skills.yml  # CI: builds .skill files on tagged releases
plugins/
  <plugin-name>/
    .claude-plugin/plugin.json    # Plugin manifest (name, description, version, author)
    skills/
      <skill-name>/
        SKILL.md                  # Skill definition (YAML frontmatter + markdown body)
        references/               # Reference files loaded by the skill on demand
```

## Adding a New Plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` matching the pattern in existing plugins.
2. Create `plugins/<name>/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`) and a markdown body.
3. Add reference files under `references/` — use relative paths in SKILL.md (e.g., `references/foo.md`).
4. Validate with: `python plugins/skill-creator-enhanced/scripts/quick_validate.py plugins/<name>/skills/<name>`
5. Add an entry to `.claude-plugin/marketplace.json` in the `plugins` array.
6. Update `README.md` with the plugin description.

## Skill Conventions

- **SKILL.md frontmatter** must have `name` (lowercase, hyphens only, must match directory name) and `description` (under 1024 chars, comprehensive trigger phrases).
- **Reference files** use relative paths. No `${CLAUDE_PLUGIN_ROOT}` in SKILL.md — that variable only works in hook/MCP JSON configs.
- **Strip images** from reference files — `![alt](path)` patterns are useless to Claude. Keep surrounding text.
- **Replace relative links** with prose: "See the X section in references/Y.md" instead of `[X](../path)`.
- **Add a Table of Contents** to any reference file over 100 lines.
- **Add `> Sources:` line** to reference files listing original source documents.

## Validation and Packaging

```bash
# Validate a skill (must pass before packaging)
python plugins/skill-creator-enhanced/scripts/quick_validate.py plugins/<name>/skills/<name>

# Package a skill into a .skill ZIP (for manual distribution)
cd plugins/skill-creator-enhanced/scripts
python package_skill.py /path/to/skills/<name> /output/dir
```

`.skill` files are ZIP archives containing `<skill-name>/SKILL.md` + `<skill-name>/references/*`. They work in Claude.ai, Claude Desktop, and Claude Code.

## Versioning

There are two distribution channels, each keyed off a different version source:

| Channel | Version Source | Who Consumes It |
|---|---|---|
| **Plugin marketplace** (`/plugin install`) | `version` in `plugins/<name>/.claude-plugin/plugin.json` | Claude Code users |
| **GitHub Releases** (`.skill` downloads) | Git tag (e.g., `trmm-expert-v1.1.0`) | Claude.ai / Claude Desktop users |

**These must stay in sync.** If you change plugin code but don't bump `plugin.json` version, marketplace users won't see the update (Claude Code caches by version string). If you bump `plugin.json` but forget the tag, `.skill` downloads won't be built.

### Releasing a Plugin Update

Use the bump script to update `plugin.json` and create the tag atomically:

```bash
# Bump version, commit, and create tag in one step
./scripts/bump-version.sh trmm-expert 1.1.0

# Review, then push both commit and tag
git push && git push origin trmm-expert-v1.1.0
```

The CI workflow will:
1. Verify the tag version matches `plugin.json` (fails the build if mismatched)
2. Validate the skill with `quick_validate.py`
3. Package and attach the `.skill` file to a GitHub Release

### Version Rules

- Use semver: `MAJOR.MINOR.PATCH` (e.g., `1.2.0`)
- Bump PATCH for reference content updates and fixes
- Bump MINOR for new reference files, SKILL.md routing changes, or new features
- Bump MAJOR for breaking changes (restructured references, renamed files)
- Never reuse a version number — Claude Code caches by exact version string

### Tag Patterns

| Pattern | Example | Behavior |
|---|---|---|
| `<plugin>-v<semver>` | `trmm-expert-v1.1.0` | Builds only that plugin's skill, verifies version match |
| `v<semver>` | `v2.0.0` | Builds all skills (use for coordinated multi-plugin releases) |

### What Happens When You Forget

- **Changed code, didn't bump version:** Marketplace users stay on the old cached version. Fix: bump version and re-release.
- **Bumped plugin.json, didn't tag:** No `.skill` file built. Marketplace users get the update, but Claude.ai/Desktop users don't. Fix: create the tag.
- **Tag version doesn't match plugin.json:** CI fails the build and tells you what to fix.

## Release Workflow

The GitHub Actions workflow at `.github/workflows/release-skills.yml` automates building and releasing `.skill` files.

**Steps:**
1. Verifies tag version matches `plugin.json` version (for single-plugin tags)
2. Discovers all skills under `plugins/*/skills/*/`
3. Runs `quick_validate.py` on each — fails the build if any skill is invalid
4. Packages each into a `.skill` ZIP with correct directory structure
5. Attaches `.skill` files to a GitHub Release with auto-generated notes

## Commits

Use conventional commit format: `feat:`, `fix:`, `docs:`, `chore:`. Descriptive messages explaining "why", not "what". Version bumps use `chore(<plugin>): bump version to X.Y.Z`.

## Key Files

| File | Purpose |
|---|---|
| `.claude-plugin/marketplace.json` | Plugin registry — must be updated when adding/removing plugins |
| `.gitignore` | Excludes `*.skill`, `__pycache__/`, `*.pyc`, `*.pyo`, `.DS_Store`, `dist/` |
| `scripts/bump-version.sh` | Version bump helper — updates plugin.json, commits, and creates git tag |
| `plugins/skill-creator-enhanced/scripts/quick_validate.py` | Skill validator — checks frontmatter, name format, description length |
| `plugins/skill-creator-enhanced/scripts/package_skill.py` | Skill packager — creates `.skill` ZIP archives |
