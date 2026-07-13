# setup-aiengineering: self-audit + versioned re-run upgrade

- Added a `references/baseline-checklist.md` (canonical baseline concerns + a skill version) and a
  Step 8b coverage self-audit that reports any concern a repo is missing, so gaps surface as skill
  output instead of a later one-off PR.
- Made the provenance note carry a version stamp, and added Step 1 re-run upgrade mode: an older
  setup is offered the newer concerns and its drifted injected blocks are refreshed (diff-and-ask,
  never clobber).
- Guarded the Step 6 delegated skills for availability (mirrors review lens 5c), host-gated the
  Step 7 worktree module on Claude Code, and made Step 5 confirm detected commands before they ship
  into a mandatory gate.
- Why: the skill had been patched reactively through many follow-up PRs. These changes let it detect
  its own gaps and propagate fixes through re-runs, and stop three steps from failing silently.
