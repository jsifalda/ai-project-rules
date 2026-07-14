# File Organization Template

Inject the section below into the project's agent instructions file. Copy it verbatim.

---

## File Organization

- All documentation and markdown files (guides, explorations, architecture docs, notes) go in the
  `docs/` folder — never the repository root.
- Only these files belong at the root: `README.md`, `AGENTS.md`, `LICENSE`.
- Planning artifacts (implementation plans, scoping docs) go in `plans/`.
- Link every new reference doc (guides, ADRs, architecture notes) from the `## Documentation` section
  of `README.md` in the same change that adds it, so it stays discoverable — create that section if it
  is missing. Scratch / exploration notes are excepted. This applies to docs-only changes too.
