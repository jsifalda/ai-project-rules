# Fix ship-pr GitLab self-assign silent failure

- ship-pr now self-assigns GitLab MRs in a dedicated post-create `glab mr update --assignee` step, then reads back and reports the assignee.
- Why: `glab mr create --assignee` is a known silent no-op (glab issues #974/#878/#358) — it returns `ok created` with an empty assignee, so MRs shipped unassigned and had to be fixed manually. The verify-and-report step surfaces a failed assign instead of hiding it.
- GitHub path unchanged (its `--assignee @me` is reliable); added the same `assignee:` report line for parity.
