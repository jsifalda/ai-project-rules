# Stop resending calls that fail hard

- Added a rule to `rules/general.md`: after a credits, quota or auth failure, never resend the call until the user fixes the cause. Switch tool or report.
- A denied call gets its own remedy: report it, and never get the denied effect through another call or tool.
- Merged the two install-ban lines in `RESTRICTIONS` into one, with the same scope, to keep the always-loaded layer small.
- Why: agents resent the same failing call again and again, and a denial must never be routed around.
