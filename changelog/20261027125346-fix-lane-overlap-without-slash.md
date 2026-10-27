# Fix lane overlap check for directories without a trailing slash

- `check_lanes.py` now reports an overlap when one lane owns a directory written without a trailing `/` and another lane owns a path under it, or the same directory with a `/`.
- Why: the validator printed `OK` for two lanes that edit the same tree, which is the merge conflict the skill exists to prevent.
