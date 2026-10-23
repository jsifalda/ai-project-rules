# ship-pr redacts remote URLs and checks the GitHub path

- `ship-pr` removes credentials (`user:token@`) from the remote URL in its abort messages.
- `ship-pr` rejects a GitHub origin path that is not `owner/repo`. GitLab subgroup paths stay allowed.
- Why: review findings on the origin-slug change.
