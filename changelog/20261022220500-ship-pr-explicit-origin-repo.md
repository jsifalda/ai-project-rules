# ship-pr targets origin explicitly

- `ship-pr` now reads the `owner/repo` of `origin` from the remote URL in Phase 1, with no network call.
- Every `gh` call in the main GitHub block now names that repo or the PR URL.
- Phase 1 default-branch lookup also names the origin repo.
- Failure messages now include `--repo <slug>` in the manual command.
- Why: in a fork clone made with `gh repo clone`, gh's default repo is the upstream. A bare `gh pr create` opened a duplicate PR there instead of finding the open PR on the fork.
