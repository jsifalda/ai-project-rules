# Documentation and diagrams

Load when writing a doc, an ADR, a README, or a diagram.

## Documentation

- Code is the record. Prose holds only what code cannot state: the constraint, the option that
  lost, the failure it prevents.
- The deletion test: what does a reader get wrong once the line is gone? "Nothing, they would
  read the code" → delete it.
- Prefer a clear name, a type, or a test. A doc is the last place for a fact.
- Argue a decision once. Every other place states what to do and links to it.
- A module-wide why goes to the project's decision record, never a comment.
- Never open a doc surface the project does not already keep.

## Diagrams

- Diagram when a picture beats words on something complex. Never force one onto simple things.
- Default: inline ASCII or unicode box-drawing — trees, boxes and arrows, flows.
- A fenced ` ```mermaid ` block is correct where the output renders it with no extra tooling,
  such as GitHub markdown or Obsidian, and a skill calls for it. Never convert those to ASCII.
  ASCII governs terminal and chat.
- Dense architecture with many nodes and relationships, or a multi-step flow → ask first, then
  use a diagramming tool the environment already provides.
- One idea per diagram, roughly 15 nodes maximum. Split, never cram.
- Label every edge.
- Never create a standalone `.mmd` file. Never install a renderer or parser to preview or
  validate.

## Counts in instructions

`rules/authoring.md` holds the whole rule. Read it there.
