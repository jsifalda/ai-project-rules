# Sharpen the latest-stable dependency rule

- Replaced the one-line "Always use the latest stable version of dependencies" rule in `rules/general.md` with a rule that says how to get the latest version, what to do when latest is not possible, and how far the rule reaches.
- The old line gave no method, so agents wrote version strings from memory or copied them from other projects. It gave no exception path, so a blocked agent either forced latest and broke the build or downgraded in silence.
