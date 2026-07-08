# Add docs-alignment gate to setup-aiengineering verification protocol

- Added gate 6 "Docs & instructions alignment" to the injected verification block: before a task
  is marked done, the agent checks whether the change made project docs or agent-instruction
  files stale. Stale docs get updated as part of the change; instruction-file updates are
  drafted and applied only after asking the user.
- Why: nothing in the injected protocol forced doc updates to ride with code changes, so README,
  ARCHITECTURE.md, and AGENTS.md drifted from the implementation.
- Degraded mode (repos with no build tooling) now keeps two gates: code review + docs alignment.
