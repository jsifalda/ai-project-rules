# Add qmd-project skill (folder-local qmd index + shipped qmd-ask)

- New `qmd-project` skill: bootstraps any folder into a folder-local qmd semantic index over all nested `.md` files. Scopes `INDEX_PATH` + `QMD_CONFIG_DIR` into `<folder>/.qmd/` and uses a named index, so the index is fully isolated from the global qmd index while the embedding models stay shared globally (no per-project 2.1GB duplication).
- Writes per-folder `.mcp.json` (scoped qmd MCP server), `.claude/settings.json` (pre-approved server + auto-reindex SessionStart hook), `.gitignore`, and a folder `CLAUDE.md`.
- Ships a project-local `qmd-ask` skill into `<folder>/.claude/skills/qmd-ask/` (baked with the index name) that answers questions from the embeddings: retrieve -> read-full-if-thin -> answer grounded in the files with source-path citations. Includes a scoped `ask.sh` wrapper that resolves the project root from any subdir.
- Why: turn folders of notes/docs into queryable local "projects" without polluting or being visible to the global qmd index.
