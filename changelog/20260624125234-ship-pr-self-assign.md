# ship-pr: self-assign the new PR/MR

- `ship-pr` skill now self-assigns the opened PR/MR to the authenticated CLI user. GitHub uses `gh pr create --assignee "@me"`; GitLab resolves the username via `glab api user` and passes `--assignee`.
- The GitHub fork-fallback path skips `--assignee` on create (you usually lack assign rights upstream) and instead does a best-effort `gh pr edit --add-assignee` afterwards.
- Why: removes a manual step — no more opening the PR/MR in the web UI to assign yourself.
- Self-assignment is best-effort and never aborts the ship.
