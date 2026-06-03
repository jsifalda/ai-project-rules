# ship-pr: GitHub fork fallback on push-denied

- Added a GitHub-only fallback to the `ship-pr` skill: when `git push` to origin is denied for lack of write access (403 / "Permission … denied"), it now forks the upstream, pushes the branch to the fork, and opens a cross-repo PR instead of aborting.
- Phase 2 captures `$ORIGIN_SLUG`; Phase 5d does the fork + push to a `fork` remote; Phase 5e opens the PR with `--repo`/`--head owner:branch`; Phase 6 reports the fork.
- Carved out the new path explicitly against the "abort on first failure" rule and the hard rules, so it reads as an alternate destination, not a bypass flag.
- Why: contributing to repos without write access is the common open-source case; aborting there was wrong. GitLab keeps the existing abort behavior (different fork+MR model, out of scope).
