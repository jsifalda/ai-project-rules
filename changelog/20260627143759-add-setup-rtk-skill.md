# Add setup-rtk skill

- New `setup-rtk` skill to install RTK (Rust Token Killer) and wire its `rtk hook claude` PreToolUse hook into a single Claude Code profile, using RTK's own `rtk init` installer.
- Why: there was no repeatable way to bring RTK up on another machine. The skill makes the working local setup reproducible and universal (single profile, no personal paths).
- README Skills table updated with the new row.
