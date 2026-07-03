---
name: yt-video-finder
description: >-
  Drives a real Chrome browser through Playwright to search YouTube, gather candidate videos, categorize and rate them, read their comments, then synthesize a report that names the single best video for the user's criteria. Use when the user says find the best youtube video about X, search youtube for a video on X, pick the best youtube video for X, which youtube video should I watch on X, or otherwise wants one recommended YouTube video chosen against stated criteria such as topic, purpose, upload recency, length, language, or channel. Do NOT use to download videos, do NOT use the YouTube Data API (this skill drives a real browser via Playwright, not the API), and do NOT use for non-YouTube video sites like Vimeo or TikTok.
---

# YouTube Video Finder

Search YouTube through a real browser, shortlist the strongest candidates for the user's criteria, inspect their engagement signals and comments, then pick the single best video and write it up. The goal is one confident recommendation backed by evidence, not a raw list of links.

## Tools

This skill drives the Playwright MCP browser. The tools you will lean on are `mcp__playwright__browser_navigate`, `mcp__playwright__browser_snapshot`, `mcp__playwright__browser_evaluate`, `mcp__playwright__browser_click`, `mcp__playwright__browser_type`, `mcp__playwright__browser_press_key`, `mcp__playwright__browser_wait_for`, `mcp__playwright__browser_take_screenshot`, and `mcp__playwright__browser_tabs`.

Prefer `browser_evaluate` to run JavaScript in the page and pull structured data reliably. Fall back to `browser_snapshot` to read the accessibility tree when JS extraction comes up short. Take one browser action at a time and wait for each load before the next step.

## Phase 1 - Input gate

Criteria come from the skill arguments. Parse them for:

- topic (required)
- purpose or intent (what the user wants the video for)
- upload recency window
- max length
- language
- channel preferences or exclusions

If no criteria were passed at all, stop and ask the user for them before doing anything else. Ask for at least the topic and the purpose. Do not guess criteria, and do not open the browser until you have them.

## Phase 2 - Search

- Session. Prefer the existing logged-in browser session if the Playwright context already has one. A signed-in session is better because it is ungated and carries personalized signals. Degrade gracefully. If the session is logged out, proceed anonymously.
- Navigate to a YouTube search URL of the form `https://www.youtube.com/results?search_query=<url-encoded query>`. You can append YouTube filter tokens through the `&sp=` parameter (upload date, duration, sort by relevance or view count), or apply filters through the Filters UI by clicking.
- On first navigation you may hit a cookie-consent wall or a "before you continue to YouTube" interstitial. Detect it in the snapshot and dismiss it (accept or reject) before continuing.
- Use `browser_evaluate` to pull a structured list from the results. Prefer reading `window.ytInitialData` when it is available, and fall back to reading the visible result nodes when it is not. For each candidate capture the title, channel name, view count, upload date, duration, and the canonical watch URL.
- Depth default. Collect the top 12 to 15 candidates. Override this when the criteria call for a different depth.

## Phase 3 - Categorize

- Tag each candidate by content type (tutorial, review, talk, vlog, news, and so on) and by how well it maps to the topic plus purpose.
- Drop candidates that clearly miss the criteria or break a hard constraint (wrong language, far over the max length, outside the recency window). Note why you dropped each one.
- Narrow to a shortlist of 3 to 5 candidates to deep-dive.

## Phase 4 - Rate

- Open each shortlisted watch URL. Use `browser_evaluate`, preferring `window.ytInitialData` and `ytInitialPlayerResponse`, to capture the visible engagement signals. Grab view count, like count, the like-to-view ratio, the exact upload date, and channel authority (subscriber count and track record).
- YouTube hides public dislike counts, so rate on the visible signals only. Do not try to infer a dislike number.

## Phase 5 - Comments

- On each shortlisted video, comments load lazily on scroll. Scroll the page (for example `browser_evaluate` with `window.scrollTo`, or press End) and `browser_wait_for` the comment section to populate, then extract the top 10 to 20 comments (text plus like counts) with `browser_evaluate`.
- Analyze the ratio of praise to complaints, whether commenters confirm the video delivers on its title, recurring specific praise against recurring specific complaints, and whether comments are disabled.

## Phase 6 - Synthesize

- Load `references/scoring-rubric.md`. Score every shortlisted candidate on its four weighted dimensions, apply the hard-constraint disqualification rule, rank the candidates, and pick one winner.
- Produce the report using the template in that reference file. Fill every applicable placeholder.
- Output. Always print the report in the chat. Also save it as a markdown file when the current working directory sits inside a repo that has an `outputs/` directory, writing to `outputs/youtube-pick-<short-topic-slug>-<YYYY-MM-DD>.md`. If there is no `outputs/` directory, print to chat only and say that it was not saved.

## Notes and robustness

- YouTube's DOM shifts over time, so prefer `ytInitialData` extraction with a visible-DOM fallback rather than hard-coding selectors.
- Act one step at a time and wait for each load before moving on.
- If a consent wall or a login wall blocks a step, handle it and then retry the step.
- If an extraction returns nothing, fall back to `browser_snapshot` and read the accessibility tree instead.
