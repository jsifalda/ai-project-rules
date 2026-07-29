---
name: sync-mattpocock-skills
description: Sync a curated subset of skills from the mattpocock/skills GitHub repo into a flat skills/ folder, ready to use. Upstream nests each skill under a category dir (engineering, productivity), so the sync flattens it into a top-level skills directory named after the skill. Defaults to this repo's skills/, and --dest points it at any other skills folder instead. Use when the user wants to sync, update, or pull mattpocock skills, or sync them into another project. Given skill names, syncs exactly those; given none, it offers the previously-synced set from state/synced.txt for confirmation. Re-sync refreshes unchanged copies silently but warns and skips any locally-modified skill, or a name that collides with a native skill, until run with --force.
---

# Sync Matt Pocock Skills

Pulls named skills from [mattpocock/skills](https://github.com/mattpocock/skills) into this repo's `skills/` folder. The upstream repo nests skills under category dirs (`engineering/`, `productivity/`, `misc/`, …); this sync **flattens** them so `skills/engineering/tdd/` lands locally as `skills/tdd/` — ready for the `setup-skills-autorefresh` hook to symlink into `~/.claude/skills/`.

## When to Use

- User asks to sync, update, or pull Matt Pocock skills
- User names one or more upstream skills to bring in
- User wants to refresh already-synced skills to the latest upstream version

## Skills Synced (default set)

Used when the user names nothing (the seed in `state/synced.txt`):

| Skill | Upstream | Description |
|-------|----------|-------------|
| prototype | engineering/prototype | Build a throwaway prototype to flesh out a design |
| handoff | productivity/handoff | Compact the conversation into a handoff doc for another agent |

Any other upstream skill can be synced ad-hoc by name (e.g. `tdd`, `diagnosing-bugs`, `domain-modeling`, `to-spec`, `to-tickets`). Bare names are searched across all categories; if a name exists in more than one, qualify it as `category/name`.

## Instructions

1. **User named skills** → run them directly. From this skill's directory:
   ```bash
   bash scripts/sync.sh <name> [<name> ...]
   ```
   Or from anywhere:
   ```bash
   bash "$(dirname "$(realpath SKILL.md)")/scripts/sync.sh" <name> [<name> ...]
   ```
   This writes into **this repo's** `skills/`. Only pass `--dest` when the user names another folder to sync into — see "Syncing into another folder" below.

2. **User gave no list** → do NOT run blind. First show the previously-synced set and confirm:
   ```bash
   cat state/synced.txt
   ```
   Show that set to the user and ask whether to sync exactly it. On yes, run `bash scripts/sync.sh` (no args — it reads `state/synced.txt`). On no, ask which skills they want and pass those as args.

3. **Handle skip warnings.** A `[skipped: locally modified]` line means the local copy was edited since last sync, or the name collides with a native skill this sync never created. Surface the named files to the user and only re-run with `--force` after they confirm they want to overwrite:
   ```bash
   bash scripts/sync.sh <name> --force
   ```

4. **After a sync that created new skills** (this repo commits synced skills): for each new `skills/<name>/` dir, add a row to the `## Skills` table in `README.md`, filling its `Origin` cell with a link to `https://github.com/mattpocock/skills` (the upstream repo root), then commit per the repo changelog convention. This step is about **this** repo's catalog, so skip it on a `--dest` run and follow the target project's own conventions instead.

## Syncing into another folder (`--dest`)

By default the sync writes into this repo's `skills/`. Pass `--dest` to point it at any other skills folder, such as another project's or a bare `~/.claude/skills`:

```bash
bash scripts/sync.sh tdd handoff --dest ~/some-project/skills
```

- One destination per run. To feed two folders, run it twice.
- A missing destination is **created** (`mkdir -p`) and reported as `[created] <path>`. Watch that line — a typo'd path is a real folder, not an error.
- The resolved destination is echoed at the start and repeated in the summary. Check it before trusting a run.
- Every other flag behaves the same. `--dest=<dir>` also works.

**State is per-destination**, so two folders never share a synced-set or an overwrite baseline:

| Destination | State lives in | Tracked in git |
|---|---|---|
| default (this repo's `skills/`) | `state/synced.txt`, `state/manifest.txt` | yes |
| any `--dest` | `state/dests/<slug>/` | no, gitignored |

The slug is the first 8 chars of a sha256 of the absolute destination path. Only the hash is stored, never the path itself, so a local folder name can never leak into this public repo. A `--dest` that resolves to the default folder (e.g. `--dest .` from the repo root) uses the tracked state, not a second copy.

## How re-sync decides (overwrite safety)

The script keeps a per-file sha256 baseline in `state/manifest.txt` (or the matching file under `state/dests/<slug>/` for a `--dest` run):

- local copy unchanged since last sync → refreshed silently to latest upstream
- local copy edited (hash differs) or no baseline (native skill) → skipped with a warning, needs `--force`
- this means a legit upstream update still applies without `--force`, but your local edits are never clobbered silently

## Forked skills — renamed on purpose, NOT tracked

The script derives the local directory from the **upstream** skill name. It has no rename map, so a skill that lives here under a different name is invisible to it. Re-syncing such a skill by its upstream name creates a **second, duplicate copy** rather than refreshing the fork — and no `[skipped]` warning fires, because the two names never collide.

| Local | Upstream | Status |
|-------|----------|--------|
| `grill-me` | `productivity/grilling` | manual fork — body synced by hand, name deliberately kept |

**`grill-me` vs `grilling`.** Local `grill-me` carries the upstream `grilling` body verbatim (one question at a time, look up facts but always ask the user for decisions, don't act until shared understanding is confirmed). Only the frontmatter differs — `name: grill-me` and a description keeping the explicit `"grill me"` trigger, in place of upstream's vaguer `'grill' trigger phrases`.

The name is load-bearing, not cosmetic. `better-plan` and `prd-creator` both declare a dependency on `grill-me` by that exact name (see the `Depends on` column in `README.md`), so renaming the directory to `grilling` would silently break both. Re-check that column before touching the name — the dependent set may have grown.

Therefore:

- **Do NOT run `sync.sh grilling`.** It would create a duplicate `skills/grilling/` alongside `skills/grill-me/`, leaving two skills with near-identical descriptions competing for the same triggers.
- **To pull an upstream `grilling` update**, refresh the fork by hand: copy the new upstream body into `skills/grill-me/SKILL.md` and keep the existing frontmatter untouched.
- If upstream `grilling` starts changing often enough that hand-copying is a chore, the durable fix is a rename map in `scripts/sync.sh` (upstream `grilling` → local `grill-me`, rewriting the frontmatter `name` on copy). Not worth it for a rarely-changing skill.

## Configuration

- `state/synced.txt` — the default set offered when no skills are named. Edit to change it.
- `state/dests/<slug>/` — per-destination state for `--dest` runs. Gitignored, safe to delete (the next run rebuilds it, treating every existing file as unbaselined).
- `scripts/sync.sh` — `REPO_OWNER`, `REPO_NAME`, `BRANCH` to change the upstream source.
- Set `GITHUB_TOKEN` for higher API rate limits.
- `--force` (or `FORCE=1`) overwrites locally-modified skills.
- `--dest <dir>` (or `--dest=<dir>`) writes into another skills folder instead of this repo's.
