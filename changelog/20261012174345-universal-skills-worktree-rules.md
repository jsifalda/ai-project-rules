# Add universal-skills and worktree setup rules

- Skills, shared AGENTS.md files and templates must not hardcode repo names, repo lists, project slugs or people. `create-skill` now checks this for every skill.
- A fresh worktree is set up before its first gate, commit or dev server: copy `.env*` with `cp`, then install the project's dependencies.
- The install ban now covers only installs outside a project. Restoring a project's declared dependencies is always allowed. A new package still asks first.
- Why: fresh worktrees ran gates with no `.env` or `node_modules`, and the old ban blocked even `pnpm install`.
