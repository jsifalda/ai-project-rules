# Add architecture, dependency-preference, and prior-art rules to general.md

- New `# ARCHITECTURE` section: decide for the long term, durable interfaces over minimal implementations, grow the system in layers, enforce boundaries between concerns.
- `## Dependency Management` gains a preference order (existing dep → stdlib → established library → own code), a capability-check rule, and a "small enough to write? write it" default that keeps the install-nothing posture from RESTRICTIONS.
- `# PLAN MODE DEFAULT` gains a prior-art rule: start from how established products solve the problem, as a bias to challenge rather than an answer to copy.
- `Simplicity First` now spells out the no-speculative-abstraction half explicitly.

Why: these were recurring corrections given per-session. Folded into existing sections rather than appended, so nothing duplicates or contradicts what was already there.
