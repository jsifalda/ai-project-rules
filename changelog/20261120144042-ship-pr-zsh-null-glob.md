# Fix ship-pr Phase 1 block under zsh

- Added `setopt NULL_GLOB` as the first line of the ship-pr Phase 1 block, and raised the skill version to 2.6.
- Why: zsh stops the block when the `.gitlab/merge_request_templates/*` glob has no match. The conventions and PR template sections then do not print, and the PR text loses the repo rules.
- Other shells are not affected. They ignore the line. Tested in zsh, bash, sh, dash, ksh, Debian and Alpine.
