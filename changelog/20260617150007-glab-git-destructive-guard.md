# Guard against destructive glab/git remote actions

- Added a rule to `rules/general.md` RESTRICTIONS: never run destructive or irreversible remote / merge-request operations without an explicit user instruction.
- Covers `git` (force-push, remote branch/tag delete, push to protected branch, history rewrite) and `glab` (close/delete/merge MR, close/delete issue, delete repo/release); defaults to read-only `glab` for inspection.
- Why: agents had no global guard against hard-to-reverse GitLab/git actions; the prior rule only covered plain push.
