---
name: claude-allow-home
disable-model-invocation: true
description: Mark a folder as trusted in Claude Code by setting hasTrustDialogAccepted in ~/.claude.json, skipping the interactive "Do you trust the files in this folder?" prompt — useful when provisioning a fresh server or running Claude Code non-interactively. Use when the user asks to "trust this folder in Claude Code", "skip the trust dialog/prompt", "allow my home folder", "make /root trusted", "pre-trust a directory", or invokes /claude-allow-home. Do NOT use to change tool permissions, allowlists, env vars, hooks, or any other Claude Code setting (use update-config for those) — this only flips the per-directory trust flag.
---

## What this does

Sets `projects["<path>"].hasTrustDialogAccepted: true` (and `hasCompletedProjectOnboarding: true`)
in Claude Code's global config `~/.claude.json`, so the one-time trust dialog never appears for
that path. Normally this flag is written when a human accepts the dialog on first launch — this
sets it programmatically instead.

## Prerequisite

`jq` must be installed. Check with `jq --version`; install via `apt-get install -y jq` (Debian/Ubuntu)
or `brew install jq` (macOS).

## Steps

1. **Stop Claude Code in the target path first.** It rewrites `~/.claude.json` on exit and can
   overwrite the change. The script prints a warning if a `claude` process is running.

2. Run the bundled script. It defaults to `$HOME`; pass an explicit path to trust a different folder:

   ```bash
   bash scripts/allow-home.sh            # trusts "$HOME"
   bash scripts/allow-home.sh /srv/app   # trusts an explicit path
   ```

   The script is idempotent, backs up the config to `<config>.bak`, merges without touching other
   keys, and writes atomically. Expected final line: `Trusted <path>: true`.

3. **Verify** independently if desired:

   ```bash
   jq -r --arg p "$HOME" '.projects[$p].hasTrustDialogAccepted' "$HOME/.claude.json"   # -> true
   ```

## Notes

- Config path can be overridden with `CLAUDE_CONFIG_DIR` (edits `$CLAUDE_CONFIG_DIR/.claude.json`).
- **Revoke**: `jq 'del(.projects["<path>"].hasTrustDialogAccepted)' ~/.claude.json` written back via
  a temp file, or set the flag to `false`.
- **Rollback**: restore the backup — `cp ~/.claude.json.bak ~/.claude.json`.
