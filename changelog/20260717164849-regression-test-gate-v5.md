# Require tests for new features and a regression test for every bug fix

- Gate 4 of the injected verification protocol only required tests for a new "module", so a feature
  added inside an existing module fell through. It now says "module or feature" and states that new
  behavior needs new tests wherever it lands.
- Added a new standalone gate 5, "Regression test for bug fixes": every bug fix ships a test that
  fails before the fix and passes after, written test-first. Exemptions are named and narrow (typos
  in copy, build/CI config, dependency bumps, formatting).
- Why: nothing in the skill required a test for a bug fix, and the coverage gate could not backstop
  it. A bug fixed on an already-covered line does not move the coverage percentage, so the coverage
  command passes and the fix ships with no test. Coverage measures executed lines, not asserted
  behavior, which makes a regression test the exact case it is blind to.
- Gate 5 degrades on three paths keyed off source code, not tooling: enforced in a source repo with a
  test framework, kept as dormant prose in a source repo without one (it carries no command, so
  nothing empty or guessed gets injected), dropped only in a config/no-source repo. Two older
  passages still branched on "has tooling" and contradicted this for a source repo with no tooling;
  both now key off source.
- Renumbered as a consequence: code review is gate 6 (lenses 6a-6d, formerly 5a-5d) and docs
  alignment is gate 7. Updated every reference across SKILL.md and baseline-checklist.md.
- Bumped Skill version v4 to v5 and added the checklist row so re-run upgrade mode offers the gate to
  repos stamped v4, per the skill's maintainer loop.
