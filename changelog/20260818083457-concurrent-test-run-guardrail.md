# Add a concurrent test run guardrail to `rules/general.md`

- Added a `### Concurrent test runs` block under `## Testing`: one test suite per machine at a
  time, and an explicit cap on the runner when an overlap cannot be avoided.
- Why: several agent sessions each ran a project test suite at once and livelocked the machine. A
  runner's parallelism cap is per process, not per machine — each run reads the core count rather
  than the remaining capacity, so N runs give N times the cap.
- The cap list names the knob that bounds test workers per runner, not the one that bounds build
  jobs, because the two differ in Go and Rust.
