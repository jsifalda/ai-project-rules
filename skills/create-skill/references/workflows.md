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

## When not to prescribe steps

Sequential steps work when the order genuinely matters. Most of the time it doesn't — and over-prescribed steps strip Claude of its ability to adapt, recover from errors, or find a better path. Describe the outcome, not the route to it.

**Describe what to achieve, not each step:**

- ❌ *"Step 1: Read the config file. Step 2: Find the database URL. Step 3: Update the port number. Step 4: Write the file back."*
- ✅ *"Update the database port in the config file to the value specified by the user."*

**Provide constraints, not procedures:**

- ❌ *"Step 1: Create a branch. Step 2: Make the change. Step 3: Run tests. Step 4: Open a PR."*
- ✅ *"Always run tests before opening a PR. Never push directly to main."*

**Rule of thumb**: if the exact order of steps is load-bearing — doing step 3 before step 2 breaks everything — that's not a skill problem, it's a scripting problem. Move the sequence into a script under `scripts/` and have the skill call it.