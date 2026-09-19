# Split rules into an always-loaded core and on-demand rule files

- `rules/general.md` cut from ~4,830 to ~2,500 tokens. It now opens with a trigger table that
  routes to every other rule file.
- New on-demand rule files: `authoring.md` (how to write an instruction, plus the counts ban),
  `testing.md`, `git-ship.md`, `browser.md`, `docs-diagrams.md`.
- Why: `general.md` loads on every session for every consumer. Testing rules, git and MR
  format, browser automation and doc conventions only matter once that work starts, so they
  were being paid for on every unrelated request.
- `authoring.md` is the durable part: it sets a token cap on the always-loaded tier, bans
  rationale and examples from an instruction, and states the test a rule must pass to be
  always-loaded. Load-bearing rationale belongs in the commit message instead.
- `README.md` and `CLAUDE.md` updated to describe the new layout. The counts rule moved from
  `general.md` to `authoring.md`, and `CLAUDE.md` now points at the new location.
- Review caught several rules dropped in the first pass and they were restored: the
  `always_apply` frontmatter on `general.md`, the AGENTS.md-first directive, the tooling-directive
  carve-out, a self-contained comments policy, the assumptions and error-handling rules, and the
  dependency carve-out that keeps `fetch` winning over an already-installed `axios`.
