# Wait on a job's completion notice, never a sleep poll

- The `# BLOCKERS` wait rule in `rules/general.md` now says to wait for a needed background job on its completion notice, else wait in the foreground, never `sleep`-poll, then start that task.
- Dropped "native" before `Read` in the no-install check. The word named no real difference.
- Why: a `sleep` poll blocks the turn and wastes time when the harness already sends a completion notice. The foreground fallback keeps the rule working in tools with no notice.
