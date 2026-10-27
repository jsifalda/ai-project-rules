# Split the ship-pr staging and commit block

- Split the Phase 3a dirty-mode block of ship-pr into two Bash calls, stage first, then commit and push.
- Claude Code 2.1.309 and later misread a heredoc on the line right after another heredoc's terminator. It asks for approval as a dangerous rm operation, and an unattended run denies it, so ship-pr stalled.
- Added a ship-pr rule against two heredocs in one Bash call.
