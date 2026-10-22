# ship-pr origin slug review fixes

- `norm_remote` now removes a port from a scheme-form remote URL. A remote such as `ssh://git@ssh.github.com:443/o/r` gave a four-part slug that `gh --repo` rejects.
- The main GitHub block reads the branch name from git, not from a pasted value. A branch name can hold `$(...)`, and a pasted value ran it.
- The existing-PR fallback no longer filters by `--author "@me"`. It filters out cross-repository PRs, so it finds an open PR that a teammate or a bot opened on this branch.
- The Phase 1 comment now says that only the main GitHub block names the slug.
- Why: review findings on the origin-slug change.
