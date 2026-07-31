# Keep Mermaid in the skills, remove it only from the global rules

- Reverted `create-codebase-docs`, `obsidian-markdown`, and `sync-obsidian-skills` to their
  previous state. Mermaid stays there.
- Why: their output targets render Mermaid natively (GitHub for `STARTHERE.md`, Obsidian
  for notes), so ASCII was a downgrade. Only `rules/general.md` needed it gone, because
  its old section mandated npm installs to validate diagrams.
- Added a native-renderer exception to `rules/general.md`'s `## Diagrams`, and narrowed the
  ban to the toolchain rather than the syntax. Why: that file loads every session, so
  without a named exception the next agent strips the skills again.
- Corrections to `20260731134002`, which cannot be edited: the Mermaid removal is scoped to
  the global rules, not repo-wide, and the `CLAUDE.md` section landed as
  `## Verification Protocol (MANDATORY)`, not `## Verification Gate`.
