# Git, commits, and merge requests

Load before a commit, a push, or opening a PR or MR.

## Destructive operations — ask first, every time

Never run these without an explicit instruction in chat.

- `git`: force-push (`--force`, `--force-with-lease`, `-f`), delete a remote branch or tag
  (`git push --delete`, `git push origin :ref`), push to a default or protected branch,
  rewrite pushed history.
- `glab`: `mr close`, `mr delete`, `mr merge`, `issue close`, `issue delete`, `repo delete`,
  `release delete`.
- Default to read-only `glab`: `mr view`, `mr list`, `mr diff`, `ci view`, `issue view`.
- Genuinely needed → stop, state what and why, wait for approval.

## Commit messages

- Conventional commits: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `perf:`,
  with an optional `(scope)`.
- Subject: imperative, 72 characters or fewer, no articles, no trailing period, task or issue
  ID when one exists. The subject line is exempt from the writing-style rules.
- The PR or MR title keeps the same conventional-commit format, and is exempt the same way.
- Body optional and why-focused. Write one only when the reason or impact is not obvious from
  the subject plus the diff. One or two short bullets. Never a file-by-file list.
- Example: `feat(module): add payment validation logic, #ISSUE-ID`.

## MR and PR descriptions

- A single-commit MR or PR uses the commit body verbatim as its description.
- Description is `## Summary` only, or the clean commit body verbatim.
- No `## Test plan` or `## Testing` section unless asked. No checklists, no how-to-verify
  boilerplate.
- Write the commit body as a clean description, not a change inventory.

## Git inside an isolated worktree (`.claude/worktrees/*`)

- Run git as `/usr/bin/git -C <worktree> ...`. A bare `git ...` is rewritten to `rtk git ...`
  and the worktree guard refuses it. The absolute path stops the rewrite.
- One git command per Bash call. The guard refuses a chained block using `&&` or `;`.
