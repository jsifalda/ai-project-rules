# Keep README skills list fresh via an agent instruction

- Replaced the README `## Skills` section (stale hardcoded count of 35 + a
  curated sample) with a full table — one row per skill, all 42, name +
  one-line summary. Dropped the hardcoded number so the table is the list.
- Refreshed the Gemini CLI "Current commands" list (was missing 4 commands).
- Added a convention to `CLAUDE.md`/`AGENTS.md`: README lists are manually
  maintained, so any skill or Gemini-command add/remove/rename must update the
  matching README row/list in the same change. Reinforced the same in the
  README Contributing section.
- Why: the README skills list silently drifted because nothing instructed
  agents to maintain it and there is no generator. The instruction closes that
  gap without adding tooling.
