# Point broad exploration at the scout agent

- `rules/general.md` now sends a broad search to `scout`, and to `Explore` where `scout` is not installed.
- Why: `op` and the delegation rules already send reads to `scout`, so two rules named different agents for the same job.
