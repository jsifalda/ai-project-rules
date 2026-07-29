# Stop tracking sync state in git

- Untracked all four `state/synced.txt` and `state/manifest.txt` files under `sync-mattpocock-skills` and `sync-anthropic-skills` (`git rm --cached`, working copies kept). `.gitignore` now covers `skills/*/state/` instead of just the per-destination subdir.
- These files are machine state, not source. The anthropic pair proved it: they baselined `design-critique`, a skill that is not in this repo at all and lives in an unrelated source tree, so the committed state described a sync whose output never landed here.
- Documented the consequence in both `SKILL.md` files rather than hiding it. A fresh clone has no baseline, so the first re-sync of an already-committed skill reports `[skipped: locally modified]` and needs `--force`. That fails safe, it never clobbers.
- Dropped the stale `design-critique` caveat from the anthropic skill, which only existed because that state was committed.
