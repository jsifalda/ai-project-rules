# Fix `op` transcript lookup in worktrees

- `verify-models.py` built the project transcript directory name by replacing `/` with `-`, but
  Claude Code replaces every non-alphanumeric character. A dot-directory therefore doubles the dash
  it follows, so the no-argument invocation the skill documents failed in any worktree under
  `.claude/`.
- Replaced the single-character assumption with a rule covering all non-alphanumerics, which matches
  the real encoder rather than guessing again on the next surprise character.
- The not-found error now names where transcripts live and how to pass one, so the failure is
  self-serve.
- No fallback scan across project directories. Analysing another project's transcript would report
  confident, wrong routing results — a clear failure is better.
- Known limit, stated in the docstring rather than hidden: a slug over 200 characters is truncated
  and hashed by Claude Code, which this does not reproduce.
