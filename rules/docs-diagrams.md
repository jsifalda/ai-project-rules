# Documentation and diagrams

## Documentation

- Write only what code cannot state: the constraint, the option that lost, the failure it prevents.
- Apply the deletion test. If a reader would get nothing wrong once the line is gone, delete it.
- Prefer a clear name, a type, or a test. Reach for a doc last.
- Argue a decision once. Link to it everywhere else.
- Put a module-wide why in the project's decision record, never a comment.
- Never open a doc surface the project does not already keep.
- Set length by these rules. There is no word limit.

## Diagrams

- Draw one only when a picture beats words on something complex.
- Default to inline ASCII or box-drawing: trees, boxes and arrows, flows.
- Use a fenced `mermaid` block where the output renders it natively and a skill calls for it. Never convert those to ASCII.
- Use ASCII in the terminal and in chat.
- Ask first before a rendered image, an interactive diagram, or a diagramming tool.
- Keep one idea per diagram, roughly 15 nodes. Split, never cram.
- Label every edge.
- Never create a standalone `.mmd` file. Never install a renderer or parser.

## Counts

- `rules/authoring.md` under `## Counts` holds the whole rule. Read it there.
