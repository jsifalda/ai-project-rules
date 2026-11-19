# ship-pr assigns GitHub PRs over REST and warns on failure

- GitHub self-assign now uses `gh api -X POST repos/<owner>/<repo>/issues/<n>/assignees` on the origin and fork paths, not `gh pr edit --add-assignee`.
- Every failed login lookup, assign or read-back prints a `WARN:` line. Phase 4 prints it. GitLab assign warns the same way.
- Why: older gh versions fail the `gh pr edit` GraphQL call on the retired Projects (classic) field. The `|| true` hid the error, so PRs stayed unassigned with no signal.
