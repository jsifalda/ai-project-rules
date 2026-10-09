# Add yt-narrate-video skill

- Imported the `yt-narrate-video` skill, built in claude.ai, into `skills/`. It turns a YouTube link into an interactive narrated editorial web page.
- Why: the repo sync ships it to every agent, and it is versioned and reviewed like the other skills.
- Rewrote stated set counts to meet the counts rule, added a runtime-requirements line, and changed the publish step from an emoji favicon to an icon.
- Hardened the page template and scripts: escaped text at `innerHTML` sinks, made figure code run, fixed sticky-bar accessibility, the URL host check, the chapter parser and the placeholder check.
- Fixed skill instructions: script paths, the `--chapters` command, interactive and takeaway counts deferring to the genre tables, and transcript fallbacks asking for a pasted transcript before a metadata-only page.
