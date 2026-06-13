---
name: qmd-project
description: Turn the current folder into a local on-device qmd knowledge base, a private semantic index over all its nested .md files that only this folder can query. The index DB and config are stored inside the folder (isolated from the global qmd index) while the 2.1GB embedding models stay shared globally. Sets up a folder-scoped qmd MCP server, an auto-reindex-on-session-start hook, and a folder CLAUDE.md so Claude answers questions from the index instead of reading files one by one. Use when the user says "index this folder for qmd", "make this folder a qmd project", "set up local qmd search here", "build a queryable knowledge base from these notes", or runs /qmd-project. Do NOT use to search an already-indexed folder (just query it), or to add a folder to the global qmd index.
---

# qmd-project

Bootstrap any folder of markdown into a queryable, folder-local qmd "project". After setup, questions about the folder's contents are answered from a local semantic index, not by reading files one by one.

## Isolation model (why this is safe)

qmd keeps three things in separate places:
- **Models** (2.1GB) at `~/.cache/qmd/models` -> kept global and shared, never duplicated.
- **Index DB** via `INDEX_PATH` -> written to `<folder>/.qmd/<NAME>.sqlite`.
- **Collections config** via `QMD_CONFIG_DIR` -> written to `<folder>/.qmd/config/<NAME>.yml`.

Both the DB and the config are scoped into the folder, plus a named index `<NAME>`. A bare `qmd` call from anywhere else reads the global config and DB and **cannot see this folder**. The data lives inside the folder and deletes with it.

## Steps

1. Determine the target folder. Default to `$PWD` (the folder Claude Code was opened in). If the user named a specific folder, use that.

2. Run the bundled bootstrap, passing the target folder:
   ```bash
   ~/.claude/skills/qmd-project/scripts/init.sh "$PWD"
   ```
   It is idempotent. It writes `.mcp.json`, `.claude/settings.json` (pre-approves the MCP server + an auto-reindex SessionStart hook), appends `/.qmd/` to `.gitignore`, appends a qmd section to the folder `CLAUDE.md`, then runs `qmd collection add` + `update` + `embed`. The first `embed` loads the shared models and is the slow step. Re-runs are incremental.

3. Report the result: the index name, the doc/chunk counts from the `qmd status` output the script prints.

## After bootstrap

- **Query now (same session), via CLI:**
  ```bash
  INDEX_PATH=.qmd/<NAME>.sqlite QMD_CONFIG_DIR=.qmd/config qmd --index <NAME> query "<question>"
  ```
  Always set both env vars and the `--index` flag, or qmd hits the global index instead.
- **Next Claude Code start in this folder:** the `qmd` MCP `query` tool is live (MCP servers load at startup) and the SessionStart hook keeps the index fresh automatically. Tell the user to restart Claude Code once to get the MCP tool. No restart is needed to query via the CLI.

## Maintenance

- Force a refresh after editing files: `~/.claude/skills/qmd-project/scripts/reindex.sh "$PWD"` (or the CLI env prefix above with `qmd --index <NAME> update && qmd --index <NAME> embed`).
- Remove the project: delete the folder's `.qmd/` dir and the `qmd` entries from `.mcp.json` / `.claude/settings.json`.

## Notes

- `NAME` is the sanitized folder basename (lowercase, spaces to dashes, kept to `a-z0-9._-`).
- Requires `qmd` and `jq` on PATH. Do not scope `XDG_CACHE_HOME` into the folder, that would re-download the 2.1GB models per project.
- Absolute paths are written into `.mcp.json`. If the folder will be committed to a public repo, switch them to relative (`.qmd/<NAME>.sqlite`, `.qmd/config`) to avoid leaking your home path.
