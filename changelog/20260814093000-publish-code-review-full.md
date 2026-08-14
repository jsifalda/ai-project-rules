# Make code-review-full safe to publish

- Added the `code-review-full` skill, moved in from a private repo, after an audit for
  publishable content.
- Removed a hardcoded Atlassian tenant id from the spec-conformance reference. The skill now
  resolves the reader's own Atlassian site at run time and asks when more than one is accessible.
- Anonymized the incident evidence the skill teaches from: employer brand token, real
  merge-request numbers, and real source filenames. The narratives and their line numbers stay,
  because they are what stops an agent relaxing the rules.
- Replaced an absolute home path in an example with a `<cwd>` form.
- Added the skill's row to the README table.
- Why: the repo is public and reusable, so nothing may carry an employer identity or a value
  true only on one machine.
