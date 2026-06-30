# Add "research before you edit" rule

- Added two bullets to `rules/general.md` `# READING FILES`: grep ALL callers/usages before modifying a function, and a general "research before you edit, never edit blind" rule.
- Why: prevent blind edits and signature changes that miss call sites. The read-before-edit part already existed; the grep-callers clause was the genuinely new gap.
- Companion emphasis pointer added to `~/.claude/CLAUDE.md` (not in this repo).
