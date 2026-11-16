# Keep working until approved tasks are done

- Added a `# BLOCKERS` rule in `rules/general.md`: never end a turn while approved tasks remain, except on a blocker or a question the next task needs, and wait in the foreground for a background job the next task needs.
- Merged the "Pursue the goal" and "Captcha, bot wall" lines into one, so the always-loaded file stays small.
- Why: agents ended turns on status reports while approved tasks were open, and the user had to prompt them to go on.
