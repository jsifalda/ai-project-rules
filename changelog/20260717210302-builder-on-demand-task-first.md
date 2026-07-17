# Load builder.md on demand, reframe its stack as task-first

- Rewrote `rules/builder.md`: leads with task-first stack-selection criteria (constraints, scale, runtime, team, longevity, cost) and a ruthless-challenge directive; the specific tools (pnpm, Next.js, shadcn, etc.) now sit under a "current defaults" footnote, not a mandate. Dropped the `always_apply` frontmatter so it is no longer an always-load file.
- Updated `CLAUDE.md` and `README.md` to match: `general.md` still loads on every session via First Action, `builder.md` now loads on demand only when a new-app build or stack/tooling choice is in play.
- Why: the file was force-loaded into every session and read as a required stack, nudging toward the default tools regardless of fit. Making it on-demand frees context for non-build sessions, and reframing it as defaults-you-must-justify makes the agent recommend the best fit for the actual task instead of reaching for habit.
