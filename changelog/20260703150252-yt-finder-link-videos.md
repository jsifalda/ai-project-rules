# yt-video-finder always links every mentioned video

- Added a mandatory linking rule to the skill: every video named in the report (winner, runner-up, candidates, prose mentions) must carry its YouTube watch URL as a clickable link.
- Patched the report template so the winner and runner-up render as `[title](url)`; the runner-up previously had no link.
- Why: readers should be able to click through to any video the report names, not just the winner and the candidates table.
