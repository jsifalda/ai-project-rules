# Add How it works section to code-review-full

- Added a `## How it works` section to the `code-review-full` skill, placed before `## Invocation`.
- The section holds an ASCII pipeline map, a table of what the skill calls at each stage, a table
  of its caps, and a table of its gates.
- No behaviour changed. The section documents what the skill already did.

Why: the skill runs a pipeline of many stages across several delegates and bundled scripts. Its
caps and gates were spread over the stage prose and the reference files. A reader could not tell
what the skill calls, in what order, or where it stops without reading the whole file.
