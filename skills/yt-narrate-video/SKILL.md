---
name: yt-narrate-video
description: Turn any YouTube link into a beautiful interactive narrated web page in an editorial New Yorker or NYT-graphics style. Works for every genre (podcasts, talks, tutorials, lectures, documentaries, reviews, music, vlogs, Shorts) and any URL form (youtu.be, watch, shorts, live, embed, with timestamps or playlists). It re-tells the whole video chapter by chapter with timestamp links, picks a genre lens for the takeaways, adds original inline SVG illustrations, interactive data-viz figures, fact-check boxes and a filterable deck of all takeaways. Use when the user shares a YouTube link and asks to narrate it, make an artifact, page or explainer from it, visualize it, or turn it into a scrollytelling piece. Do NOT use for a plain chat summary or bullet takeaways with no page, a transcript-only request, downloading or editing video, or slide decks.
metadata:
  version: "2.0"
---

# YouTube Narrate Video

Build one self-contained HTML page that narrates a YouTube video from start to finish, so a reader who never watches it still gets all of it. The quality bar is a magazine feature, not a summary.

Bundled files, at paths relative to this skill's directory (not the working directory):
- `scripts/yt_url.py`: normalizes any YouTube link (id, start second, kind, deep-link template) and parses creator chapters from a description.
- `assets/template.html`: page shell. Tokens, light and dark themes, inline SVG illustration slots with theme classes, marker rail, sticky chapter bar, chapter pattern, configurable `LENS`, auto-built takeaway deck, mobile text scaling.
- `scripts/assemble.py`: checks the finished page. Fails on an unfilled `{{...}}` token, a remote or missing image, sample art (`data-sample`), a duplicate id, or an em-dash in visible text.
- `scripts/shoot.py`: headless screenshots with a system Chrome or Chromium at 1360px and 390px, one dark-mode shot, and JS errors. Skips with a message when no browser is found.
- `references/genres.md`: genre detection, lens table, per-genre recipes, scale by length, transcript fallbacks. Read first.
- `references/editorial.md`: chapter recipe, lens rules, writing rules, copyright and likeness rules, design tokens, checklist.
- `references/illustrations.md`: inline SVG scene rules and examples.
- `references/interactives.md`: the tested figure patterns. Read the contents list, then only what you use.
- Runtime needs: Python 3 standard library, and optionally a system Chrome or Chromium for screenshots.

## Workflow

1. **Parse the link.** Run `python3 scripts/yt_url.py "<url>"`. Use the returned `id` for every deep link (`https://youtu.be/<id>?t=<seconds>`). A playlist-only or channel link has no video, so ask which video. If the link has a start time, mention it but still narrate the whole video unless the user asked for a part.

2. **Get the source.** Fetch title, channel, duration, description and a timestamped transcript, following the fallback order in `references/genres.md`. Save the description to a file and run `python3 scripts/yt_url.py "<url>" --chapters <file>` to get creator chapters.

3. **Pick genre, lens and scale.** Use `references/genres.md`. Write down the genre, one lens name per marker state (`go`, `yield`, `stop`), the apply label, and the chapter, interactive and illustration counts for this length. A user-named angle overrides the apply label. If the video does not support that angle, say so in the reply.

4. **Map the video.** Split the transcript into chapters at topic, step or scene changes. For each, record start second, a concrete title, what happens, the takeaway, a marker, one image idea, and whether it has a shape worth an interactive. List factual claims worth checking.

5. **Fact-check.** Search the most specific factual claims (one to three for Ideas, more for Story and Lecture). Record a verdict for each. These become `.check` boxes.

6. **Illustrate.** Copy `assets/template.html` to the page. Draw the hero and one scene per illustrated chapter as inline SVG in its slots, colored only through the theme classes, with repeated shapes from `rep()`. Follow `references/illustrations.md`.

7. **Write the page.** Fill every `{{PLACEHOLDER}}` in that page, including the `LENS` names and `{{APPLY_LABEL}}`. Repeat the chapter pattern per chapter. Adapt figures from `references/interactives.md`, or invent new ones with the same helpers when an idea has a shape no pattern fits. Follow `references/editorial.md`, especially paraphrase over quotation, no lyrics, and notes on invented numbers.

8. **Check and critique.** Run `python3 scripts/assemble.py page.html`, then `python3 scripts/shoot.py page.html shots/ <id> ...` with one element id per figure (no id shoots the top of the page). View the screenshots. Fix overlap, small text, dark-mode contrast and JS errors until the checklist in `references/editorial.md` passes.

9. **Deliver.** Where a tool can publish a hosted page (for example a claude.ai Artifact publish action), publish it with a fitting icon. Otherwise save it to the outputs folder and present it. The page uses no remote images and only Google Fonts.

10. **Report briefly.** Genre and lens used, what the page contains, the interactives, fact-check verdicts, what was not possible and why (for example no transcript, or no historical photos), and one or two ideas for a next pass.

## Defaults

- The whole video, in order. Compress long stretches, never skip them.
- A source that is not a video (a note, book chapters): skip step 1, use chapter labels in place of timestamps, drop `data-t` and the watch links, and make no youtu.be links.
- Quotes under 15 words, at most one per chapter. Never song lyrics.
- No photos or likenesses of real people, no logos, no remote images.
- Every chart with invented numbers says so in a note.
- Narrate in the user's language, even when the video is in another.
