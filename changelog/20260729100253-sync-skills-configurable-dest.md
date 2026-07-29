# Configurable destination for the skill sync scripts

- `sync-mattpocock-skills` and `sync-anthropic-skills` gained a `--dest <dir>` flag. Both previously hardcoded their target to this repo's `skills/`, so pulling upstream skills into another project meant copying files by hand.
- Sync state is now per-destination. The default target keeps its tracked `state/` files, any other target gets `state/dests/<slug>/`, gitignored. Without the split, two folders would share one overwrite baseline and one "previously-synced" set.
- The slug is a hash of the destination path, never the path itself, so a local folder name cannot leak into this public repo.
- Fixed a latent bug in `sync-mattpocock-skills`: its path resolution was logical, so running it through the `~/.claude/skills` symlink would have written outside the repo. `sync-anthropic-skills` already had the `-P` fix.
- A missing `--dest` is created rather than rejected, and the resolved destination is now printed at the start and in the summary.
