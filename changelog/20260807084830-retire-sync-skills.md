# Retire the three sync-* skills, keep their scripts as manual tools

- Deleted `skills/sync-anthropic-skills/`, `skills/sync-mattpocock-skills/`, and
  `skills/sync-obsidian-skills/`. An audit found all three syncs were already fully
  deterministic bash, so the skill wrapper only added natural-language triggering and
  prose reminders on top of a script that needed no agent in the loop.
- Kept the scripts, moved to `scripts/sync-<upstream>-skills.sh` (plus
  `scripts/sync-anthropic-contextualize.py`), to be run by hand. Sync state moved to the
  gitignored `scripts/.sync-state/<upstream>/`.
- Closed the gaps the deleted prose had been covering: `--help` on all three, `--list` on
  the mattpocock script, a `NEW SKILLS` registration reminder on mattpocock and obsidian,
  and a loud overwrite warning on obsidian, which alone has no baseline and no `--force`
  gate.
- Hard-refused the names `grilling` and `grill-me` in the mattpocock script, exit 2, not
  bypassable by `--force`. Local `skills/grill-me/` is a deliberate fork. Syncing
  `grilling` would add a duplicate directory, and upstream's own `grill-me` is now a stub
  that would replace the working fork with a skill that does nothing here. `better-plan`
  and `prd-creator` both depend on that name.
- Fixed a pre-existing bug in all three scripts: `-f` on the tree request made curl exit
  non-zero, so the `|| echo "000"` fallback turned a 403 into `403000` and the rate-limit
  hint could never print. The tree request now uses a separate `API_OPTS` without `-f`,
  while file downloads keep it.
- Documented every script in `README.md` under a new `## Upstream skill sync` section, and
  dropped the three rows from the `## Skills` table.
