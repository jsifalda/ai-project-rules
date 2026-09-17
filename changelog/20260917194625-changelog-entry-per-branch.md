# One changelog entry per branch

- The changelog rule now keys an entry to the branch, not the agent session. A later session on
  the same branch extends the branch's entry. Entries already on the default branch stay
  immutable. Changed in `setup-changelog` (skill body and the injected policy template), this
  repo's own `## Changelog` section, and the README summaries.
- PR 167 carried two entries because two sessions built one branch, and each followed "one file
  per session" to the letter. A reader reads a PR, and one PR should read as one entry.
- `setup-aiengineering` needed no edit. It delegates the changelog module to `setup-changelog`
  by name and carries no wording of its own.
