# Keep the agent-instructions file directive-only in `setup-aiengineering`

- The `AGENTS.md` / `CLAUDE.md` this skill writes now holds agent directives and read-first
  pointers only. Documentation goes to `README.md`, `ARCHITECTURE.md`, or `docs/adr/`, and the
  agent file points at it with a rule that names the trigger.
- New `references/instructions-scope.md`, injected in Step 1 for every repo and not deselectable.
  It carries the content-homes table and the fallbacks for a repo that has no `ARCHITECTURE.md` or
  ADR directory.
- Step 3 backfill now writes to `README.md` and `ARCHITECTURE.md` instead of the agent file. It was
  the direct cause of the problem.
- Re-runs now scan the agent file for documentation that drifted back in, and offer to relocate it
  per section. It reports and asks, never moves on its own.
- The verification protocol's docs-alignment gate gained a scope check, which survives the
  markdown-only exemption — a docs-only session is exactly how documentation reaches an
  instructions file.
- Why: a real `CLAUDE.md` this skill produced had grown to 51 KB, with about 55 bullets of
  architecture rules and traps. The file's own "instructs, not explains" test had passed them,
  because they were written as imperatives. The test now asks whether a line binds every session,
  which a body of project knowledge does not, however it is phrased.
- Baseline checklist bumped v12 to v13 with two rows, so a re-run offers this to older setups.
