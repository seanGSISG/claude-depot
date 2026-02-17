# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Skill Lifecycle Workflow

Skills use a three-stage progressive disclosure flow. Design your skill's content with this loading sequence in mind:

```
Stage 1: Metadata (always loaded, ~100 tokens)
  └── name + description from YAML frontmatter
  └── Used by the agent to decide IF the skill is relevant

Stage 2: Instructions (loaded on activation, <5000 tokens recommended)
  └── Full SKILL.md body (markdown)
  └── Core workflows, decision trees, script references

Stage 3: Resources (loaded on demand, unlimited)
  └── scripts/ — executed directly or read for patching
  └── references/ — loaded into context when needed
  └── assets/ — used in output, not loaded into context
```

**Design implications:**

- **Stage 1**: The description must contain all triggering information. "When to use" sections in the body (Stage 2) are invisible at trigger time.
- **Stage 2**: Keep SKILL.md under 500 lines. Use references for detailed documentation, schemas, and examples.
- **Stage 3**: Organize resources so Claude can load only what's needed for the current task. Domain-specific reference files are better than one large file.