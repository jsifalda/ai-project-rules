# Make end-to-end verification universal

- Added Phase 4 "End to end" to the verification protocol in `rules/general.md`: every task with an observable outcome gets one safe e2e check, or an `e2e: n/a` line that names what stays unverified.
- Removed the Tier 2-only "Runtime verification" section from `rules/review-tiers.md`, and made every tier run Phase 4.
- Updated `CLAUDE.md` and `README.md` to match, and shortened Phase 2 to keep the always-loaded layer small.
- Why: before, runtime checks ran only at Tier 2, so most changes were reported done without the real behavior being checked.
