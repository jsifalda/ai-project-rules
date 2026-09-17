# ship-pr ships an already-committed branch

- `ship-pr` gains a second entry state. A clean tree on a branch that is ahead of the default
  branch now pushes and opens the PR instead of aborting with `no changes to commit`. The PR
  title and body come from the branch's own commits. A clean tree with nothing ahead, or on
  the default branch, still aborts, and that abort now fires before any remote check.
- Any repo whose rules require a commit before the ship could never use the skill. This repo's
  changelog autocommit rule is one such case, and the previous session hit it.
- The committed path scans the branch's added and changed paths with the same secret patterns
  and size cap the dirty path applies to staged files, so nothing leaves the machine that the
  dirty path would have refused.
- The stale statements about the clean-tree abort in `better-plan`, `loop-todos`, and the
  README row were updated to match.
