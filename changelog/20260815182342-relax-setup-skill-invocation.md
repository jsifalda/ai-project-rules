# Give the four setup-* skills their descriptions back

- Restored the `description` on `setup-adrs`, `setup-changelog`, `setup-todo-backlog`, and
  `setup-user-scenarios`. Each one describes the skill again and carries its own `Use when ...`
  triggers. The `RESTRICTED-INVOCATION` preamble is gone from all four.
- Deleted the `## Invocation (check this first)` section from each of the four, and put the
  `## When to use` bullets back.
- Why — a `description` is what the agent reads before it picks a skill, so trigger text belongs
  there. The body loads only after the skill fires, so an `## Invocation` section full of triggers
  cannot affect which skill fires. The earlier change put the triggers where they cannot work.
- What the four workflows do and do not guard — they guard against clobbering. Each asks before it
  overwrites an existing file or touches an existing policy section. None asks before the first
  scaffold write. On a repo with no `docs/adr/`, no `changelog/`, and no `AGENTS.md`, `setup-adrs`
  Step 2 and `setup-changelog` Step 2 create the directory, and `setup-changelog` Step 4 creates
  `AGENTS.md`, all without a prompt. These are collision guards, not consent gates.
- Residual risk, stated plainly — a loose natural-language match can now scaffold files into a
  greenfield repo with no confirmation. The `description` triggers and `Do NOT use for` clauses are
  the only thing that holds the match, and they are prompt text. The earlier flag blocked this at
  the harness, at the cost of killing every delegation. A first-write consent gate in each workflow
  would remove the risk without either cost — it is not in this change.
- Gave each skill a `## When to use` bullet for its delegation route, so the
  `setup-aiengineering` Step 6 path and the `domain-modeling` path stay documented.
- `disable-model-invocation` stays removed from all four. That flag was the defect the previous
  entry fixed.
- Moved the reason into `create-skill`, which is where a future author will look. Its
  `disable-model-invocation` guidance no longer recommends the flag for the whole `setup-*` family,
  and it now states the rule — never set the flag on a delegation target, because it removes the
  skill from the Skill tool completely and the caller fails with `cannot be used with Skill tool`.
