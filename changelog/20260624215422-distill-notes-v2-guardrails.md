# Add fidelity guardrails to distill-notes-v2 skill

- Added three source-fidelity rules to the `distill-notes-v2` skill: use only the provided notes
  (no self-injected ideas or maxims), state every assumption, and ask the user when critical
  context is missing.
- Added a pre-flight check step, an uncertainty escalation ladder, an Assumptions output section,
  and matching self-test checks so the rules bind behavior instead of sitting as a preamble.
- Why: the lossy heuristic-distillation half of the skill is where the agent can drift into its
  own knowledge or silently resolve ambiguity. These guardrails lock the output to the source.
