# Docs gate states how to find stale docs

- setup-aiengineering's docs gate now requires a grep for removed or renamed names, a re-check of every edited paragraph, and current-state-only docs.
- A stale migration note survived a docs pass because the gate never said how to check. Existing repos get the fix on re-run.
