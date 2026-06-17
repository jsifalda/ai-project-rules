# Autocommit changelog entries with related changes

- Added a "Commit the entry (autocommit)" rule to the `## Changelog` policy in `CLAUDE.md`.
- Now every new changelog entry is committed automatically, bundled with the related session changes in one local commit (conventional format, targeted staging, hooks run, no push).
- Why: entries were piling up uncommitted in the working tree — the policy described when to write an entry but never said to commit it.
