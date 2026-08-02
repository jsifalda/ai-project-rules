# loop-todos plans each entry and ships it as its own PR

- Each firing now writes a plan to `plans/<todo-id>.md` before touching code, then executes that
  plan step by step. The plan ships inside the item's PR, so the reasoning and the diff get reviewed
  together. No approval gate, because a gate per item would mean the loop only advances while
  someone is at the terminal.
- Each item now ends in a pull request via the `ship-pr` skill instead of a local commit. `loop-todos`
  commits nothing itself. It hands over a dirty tree, which is what `ship-pr` expects and why
  committing first would break the step rather than prepare it.
- Why: a local commit on a shared branch left every item's work tangled in one place and required a
  human to untangle it before anything could be reviewed. One PR per entry is reviewable on arrival.
- Branches are **stacked**, item N cut from item N-1's branch, and each PR is retargeted onto the one
  below it. Independent branches off the default were tried first and abandoned: every item moves its
  entry into `## Resolved` in the same backlog file, so every PR after the first conflicted with the
  first, on a file no entry ever names and no path-based guard could see. Accepted cost is a forced
  merge order.
- Gates the host defines over a committed range now run against the working tree diffed against the
  item's base, rather than being deferred until after the PR exists. Nothing gets pushed before its
  security review has run on it.
- Pushing is authorised as consent given at invocation. A host that forbids pushing without an
  explicit instruction has had one, since typing `/loop-todos` is that instruction. Everything else
  in the host's policy still wins.
- Two rounds of adversarial review against a real 20-entry backlog shaped this. The first found the
  clean-tree abort that made the ship step's recovery path unreachable, the stale work list built
  from a checkout behind origin, and the conflict the overlap guard could not see. The second, after
  the fixes, found four more, including a firing dying between the push and the retarget leaving a PR
  that permanently displays every earlier item's diff.
- New skill dependency, `ship-pr`. Indexed in `README.md`.
