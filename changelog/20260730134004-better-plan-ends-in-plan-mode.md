# better-plan now runs inside plan mode

- `/better-plan` enters plan mode in its preface, keeps the plan in the harness plan file
  across all stages, and ends at the native approval gate.
- Why: the skill is slash-only, so it always started from normal mode and always fell
  through to its text approval fallback. The plan only existed as chat scrollback and
  approval was a free-text reply.
- Added ground rules so the plan-mode workflow the harness injects is treated as Stage 1
  only, and no early exit skips the grill and the routing.
- The text approval gate stays as a fallback for agents with no plan mode.
- README skills table updated to match.
