# Make the setup-* delegations reachable, and let domain-modeling use the repo's ADR system

- Removed `disable-model-invocation: true` from `setup-adrs`, `setup-changelog`,
  `setup-user-scenarios`, and `setup-todo-backlog`. That flag removes a skill from the Skill tool
  completely, so `setup-aiengineering` Step 6 could never reach any of the four. All four
  delegations looked wired and were dead. They work now.
- Replaced the flag with the prompt-level guard `ship-pr` uses — an anti-trigger clause at the
  front of each `description`, plus an `## Invocation (check this first)` section that names the
  only allowed entry points.
- Deleted the natural-language trigger lists from those four skills, in both the `description`
  and the `## When to use` section. The flag made those lists inert; removing the flag would have
  made them live, so a phrase like "let's set up ADRs" would have written `docs/adr/`,
  `ARCHITECTURE.md`, and a policy block into the user's repo with no confirmation. Deleting them
  keeps the behaviour the flag gave. Every `Do NOT use for` exclusion stayed.
- Tradeoff, the same one the `ship-pr` change accepted — four skills that write into a user's
  repo are now held back by prompt text instead of by the harness. Do not re-add the flag without
  first removing every delegation step that depends on the skill.
- `domain-modeling` now uses the repo's own ADR system when there is one. `ADR-FORMAT.md` gained
  a four-step precedence rule — an existing ADR template first, then an existing `## ADRs` policy,
  then `setup-adrs` if it is available, and its own minimal format last. It searches `docs/adr/`,
  `doc/adr/`, `adr/`, and `docs/architecture/decisions/`, because `setup-adrs` reuses any of them.
- `setup-adrs` is invoked only when the repo has no ADR system, and only after the user agrees.
  It writes several files, so it must not run as a side effect of one ADR. A machine without
  `setup-adrs` still works — the minimal format is the fallback.
- README `Depends on` for `domain-modeling` is now `setup-adrs` (optional).
- `domain-modeling` drifts further from upstream. A `--force` re-sync overwrites all of it.
