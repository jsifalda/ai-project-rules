# Add lean worker and scout subagents

- Add `agents/worker.md` and `agents/scout.md`, custom subagents with a small tool list.
- Sync hook now links `agents/*.md` into each config folder, so every seat gets them.
- `op` routes edit tasks to `worker` and read tasks to `scout` when they exist, else falls back to `general-purpose` and `Explore`.
- Why: a probe showed general-purpose starts at about 67k tokens and Explore at 43k. The lean agents start at about 16k on the same model and still load CLAUDE.md.
