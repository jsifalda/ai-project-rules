# Keep pre-report gates always-loaded

- The always-loaded test keeps a pre-report gate (runs before every task-done report) always-loaded.
- Why: the test moved the verification protocol on-demand. George reverted it, it must always load.
