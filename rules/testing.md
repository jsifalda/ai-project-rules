# Testing

Load before writing, changing or running tests.

## Coverage

- Write many tests. Cover all user scenarios. Unit, integration, e2e, whichever fits.
- Prefer E2E over unit tests for user flows.
- Never remove a failing test. Remove only a test that is no longer needed.
- Never write a tautological test. A test that restates the implementation, or that would
  pass even if the behavior broke, proves nothing. Rewrite it to assert what a caller depends
  on. Never delete it only for being tautological.
- Test behavior through the public interface. Assert what a module promises its callers, never
  its internals. This applies to thin wrappers too.
- Prefer a deep module: a small interface over a large implementation.

## TDD

- Cycle: Red, Green, Refactor, Commit. One cycle per commit.
- Bug → failing regression test first, then the fix.
- Exception: pure CSS and layout changes.
- Test quality, per Kent Beck: isolated, deterministic, fast, behavioral, structure-insensitive,
  specific, predictive.
- Fix flaky tests first.

## Concurrent test runs

- One test suite per machine at a time. Several sessions or worktrees open → confirm no other
  run is in flight. Wait, never start a second.
- Overlap unavoidable → cap the runner explicitly. Bound test workers, not build jobs:
  Vitest `maxWorkers` (v4+) or `poolOptions.forks.maxForks` (v3, config overrides the CLI flag) ·
  `jest --maxWorkers=2` · `pytest -n 2` · `go test -parallel 2` (`-p` bounds packages, not one
  binary) · `cargo test -- --test-threads 2`. Never the CPU-derived default.
- Several worktrees or sessions on one machine → a machine-wide slot lock, not a bigger cap.
  `flock` on Linux, `lockf -k` on macOS and BSD. Key on
  `git rev-parse --path-format=absolute --git-common-dir`, never the bare form.
  Wrap the test script itself. Leave watch mode unwrapped.

## Never wait real wall-clock

- A test never sleeps. No bare `setTimeout`, no polling loop, no waiting out a production timeout.
- Control the clock. Vitest and Jest: `useFakeTimers()` plus `advanceTimersByTimeAsync`, modern
  timers only. Python: `freezegun` or an injected clock. Go and Rust: an injected clock, never
  `time.Sleep`. Restore on teardown with `useRealTimers()` in `afterEach`.
- Cannot fake the timer → inject it. A native deadline such as `AbortSignal.timeout` stays real
  under a fake. Take the timer or its duration as a parameter.
- Never assert a production number by waiting for it.
- A raised per-test timeout such as `it(..., 30_000)` is the tell. Fix the wait, never the ceiling.
