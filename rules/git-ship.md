# Git, commits, merge requests

## Ask first, every time

- Without an explicit chat instruction, never force-push, delete a remote branch or tag, push to a default or protected branch, or rewrite pushed history.
- Without an explicit chat instruction, never run `glab mr close`, `mr delete`, `mr merge`, `issue close`, `issue delete`, `repo delete` or `release delete`.
- Stop and state what and why to get that instruction. Never assume it.
- Default to read-only `glab`: `mr view`, `mr list`, `mr diff`, `ci view`, `issue view`. These need no approval.

## Messages

- Use conventional commits: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `perf:`, optional `(scope)`.
- Write the subject imperative, 72 characters or fewer, no articles, no trailing period, with the task ID when one exists.
- Give the PR or MR title the same format. Only subject and title are exempt from the writing-style rules.
- Write the commit body and the MR or PR body in the writing style.
- Write a body only when the reason is not obvious from the subject plus the diff.
- Keep that body to one or two bullets of why. Never a file list.
- Example: `feat(module): add payment validation logic, #ISSUE-ID`.

## Descriptions

- Use the commit body verbatim as the description of a single-commit PR or MR.
- Write that body under a `## Summary` heading so it transfers as-is.
- Add nothing else. No test plan, no checklist, unless asked.

## Worktrees (`.claude/worktrees/*`)

- Run git as `/usr/bin/git -C <worktree> ...`. A bare `git` is rewritten and the guard refuses it.
- Run one git command per Bash call. The guard refuses `&&` or `;`.
