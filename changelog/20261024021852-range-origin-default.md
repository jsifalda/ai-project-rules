# Range PR diffs against the origin default branch

- Added a `## Ranges` rule to `rules/git-ship.md`: range a diff or log against `origin/<default>`, never a bare local default branch name.
- Widened the `rules/git-ship.md` trigger in `rules/general.md` to any PR or MR work, so the rule loads before the first diff.
- Why: a PR-branch clone has no local default branch, so `main...HEAD` exits 128.
