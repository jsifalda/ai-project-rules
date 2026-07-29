---
name: sync-anthropic-skills
description: Sync skills from the anthropics/knowledge-work-plugins GitHub repo into a flat skills/ folder. Upstream is a plugin marketplace nesting each skill under a plugin dir (marketing, engineering, finance) or a partner-built vendor dir; the sync flattens that into a top-level skill directory named after the skill. Defaults to this repo's skills/, and --dest points it at any other skills folder instead. Use when the user wants to sync, pull, update, or add Anthropic knowledge-work skills, or sync them into another project. Given skill names, syncs exactly those (qualify as plugin/name when a name lives in more than one plugin). Given none, run --list, present the catalog, let the user pick, then sync the chosen names. Re-sync refreshes unchanged copies silently but warns and skips any locally-modified skill, or a name colliding with a native skill, until run with --force.
---

# Sync Anthropic Skills

Pulls named skills from [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) into this repo's `skills/` folder.

The upstream repo is a **plugin marketplace**. Skills live at `<plugin>/skills/<name>/...` (e.g. `engineering/skills/standup/`, `finance/skills/reconciliation/`) and, for partner plugins, at `partner-built/<vendor>/skills/<name>/...` (e.g. `partner-built/apollo/skills/prospect/`). This sync **flattens** any of those into `skills/<name>/`.

## When to Use

- User asks to sync, pull, update, or add Anthropic (knowledge-work) skills
- User names one or more upstream skills to bring in
- User wants to refresh already-synced skills to the latest upstream version

## Default set (bare run)

`state/synced.txt` holds the set re-synced when the script runs with no args. It is **local-only and never committed**, so a fresh clone starts empty and a bare run errors out pointing you at `--list`. The set grows on its own as you sync.

## Instructions

Run everything from this skill's directory (`scripts/` and `state/` are resolved relative to it):

1. **User named skills** → sync them directly:
   ```bash
   bash scripts/sync.sh <name> [<name> ...]
   ```
   A bare name works when it's unique upstream. If a name exists in more than one plugin (the script tells you, and `--list` flags them), qualify it as `<plugin>/<name>`, e.g. `marketing/competitive-brief`.

2. **User gave no list** → do NOT sync blind. First show the catalog, then let the user pick:
   ```bash
   bash scripts/sync.sh --list
   ```
   Present the grouped list to the user, ask which skills to sync, then run step 1 with the chosen names. (Running with no args and no `--list` re-syncs the previously-synced set from `state/synced.txt`, if any — use that only when the user asks to refresh what they already have.)

3. **Handle skip warnings.** A `[skipped: locally modified]` line means the local copy was edited since the last sync, or the name collides with a native skill this sync never created. Surface the named files to the user and only re-run with `--force` after they confirm the overwrite:
   ```bash
   bash scripts/sync.sh <name> --force
   ```

4. **Register every NEW skill (MANDATORY).** The script ends with a `NEW SKILLS — REGISTER THESE` block. For each new `skills/<name>/` dir, add a row to the `## Skills` table in `README.md` — that table is the repo's catalog and it is maintained by hand, so skipping this leaves the skill undocumented. Rows are alphabetical; link the name as `` [`<name>`](skills/<name>/SKILL.md) ``. Fill every column:
   - **What it does** — curate a one-liner from the skill's own `description`, don't paste the whole verbose description.
   - **Depends on** — other skills in this repo that this one invokes or requires to function. Usually `—` for a synced skill.
   - **Origin** — link to `https://github.com/anthropics/knowledge-work-plugins` (the upstream repo root) for every skill this sync creates.

   Then commit per the repo changelog convention.

5. **Review the context fixes.** If the script prints `CONTEXT FIXES APPLIED`, it adapted the staged copy to this repo before writing it (see "Adapting synced skills" below). Read the diff it reports — it is auditable, not silent. Nothing to do unless a fix looks wrong.

6. **Act on lint warnings.** If the script prints `DESCRIPTION LINT WARNINGS`, fix the flagged synced `SKILL.md` by hand before relying on it:
   - `": "` (colon+space) in a `description` truncates the value in Copilot CLI — rewrite with ` — ` or a `>-` block scalar.
   - Description over 1024 chars — trim it (move detail into the body).
   A hand-edit makes the file "locally modified", so later re-syncs skip it until you pass `--force`. That is the intended trade-off.

## Syncing into another folder (`--dest`)

By default the sync writes into this repo's `skills/`. Pass `--dest` to point it at any other skills folder, such as another project's or a bare `~/.claude/skills`:

```bash
bash scripts/sync.sh design-critique --dest ~/some-project/skills
```

- One destination per run. To feed two folders, run it twice.
- A missing destination is **created** (`mkdir -p`) and reported as `[created] <path>`. Watch that line — a typo'd path is a real folder, not an error.
- The resolved destination is echoed at the start and repeated in the summary. Check it before trusting a run.
- Every other flag behaves the same. `--dest=<dir>` also works.

**State is per-destination**, so two folders never share a synced-set or an overwrite baseline. The default target uses `state/synced.txt` and `state/manifest.txt`; any `--dest` target uses its own pair under `state/dests/<slug>/`. Neither is tracked in git, the whole `state/` tree is gitignored.

The slug is the first 8 chars of a sha256 of the absolute destination path. Only the hash is stored, never the path itself, so a local folder name can never leak into this public repo. A `--dest` that resolves to the default folder (e.g. `--dest .` from the repo root) uses the default state, not a second copy.

Step 4 above (the `README.md` row) is about **this** repo's catalog, so skip it on a `--dest` run and follow the target project's own conventions instead.

## How re-sync decides (overwrite safety)

The script keeps a per-file sha256 baseline in `state/manifest.txt` (or the matching file under `state/dests/<slug>/` for a `--dest` run):

- local copy unchanged since last sync → refreshed silently to latest upstream
- local copy edited (hash differs) or no baseline (a native skill of the same name) → skipped with a warning, needs `--force`

So a legitimate upstream update still applies without `--force`, but your local edits and native skills are never clobbered silently.

**On a fresh clone there is no baseline at all**, because `state/` is gitignored. The first re-sync of a skill that is already committed here reports `[skipped: locally modified]` for every one of its files. That is expected, not a bug — the script cannot tell an untouched copy from an edited one without a baseline, so it fails safe. When you know the local copy is untouched, `--force` is the right response, and it rebuilds the baseline as it writes.

The baseline is the hash of **what the script wrote**, not of the raw upstream bytes. That is what lets the context fixes below coexist with safe re-syncing: the transform is deterministic and runs before the hash is taken, so an untouched local copy still matches its baseline on the next run.

## Adapting synced skills to this repo

Upstream is a plugin marketplace: a skill sits at `<plugin>/skills/<name>/` and freely points at plugin-level siblings and at marketplace connector placeholders. Flattening into `skills/<name>/` leaves those pointers dangling — the targets are not here. `scripts/contextualize.py` rewrites the **staged** copy before it lands, and every change is reported under `CONTEXT FIXES APPLIED`:

- **Dead relative references are removed.** Any markdown link whose target doesn't resolve inside the skill's own directory (e.g. the near-universal `[CONNECTORS.md](../../CONNECTORS.md)`) has its line dropped. This enforces the repo rule that a skill only references its own bundled files.
- **Connector placeholders are marked.** `If **~~design tool** is connected:` becomes `If **design tool (connector not wired in this repo)** is connected:`, so an unavailable capability doesn't read as a real one. Paired `~~strikethrough~~` is never touched.
- **`argument-hint:` frontmatter is stripped.** No native skill here uses it.

## Limitation — connector wiring is not synced

Upstream skills often depend on plugin-level `.mcp.json` and `CONNECTORS.md` files that sit **beside** `skills/`, not inside a skill dir. Flattening copies only the skill directory, so any MCP connector a skill assumes is left behind. The context fixes remove the dangling *pointers*, but they cannot wire up the connector itself. After syncing a skill that needs external data (search, CRM, Figma, etc.), check its upstream plugin's `CONNECTORS.md` on GitHub and wire up the equivalent MCP server yourself.

## Configuration

- `scripts/sync.sh` — `REPO_OWNER`, `REPO_NAME`, `BRANCH` to change the upstream source.
- `scripts/contextualize.py` — the context-fix rules applied to each staged skill. Add a rule here when a new upstream-ism shows up.
- `state/` — all sync state, gitignored and never committed. Machine-local by design, so it describes only what *this* checkout has synced.
  - `synced.txt` — the set re-synced when run with no args. Empty on a fresh clone, grows as you sync.
  - `manifest.txt` — the overwrite baseline for the default destination.
  - `dests/<slug>/` — the same pair per `--dest` target. Safe to delete (the next run rebuilds it, treating every existing file as unbaselined).
- Set `GITHUB_TOKEN` for higher GitHub API rate limits.
- `--force` (or `FORCE=1`) overwrites locally-modified skills; `--list` prints the catalog and exits.
- `--dest <dir>` (or `--dest=<dir>`) writes into another skills folder instead of this repo's.
