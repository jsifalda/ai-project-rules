# Gate changelog entries to real changes only

- Added a "When to create an entry" rule to the `changelog-setup` skill (policy template + SKILL.md) and synced the same rule into the home-folder and instructions-repo live changelog policies.
- An entry is now created only for a real change (code/config/behavior, structural/dependency) or any destructive/hard-to-reverse action — not for low-impact work like dropping a new note file or read-only research.
- Why: the old "every session creates a file" wording produced noise from trivial, no-impact sessions.
