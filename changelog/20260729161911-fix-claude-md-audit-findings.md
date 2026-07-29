# Fix the CLAUDE.md audit findings

- Added the `## First Action` section that `CLAUDE.md` and `README.md` both already claimed existed. Neither was true: the only First Action lived in a private global file outside this repo, so a cloner got the 5-line `## Key Rules` summary and none of `rules/general.md`. Written as a plain instruction rather than an `@` import, because the repo is also read by Copilot CLI, Gemini CLI, and Cursor.
- Strengthened the install restriction. It said "never install global dependencies" while `rules/general.md` forbids installing anything anywhere, `--user` and one-offs included. An agent reading only `CLAUDE.md` would have concluded `pip install --user` was allowed.
- Dropped `changelog.md` from `.gitignore`. Git ignores only untracked files and that one is tracked, so the line did nothing but imply the frozen archive was uncommitted. Leftover from the Dec 2025 removal commit, never cleaned up after the file was re-added.
- Split the 235-word README-sync bullet and the Skills Sync paragraph into nested bullets. Both carried several separate obligations in one block. Content is unchanged, verified by word-set diff.
