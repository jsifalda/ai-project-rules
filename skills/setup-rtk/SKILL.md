---
name: setup-rtk
disable-model-invocation: true
description: Install and wire up RTK (Rust Token Killer, a CLI proxy that compresses dev-command output to cut LLM token use) on the current machine for a single Claude Code profile. Installs the rtk binary if missing (Homebrew) and registers RTK's PreToolUse Bash hook in settings.json by running RTK's own installer (rtk init), so commands like git status and cat are transparently compacted. Idempotent, detects an existing hook and stops. Use when the user says "set up rtk", "install rtk", "get the token killer on this machine", "replicate my rtk setup", or runs /setup-rtk. Do NOT use for per-project rtk filters, for editing unrelated settings.json keys (permissions, env, model, other hooks), or for any dual-profile sync, this targets one profile only.
---

## What this does

Brings RTK up on a fresh machine so dev-command output is compacted before it reaches the
model. Two pieces: the `rtk` binary, and one `PreToolUse` hook (matcher `Bash`, command
`rtk hook claude`) registered in the profile's `settings.json`. Once the hook is in place,
commands are transparently rewritten (`git status` becomes `rtk git status`, `cat` becomes
`rtk read`) and you keep using normal commands.

The hard part, merging the hook into `settings.json` safely, is done by RTK's own installer
(`rtk init`). This skill orchestrates that, it does not hand-edit JSON.

Scope: a single Claude Code profile (default `~/.claude`, or `$CLAUDE_CONFIG_DIR`). No
multi-profile logic.

## Steps

1. **Check what is already there.** If RTK is installed and the hook is already wired, stop
   and report, the skill is a no-op.

   ```bash
   rtk --version 2>/dev/null && rtk init --show
   ```

   `rtk init --show` prints `settings.json: RTK hook configured` when the hook is present.
   If it is, you are done.

2. **Install the binary (only if `rtk --version` failed).** Confirm with the user before
   installing, then use the channel that fits the machine:
   - macOS or Linux with Homebrew: `brew install rtk` (RTK is in homebrew-core).
   - No Homebrew available: do not guess a channel. Point the user to the RTK docs at
     https://www.rtk-ai.app and the homebrew-core formula, and ask which install method they
     want before proceeding.

   Verify: `rtk --version` and `which rtk`.

3. **Wire the hook into the single profile.** Run RTK's installer in hook-only mode:

   ```bash
   rtk init -g --hook-only
   ```

   `-g` targets the global (user) config, `--hook-only` installs just the `settings.json`
   hook and skips the optional RTK.md and CLAUDE.md injection. RTK prompts before patching
   `settings.json`, confirm yes. For a non-interactive run add `--auto-patch` to skip the
   prompt.

   For a non-default profile directory, set `CLAUDE_CONFIG_DIR` first so RTK patches the
   right `settings.json`:

   ```bash
   CLAUDE_CONFIG_DIR="$HOME/.claude-other" rtk init -g --hook-only
   ```

4. **Verify.**

   ```bash
   rtk init --show   # expect: settings.json: RTK hook configured
   grep "rtk hook claude" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
   ```

   Then restart Claude Code. After restart, run a `git status` (output should be compacted)
   and `rtk gain` (shows token savings). Config files (`config.toml`, `filters.toml`) are
   created with stock defaults on first run, nothing to copy.

## Meta-commands (for after setup)

The hook rewrites commands automatically, so you never call `rtk` for `git`/`cat`/etc.
You do call it directly for these:
- `rtk gain` token-savings summary, `rtk gain --history` usage history.
- `rtk discover` scan for missed compaction opportunities.
- `rtk proxy <cmd>` run a command raw and unfiltered (for debugging the hook).

## Optional enhancements (off by default)

The steps above reproduce a hook-only setup, the functional core. Two optional add-ons:
- **Fuller install** `rtk init -g` (drop `--hook-only`) also writes an RTK.md and an
  `@RTK.md` import into the global CLAUDE.md, which teaches the agent the meta-commands.
  Skip unless the user wants it.
- **CLAUDE.md note** add a short note to the user's CLAUDE.md listing the meta-commands
  above, so the agent knows they exist. Keep it generic, no personal data.

## Notes

- **Idempotent.** Re-running detects the existing hook (Step 1) and stops. `rtk init` itself
  does not duplicate the hook.
- **Single profile only.** This intentionally does not handle a second profile or any
  cross-profile sync.
- **Rollback.** Remove all RTK artifacts with `rtk init -g --uninstall` (set
  `CLAUDE_CONFIG_DIR` first if you used a non-default profile).
