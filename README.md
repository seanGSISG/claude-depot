# claude-depot

A curated depot of Claude Code plugins — skills, tools, and extensions.

## Installation

Add the marketplace to Claude Code:

```
/plugin marketplace add seanGSISG/claude-depot
```

Then install any plugin:

```
/plugin install skill-creator-enhanced@claude-depot
```

## Available Plugins

### skill-creator-enhanced
Guide for creating effective Claude Code skills with templates, validators, and packaging tools.

**What it provides:**
- 6-step skill creation workflow (understand → plan → init → edit → package → iterate)
- Python scripts for initializing, validating, and packaging skills
- Reference docs on workflow patterns and output patterns
- Progressive disclosure design principles

**Triggers when you:**
- Ask to create a new skill
- Want to update or improve an existing skill
- Need help structuring a skill's resources

## Contributing

To add a new plugin, create a subdirectory under `plugins/` with a `.claude-plugin/plugin.json` manifest and update the root `marketplace.json`.

## License

MIT
