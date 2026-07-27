# User-scenarios sync becomes a mandatory verification gate (setup-aiengineering v7)

- Added a blocking user-scenarios gate to the injected verification protocol. A user-visible change left with a stale scenario doc now fails verification the same way a failing test does, and is reported every time rather than skipped silently.
- Bumped the baseline checklist to v7 and added the matching row, so re-running the skill on an older repo offers the gate instead of the gap being rediscovered per project.
- Why: the skill delegated the scenario doc to `setup-user-scenarios` but never wired it into the gate list, so every bootstrapped repo could ship user-visible work with the doc out of date and still pass.
- The gate is a tail gate alongside the backlog sweep — both are held back in Step 5 and appended in Step 6b only after their own delegation actually ran, so neither can point at a doc that was never installed.
