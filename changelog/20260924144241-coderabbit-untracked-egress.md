# CodeRabbit lens lists untracked files before the run

- The setup-aiengineering CodeRabbit step now lists untracked files before the run, because `--include-untracked` uploads every one that is not gitignored. Gitignore or move anything that must not leave the machine.
- Why: a review run uploaded stray tool-state files that a gitignore entry did not cover yet.
