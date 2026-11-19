# Verification protocol

Run Phases 1-3 after any code change, and Phase 4 per its own scope. The task is not complete until every phase that applies passes.
A phase fails → fix, then re-run all phases.

**Phase 1 — Build.** Run the project build. Zero compile errors. Address warnings. All types
resolve.

**Phase 2 — Tests and lint.** Suite present → run it in full: zero failures. Lint present → run it: zero errors and warnings.
Changed functionality → update its tests. New functionality → write tests.

**Phase 3 — Code review.** Run the `code-review` skill on this session's changes.

- Skip this phase for a mechanical git task (pull, conflict resolution, push, rebase) unless asked. A repo's own verification protocol still applies.
- Triage every finding first. Relevance decides the fix. Severity sets the order.
- Fix every relevant finding at any severity. Reject the rest with a stated reason: wrong about
  the code, out of scope, contradicts a convention, or taste with no defect. Never queue a
  rejection for the user.
- A relevant finding needing a broad refactor, a new dependency, or a public-interface change →
  state it with the proposed fix and ask first. A review never grows the change.
- Never apply a finding that changes what a rule requires. Draft the wording, show it, ask.
- Present what the review returned and what you did with each finding.

**Phase 4 — End to end.** Before you report any task done, run its changed behavior once, end to end, as its user would.

- Fix each defect the run finds that no ask-first rule gates. Flag the rest.
- Apply it to every task with an observable outcome: code, config, a script, a skill, a rule, a workflow.
- Read-only work is exempt.
- Pick the domain's own check: a command, the test suite, a browser, a phone simulator.
- Run only safe checks: local, sandbox, dry-run, or a read-only production probe that returns no user data and changes no state.
- Never touch real user data, send a message, write to an external service, or run a destructive, paid or other production action.
- Check a skill, rule or instruction file with a fresh agent on a sample request within these safe checks.
- Only an unsafe check exists → do not run it. Report `e2e: n/a (unsafe, <what stays unverified>)` and hand the user the exact command.
- Report one line: `e2e: <check> → <observed result>`, or `e2e: n/a (<reason>, <what stays unverified>)`.
