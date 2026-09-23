# setup-aiengineering detects pre-commit hooks

- Setup detects a tracked pre-commit hook and the verification gates it already runs.
- A covered gate drops from the injected protocol. A closing Commit gate makes a local commit with hooks on, so the hook runs it once.
- Git Policy gets a matching exception for that local commit. Push still needs approval.
- Why: each check ran twice, by hand and in the hook. That cost time and tokens.
- Skill version bumped to v15.
