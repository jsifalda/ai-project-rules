# setup-rtk falls back to official install script

- Step 2 now detects Homebrew first; when it is absent, runs RTK's official install script instead of asking the user to pick a channel.
- Why: the old no-Homebrew branch stalled fresh-machine setup on any box without Homebrew (most Linux). The official script is the defined fallback.
- Updated the skill description and the README row to mention both install paths.
