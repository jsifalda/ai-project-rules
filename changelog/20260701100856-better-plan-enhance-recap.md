# Better-plan: add enhance preface and run recap

- Added a Preface to `/better-plan` that runs the raw request through the `prompt-enhancer` skill, then plans against the sharpened version.
- Added a closing Recap that shows the original vs enhanced prompt and a per-stage trace of the run.
- Updated the skill description and README row (added `prompt-enhancer` dependency).
- Why: a vague request produced a vaguer plan, and it wasn't obvious afterward what the run did or which prompt drove it.
