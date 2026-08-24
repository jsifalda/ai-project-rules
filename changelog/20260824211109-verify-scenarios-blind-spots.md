# verify-user-scenarios: make the skipped rules visible

- A run passed a broken flow while skipping Select and Plan outright, driving one control
  across twenty scenarios, and reporting clean. The rules it broke were already in the file.
- Added what was genuinely missing: the environment preflight moves to Discover and scopes
  the run; the slice is ranked by risk instead of spread; workarounds are recorded with the
  interface branches they close; URLs the application itself emits are followed.
- Added a Self-audit phase and a `references/self-audit.md` checklist, and moved the proof of
  every load-bearing rule into report fields a skipped phase cannot fill.
- Why: prose gates leave no trace when skipped. An unfilled field does.
