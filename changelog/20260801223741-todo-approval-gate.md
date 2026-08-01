# Gate TODO-backlog entry creation behind user approval

- The backlog policy `setup-todo-backlog` injects no longer lets an agent file entries on its own.
  An agent notices and drafts candidates mid-task, presents them as full drafts once at the
  end-of-session sweep, and writes only what the user approves. Declines are reported, never written.
- Closing an entry is unchanged. It stays evidence-gated, not approval-gated, and the two are now
  explicitly distinguished so they do not get conflated.
- Why: the backlog is the user's record of what is wrong with their project. An agent filing into it
  unasked produces a list the user never agreed to and then has to prune.
- The one exception is a **top-level** session with no interactive channel (headless run, scheduled
  job), which files autonomously and marks the entry `_Filed without approval in an unattended
  session._`. A subagent is explicitly not that exception — it returns candidates to its caller,
  because the parent holds the user channel. Without that carve-out every review subagent would have
  filed its own findings unapproved on the ordinary path.
- The matching mandatory **Backlog sweep** verification gate in `setup-aiengineering` was updated to
  say the same thing, since both statements ship into the same `AGENTS.md`.
- `setup-aiengineering` stays at **v8**. The change is forward-only by design: new setups get it,
  existing repos pick it up when someone re-runs `setup-todo-backlog`. A version bump would refresh
  the injected gate while leaving the delegated policy stale, and a self-contradicting
  agent-instructions file is worse than a uniformly outdated one. The baseline checklist's maintainer
  loop now documents that limitation instead of implying a mechanism that does not exist.
