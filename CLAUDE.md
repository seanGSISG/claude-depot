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

## Release Workflow

The GitHub Actions workflow at `.github/workflows/release-skills.yml` automates building and releasing `.skill` files.

**Trigger patterns:**
- Tag `v*` (e.g., `v1.2.0`) — builds **all** skills, creates a release
- Tag `<skill-name>-v*` (e.g., `trmm-expert-v2.0.0`) — builds **only** that skill

**What it does:**
1. Discovers all skills under `plugins/*/skills/*/`
2. Runs `quick_validate.py` on each — fails the build if any skill is invalid
3. Packages each into a `.skill` ZIP with correct directory structure
4. Attaches `.skill` files to a GitHub Release with auto-generated notes

**To release:**
```bash
git tag -a v1.1.0 -m "Description of changes"
git push origin v1.1.0
```

## Commits

Use conventional commit format: `feat:`, `fix:`, `docs:`, `chore:`. Descriptive messages explaining "why", not "what".

## Key Files

| File | Purpose |
|---|---|
| `.claude-plugin/marketplace.json` | Plugin registry — must be updated when adding/removing plugins |
| `.gitignore` | Excludes `*.skill`, `__pycache__/`, `*.pyc`, `*.pyo`, `.DS_Store` |
| `plugins/skill-creator-enhanced/scripts/quick_validate.py` | Skill validator — checks frontmatter, name format, description length |
| `plugins/skill-creator-enhanced/scripts/package_skill.py` | Skill packager — creates `.skill` ZIP archives |
