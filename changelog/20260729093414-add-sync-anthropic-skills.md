# Add sync-anthropic-skills, conformed to repo standards

- Added the `sync-anthropic-skills` skill, which pulls skills from `anthropics/knowledge-work-plugins` and flattens its plugin marketplace layout into the flat `skills/` folder.
- The skill arrived from another repo and described that repo's layout throughout. Retargeted its prose, script comments, and its post-sync "register this skill" banner at this repo: the flat `skills/` folder and the real four-column `## Skills` table in `README.md`.
- Registered the skill in that table so the catalog stays accurate.

Why: a sync tool whose own instructions point at a table that does not exist here would send every future synced skill to the wrong place, or nowhere.
