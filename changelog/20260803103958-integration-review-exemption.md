# Integration-only sessions skip the code-review lenses

- Added an exemption to this repo's `## Verification Protocol` and to the block
  `setup-aiengineering` injects: a session whose only change is integrating already-reviewed work
  (merge, rebase, cherry-pick, revert) with no new lines authored skips the code-review lenses, and
  only those. Every other gate still runs.
- Why: a merge burned CodeRabbit credits and a review-agent round on lines already reviewed on the
  branch they came from. Nothing new was authored, so there was nothing new to find.
- The exemption is void the moment a line neither side had gets written, and the skip must be
  reported with the git diff proving nothing was authored — never silent.
- Bumped the `setup-aiengineering` baseline to v9 so repos stamped v8 are offered the change on
  re-run.
