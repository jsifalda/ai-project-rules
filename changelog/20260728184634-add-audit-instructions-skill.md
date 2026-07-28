# Add audit-instructions skill

- New slash-only skill `audit-instructions` that audits every instruction loaded in the current session's context and reports the contradictions between them, with a reusable identification and repair guide.
- Body is the user's existing instruction-set auditor prompt, used verbatim. Verified byte-identical against the source, so re-runs stay reproducible and future edits have a clean baseline to diff from.
- Why: instruction sets grow by accretion across global rules, project rules, skill descriptions, tool definitions, and memory. Nothing checked whether they agree, so conflicts stayed invisible until two rules happened to fire on the same request. Packaging the prompt as a skill turns that check into `/audit-instructions` instead of a paste each time.
- Slash-only (`disable-model-invocation: true`) because a whole-context analysis is expensive and would misfire on loose matches like "audit this config".
- README `## Skills` table updated with the new row.
- Known issue, shipped as-is by user decision: the prompt's Constraints require verbatim quotes on both sides of every contradiction while also forbidding reproduction of system-level text. Both cannot hold for a finding involving a system rule. Left unmodified to keep the prompt exact.
