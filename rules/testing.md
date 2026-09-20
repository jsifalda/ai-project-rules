# Testing

## Coverage

- Write many tests. Cover all user scenarios with unit, integration or e2e, whichever fits.
- Prefer E2E over unit tests for user flows.
- Never remove a failing test. Remove only one no longer needed.
- Never write a test that would pass if the behavior broke. Rewrite it to assert what a caller depends on.
- Never delete a test only because it is tautological.
- Assert through the public interface, never internals. This binds thin wrappers too.
- Prefer a deep module: a small interface over a large implementation.

## TDD

- Cycle Red, Green, Refactor, Commit. One cycle per commit.
- Write a failing regression test before fixing a bug. Pure CSS and layout changes are exempt.
- Keep tests isolated, deterministic, fast, behavioral, structure-insensitive, specific, predictive.
- Fix a flaky test before anything else.

## Concurrent runs

- Run one test suite per machine. Another run in flight → wait. Never start a second.
- Cap the runner explicitly when overlap is unavoidable. Never the CPU default.
- Use Vitest `maxWorkers`, or `poolOptions.forks.maxForks` on v3 where config overrides the CLI flag.
- Use `jest --maxWorkers`, `pytest -n`, `cargo test -- --test-threads`, and `go test -parallel`. `-p` bounds packages, not one binary.
- Bound test workers, not build jobs.
- Use a machine-wide slot lock across worktrees: `flock` on Linux, `lockf -k` on macOS.
- Key the lock on `git rev-parse --path-format=absolute --git-common-dir`. Never the bare form, which is per-worktree.
- Wrap the test script. Leave watch mode unwrapped.

## Never wait real wall-clock

- Never sleep in a test. No bare `setTimeout`, no polling loop, no waiting out a production timeout.
- Fake the clock with Vitest or Jest `useFakeTimers()` plus `advanceTimersByTimeAsync`, modern timers only.
- Use Python `freezegun`, and an injected clock in Go and Rust.
- Restore with `useRealTimers()` in `afterEach`.
- Inject the timer when you cannot fake it. `AbortSignal.timeout` stays real under a fake.
- Never assert a production number by waiting for it.
- Fix the wait, never the ceiling. A raised per-test timeout is the tell.
