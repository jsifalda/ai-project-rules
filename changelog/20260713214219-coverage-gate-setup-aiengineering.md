# setup-aiengineering: required test + ≥90% coverage gate

- Verification protocol now enforces overall repository coverage at or above a user-adjustable threshold (default 90%), wired to a detected coverage command per language.
- When a source repo has no test framework, the skill asks the user which runner + coverage tool to adopt, scaffolds minimal config, and defers install (new `references/test-setup.md`). Never auto-installs deps, never auto-runs coverage during setup.
- Intrinsic to the verification module, not a new menu item. Auto-N/A on config/no-source repos.
- Bumped skill baseline v1 → v2 so existing repos pick up the concern on re-run.
- Why: qualitative "new code gets tests" was the only coverage signal. A quantitative floor makes the tests gate enforceable and portable across stacks.
