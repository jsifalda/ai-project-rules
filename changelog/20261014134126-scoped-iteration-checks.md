# Scope checks while iterating, run every gate in full before presenting

- The `setup-aiengineering` verification block now tells an agent to run only checks scoped to the changed packages, their dependents, and touched screens while iterating.
- Before presenting, every gate runs once in full. Lint, typecheck, and tests run last, after review fixes, so the full run sees the final tree.
- Review-fix re-runs now point at that rule. Baseline checklist moves to v19, skill version to 1.2.
- Why: full runs on every iteration are slow in large repos, and a full run on a tree that later changes proves nothing.
