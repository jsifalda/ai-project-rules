# Add claude-allow-home skill

- New skill `claude-allow-home` with a single bash script (`scripts/allow-home.sh`) that marks a folder as trusted in Claude Code by setting `hasTrustDialogAccepted` in `~/.claude.json`, skipping the interactive trust dialog.
- Why: lets an agent pre-trust a directory (defaults to `$HOME`) when provisioning a fresh server or running Claude Code non-interactively, instead of needing a human to accept the dialog.
- Script is jq-based, idempotent, backs up the config, and writes atomically; defaults to `$HOME` with an optional explicit-path argument.
