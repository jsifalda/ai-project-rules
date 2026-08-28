# File Organization Template

Inject the section below into the project's agent instructions file. Copy it verbatim.

---

## File Organization

- Only these files belong at the root: `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `LICENSE`.
- Every other documentation and markdown file (guides, explorations, notes) goes in the `docs/`
  folder — never the repository root.
- Planning artifacts (implementation plans, scoping docs) go in `plans/`.
- New reference docs in `docs/` should be linked from `README.md`'s documentation section, so they
  stay discoverable (scratch / exploration notes excepted).
- **Documentation never goes inside the agent instructions file.** That file holds directives and
  read-first pointers only — see the scope block at the top of it for which document owns what.
