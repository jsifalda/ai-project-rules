# Add learn-taste skill

- Vendored `learn-taste` from emilkowalski/skills (MIT) and added its README row.
- Made it universal: it learns any user correction, not only design taste, and saves each rule by scope to `DESIGN.md`, the project `CLAUDE.md`, the global rules, or memory.
- Made it restricted invocation, so the agent can call it only through the named entry points.
- Kept `distill-insight`, which distills one rule from one repeated failure.
