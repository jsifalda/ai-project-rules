# Restore op routing in better-plan, session model orchestrates

- Put the routing stage back into `better-plan` as Stage 2b. It runs by default, and `--inline`, or a plain-language form of it, skips it and executes the approved plan in the session.
- Shifted the `op` rubric. Sonnet is the default worker, Haiku takes pure chores only, Opus takes deep reasoning. The session model, Fable or Opus, orchestrates and is never a routing target.
- Reverses the removal in `f5494b1`. The opt-out flag answers the cost concern that removal cited, so the default can stay routed.
- Updated the `better-plan` and `op` rows in `README.md`.
