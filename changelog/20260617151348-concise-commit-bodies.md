# Make commit bodies why-focused so they don't pollute MR descriptions

- Rewrote `## GIT Commit Guidelines` in `rules/general.md`: body is now optional and
  why/impact-focused (1-2 bullets), never a file-by-file change inventory.
- Tightened the `ship-pr` skill's commit-body line to match.
- Why: a single-commit MR/PR uses the commit body verbatim as its description (GitLab,
  GitHub). The old "lists key changes and additions" rule produced noisy, inventory-style
  MR descriptions across all tools that read these rules.
