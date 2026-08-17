# Stop a dangling symlink from killing the skills sync

- `sync-skills.js` now finds an existing entry with `lstat`, not `existsSync`. `existsSync`
  follows a link, so it reported "not there" for a dangling symlink while the name still held
  the directory entry. `symlinkSync` then failed with `EEXIST`.
- Each skill now has its own error handler. Before, one bad entry reached the single top-level
  handler and left every remaining skill unlinked. A failure is now counted and reported, and
  the run continues.
- Why: the same defect stopped the Copilot counterpart script for five days, and no message
  showed the sync was incomplete. The Claude Code script held the same defect, unfired.
- No new dependency.
