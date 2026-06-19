# Git Policy Template

Inject the section below into the project's agent instructions file. Copy it verbatim.

---

## Git Policy

- **NEVER commit changes without explicit user approval.** After completing changes and verifying
  they pass the verification protocol, present a summary and wait for the user to confirm before
  running `git add` / `git commit`.
- **Do not push to remote unless the user explicitly tells you to.**
- When working on the default branch, create a feature branch first rather than committing directly
  to it.
