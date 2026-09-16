# Consolidate code-comment rules into one block

- Added a `## Comments` block under `# CODING STANDARDS` in `rules/general.md`: default none, the banned kinds, the closed list of allowed kinds, the existing-code rules, and the tooling-directive guard.
- Removed the `Comments:` bullet under `## Core Guidelines`, the `### Comments in tests` section, and half of one `# DOCUMENTATION` bullet. Every rule they held now lives in the new block, once.
- Why: the file loads on every session, and the comment rules were spread over three sections with gaps (no ban on diff narration, agent chatter, or echo doc blocks, and no closed list of what a comment may hold). One terse block is cheaper per session and harder to misread.
