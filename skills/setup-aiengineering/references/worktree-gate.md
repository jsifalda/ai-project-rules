# Worktree Gate Template

Inject the section below into the project's agent instructions file. Copy it verbatim. It has no
`{{...}}` placeholders.

---

## Worktree Gate

- Apply this section only in a Claude Code session inside a git repo.
- Before you write a plan, check that the session runs in a worktree under `.claude/worktrees/`.
- Not in one → make the first plan step a switch into a new worktree with `EnterWorktree`.
- The plan needs uncommitted work, unpushed work or another branch → ask the user before the switch.
- After the switch, run `bash scripts/setup-worktree.sh` before the first gate, commit or dev server.
- No such script in the worktree → install the project's dependencies instead.
