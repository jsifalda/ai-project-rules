# Remove the break-into-tasks skill

- Deleted `skills/break-into-tasks/` and its row in the README `## Skills` table.
- The skill is retired. The user wants to work without it for now and decide later if it comes back. Git history is the safety net.
- Left the sync-hook blacklists untouched, in `skills/setup-skills-autorefresh/scripts/sync-skills.js` and its Copilot counterpart. Both hooks already prune a managed copy when its source folder is gone. Deleting the source is enough to clear it from `~/.claude/skills/` and `~/.copilot/skills/` on the next session start.
- No other file in the repo depended on this skill.
- The natural-language triggers are now orphaned. `goal-breakdown` has `disable-model-invocation: true`, set when this skill arrived so the two did not race for the same phrases. Phrases like "break this down" and "this is too big" no longer start any skill. The flag stays on. This is deliberate. Fewer skills now start on their own. Use `/goal-breakdown` for that job.
- To undo: `git revert` the commit, or restore just the folder with `git checkout <commit>^ -- skills/break-into-tasks/`.
