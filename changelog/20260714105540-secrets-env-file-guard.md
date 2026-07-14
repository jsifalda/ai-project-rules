# Ban reading global env + credential files

- New `# SECRETS & ENV FILES` section in `rules/general.md`: global shell/env/credential files (`~/.zshenv`, `~/.ssh/*`, `~/.aws/credentials`, any `.env*`) are off-limits for read and write, and no secret value may reach the transcript from any source.
- Why: `# READING FILES` told agents to "read ALL relevant files in full", which licensed opening exactly these files. The new section overrides it explicitly.
- Why no-read rather than no-print: anything read is already in the transcript, so redacting on output is too late.
- Changing a global env file now follows the ask-first protocol — hand the user the line, they add it.
