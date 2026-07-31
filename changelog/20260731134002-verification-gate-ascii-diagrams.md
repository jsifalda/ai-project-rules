# Add mandatory verification gate; drop Mermaid for ASCII diagrams

- Added a `## Verification Gate` to `CLAUDE.md`: before any task is reported done, run the universality scanner and skill validator, then CodeRabbit (`cr review --agent --uncommitted --include-untracked`) and the harness `code-review` agent in parallel against the dirty tree. Critical/major factual findings get auto-fixed and re-verified; minor and normative findings go to the user. Applies to markdown too, since in this repo the instructions are the product.
- Why: the repo already exports this exact protocol to other repos via `setup-aiengineering`, while governing itself with a much weaker one.
- Fixed defects in `rules/general.md`: a phase count that said three where four were listed, a reference to a nonexistent `agent-browser` skill, and two typos.
- Dropped Mermaid repo-wide in favor of inline ASCII/Unicode diagrams (`rules/general.md`, `create-codebase-docs`, `obsidian-markdown`). Why: the old Mermaid section mandated npm installs into `/tmp`, contradicting the repo's own no-install rule; ASCII renders everywhere with nothing to keep in sync.
- Recorded `obsidian-markdown` as a deliberate local divergence in `sync-obsidian-skills`, with pre-sync and re-apply steps, since that skill is synced from an upstream repo whose sync script overwrites files unconditionally.
- Fixed a stale `--type all` flag in `setup-aiengineering/references/verification-protocol.md` — the flag doesn't exist in CodeRabbit CLI v0.7.1, so every repo bootstrapped by the skill got a command that fails.
