# Genres, lenses and scale

## Contents
- Pick the genre (L10)
- Lens table (L22)
- Per-genre notes (L38)
- Scale by length (L79)
- Transcript fallbacks (L90)

## Pick the genre

Decide from title, description, channel, tags and the first minutes of transcript. If two fit, pick the one the viewer came for. Mixed videos (a vlog that teaches a recipe) take the genre of the main payload.

- **Ideas**: podcast, interview, talk, keynote, motivation compilation, essay video
- **Tutorial**: how-to, coding walkthrough, recipe, DIY, fitness routine, software demo
- **Lecture**: course lesson, science or math explainer, whiteboard explainer
- **Story**: documentary, history, true crime, news report, biography, video essay with a narrative
- **Review**: product review, comparison, unboxing, buying guide
- **Performance**: music video, live set, stand-up, sports highlights
- **Journey**: vlog, travel, gaming playthrough, challenge, day-in-the-life

## Lens table

The template always has the marker states `go`, `yield` and `stop`, mapped to green, amber and red. The lens renames them so they mean something for this genre. Fill the `LENS` object and the `{{APPLY_LABEL}}` placeholder from this table.

| Genre | go | yield | stop | Apply label | Takeaway form |
|---|---|---|---|---|---|
| Ideas | Commit | Pause | Stop | At work (or the user's angle) | Maxim, 8 words or fewer |
| Tutorial | Must do | Tip | Pitfall | Try it | Instruction with the key value |
| Lecture | Core idea | Nuance | Misconception | Remember | One-line definition or law |
| Story | Turning point | Context | Contested | Why it matters | Sentence with who, when, what changed |
| Review | Strength | Trade-off | Dealbreaker | Buy if | Verdict for one kind of buyer |
| Performance | Highlight | Craft | Context | Listen for / Watch for | What to notice, at which second |
| Journey | Highlight | Detail | Watch out | Try it | Practical tip from the trip or run |

If the user names an angle ("focus on business wisdom", "for my team"), it overrides the apply label. Keep the takeaway honest to the video. If the video does not really support that angle, say so in the reply.

## Per-genre notes

**Ideas**
- Chapters follow topic changes. Interviewer questions mark boundaries.
- Interactives where an idea has a trade-off, break-even or distribution.
- Images: one object or place from each story.

**Tutorial**
- Chapters are steps, in order. Keep exact values (commands, amounts, settings, timings) in the narration, because the reader may follow along.
- Interactives: a step checklist with progress, a parameter playground (change one input, see the result), before/after toggles, a "common mistakes" quiz.
- Code: show short snippets in `<pre>` blocks. Long code goes in a collapsible `<details>`.
- Images: tools, ingredients, the workspace, the finished result.

**Lecture**
- Chapters are concepts, from foundation to frontier.
- Interactives: small simulators of the concept, sliders on a formula, a worked example with editable numbers, and the deck as end-of-page flashcards.
- Fact-check any number or historical claim. Mark simplifications.

**Story**
- Chapters follow the timeline, or the narrative order if the video uses flashbacks (say which).
- Interactives: a timeline, a scale comparison (numbers that are hard to feel), a map of points as SVG (no remote map tiles), a "what if" toggle.
- Heaviest fact-check load. Contested claims get the `stop` marker and both sides in one or two neutral sentences.
- Images: places, objects, documents, landscapes. Never a real person's likeness.

**Review**
- Chapters per tested aspect (design, performance, battery, price) plus the verdict.
- Interactives: a weighted scorer (the reader sets what matters, the score updates), a comparison table, a cost-over-time chart.
- Prices and specs change. Date them, and mark any price you did not verify.
- Images: generic stand-ins for the product category, no logos or real product renders.

**Performance**
- Never reproduce lyrics or a script. Describe structure, mood, technique.
- Chapters per section (intro, verse, drop, set piece) with timestamps.
- Interactives: an energy curve over time, a structure map, a "listen for" timeline that jumps to timestamps.
- Images: the instruments, the venue, abstract color fields for mood. No artist likeness, no album art.

**Journey**
- Chapters per stop, level or stage.
- Interactives: a route map as SVG dots, a cost or time tally, a stats-over-time chart.
- Images: places, gear, food, landscapes.

## Scale by length

| Video length | Chapters | Interactives | Illustrations |
|---|---|---|---|
| Under 3 min (Shorts) | 3 to 5 | 1 or 2 | 3 to 5 plus hero |
| 3 to 30 min | 8 to 16 | 4 to 8 | 8 to 14 plus hero |
| 30 to 90 min | 14 to 22 | 6 to 10 | 12 to 16 plus hero |
| Over 90 min | 18 to 24, grouped into parts | 8 to 10 | 14 to 18 plus hero |

For long videos, use the creator's own chapters (from the description, parsed by `scripts/yt_url.py` as in SKILL.md step 2) as parts, then split each part into chapters. Narrate the whole video. Compress, never skip.

## Transcript fallbacks

Try in order. Stop at the first that works.
1. A transcript tool in this session (for example a Supadata or YouTube transcript connector), in the video's language with timestamps.
2. The same tool with another available language or auto-generated captions.
3. Ask the user to paste the transcript (YouTube shows it under the description, "Show transcript").
4. Metadata only (title, description, creator chapters), only when the user declines to paste one. Build a lighter page and say so: the narration will be thinner than the video.

Auto-captions misspell names and jargon. Fix them from the title, description and context. If the transcript is not in the user's language, narrate in the user's language and mark quotes as translated.

Live streams and premieres may have no transcript yet. Members-only, private and age-restricted videos usually fail all tools. Say so, and go to step 3.
