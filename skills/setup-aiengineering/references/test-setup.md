# Test Setup (no framework detected)

When a source repo has no detectable test runner, the coverage gate in
`verification-protocol.md` has nothing to wire `{{COVERAGE_CMD}}` to. This guide walks the user
through choosing a stack, scaffolds minimal config, and hands the resulting commands back to Step
5, without installing anything or running the suite.

## When this branch fires

- The repo has source code in a detected language, but Step 2 found no test command and no test
  framework on disk.
- Skip entirely for config/IaC-only repos or repos with no source code: the whole test + coverage
  gate is N/A there, not just unwired.

## Ask the user (one prompt)

Ask which runner and coverage tool they want, offering a sensible default per detected language:

| Language | Default runner | Coverage tool |
|----------|----------------|---------------|
| JS/TS | Vitest | built-in v8 coverage (or Jest + `--coverage`) |
| Python | pytest | pytest-cov |
| Go | built-in `go test` | `-coverprofile` + a total-coverage threshold check |
| Rust | `cargo test` | `cargo llvm-cov` (or `cargo tarpaulin`) |

Also confirm the coverage threshold: default `{{COVERAGE_THRESHOLD}}` = 90, adjustable. A fresh
repo may want to start lower and ratchet up over time rather than gate on 90% from day one.

## Scaffold (confirm before writing)

- Write only the minimal, non-destructive config needed to wire the runner and its coverage
  threshold: a `vitest.config` `coverage.thresholds` block, a `[tool.pytest.ini_options]` or
  `.coveragerc` with `fail_under`, a Makefile or script target for Go, a `Cargo.toml` / CI note for
  Rust.
- Show the proposed files or diffs and confirm before writing. Never clobber existing config;
  merge into it or ask first.
- Add a co-located test placeholder only if the user wants one. Otherwise leave test authoring to
  them.

## Defer install (never run it)

- Emit the exact install command for the chosen stack as a copy-paste line for the user to run,
  for example `<pm> add -D vitest @vitest/coverage-v8` or `pip install pytest pytest-cov` or
  `cargo install cargo-llvm-cov`.
- **Never run it.** The skill emits the command; it does not execute it.
- Never run the test or coverage command either, not even to "verify" the scaffold during setup.

## Hand back

- Once the user has picked a stack, set `{{COVERAGE_CMD}}` and `{{COVERAGE_THRESHOLD}}` to the
  chosen commands and value so Step 5 can substitute them into the verification block.
- Coverage scope is the overall repository percentage, enforced through the runner's own
  fail-under mechanism, same as every other stack in `verification-protocol.md`.
- Note for the user: the gate goes live only after they install the dependencies and write tests.
  Until then it stays wired but dormant.
