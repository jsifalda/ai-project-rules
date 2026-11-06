# Check for cold caches before a long run

- `rules/general.md` now tells agents to check whether a long run's caches are cold in the current checkout, and to reuse a warm cache or take a cheaper path first.
- The "cannot reproduce" rule is shorter, so the always-loaded layer stays small.
- Why: an agent started a test runner in a fresh worktree whose package cache was empty. The runner cloned every dependency for more than 30 minutes and never reached a test, while a warm cache was already on the machine.
