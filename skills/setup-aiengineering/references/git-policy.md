# Git Policy Template

Inject the section below into the project's agent instructions file. Copy it verbatim. It has no
`{{...}}` placeholders.

---

## Git Policy

- Commit locally when a task passes the verification protocol, or the protocol exempts it. Do not
  ask first.
- On the default branch, create a feature branch first. Never commit to the default branch.
- Stage only this task's files. Never `git add -A` or `git add .`.
- Keep hooks on. Never commit with `--no-verify`.
- Never push without an instruction from the user in chat. One instruction covers one push.
- Never force-push, even when the user asks. Give the user the command to run. This covers `-f`,
  `--force`, `--force-with-lease` and a `+` refspec.
