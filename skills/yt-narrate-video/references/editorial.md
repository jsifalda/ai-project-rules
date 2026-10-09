# Editorial and design guide

## Contents
- Chapter recipe (L11)
- Lens system (L27)
- Writing rules (L35)
- Copyright and likeness rules (L46)
- Design tokens (L55)
- Self-critique checklist (L72)

## Chapter recipe

Split the transcript into chapters at topic, step or scene changes, never at fixed time intervals. Chapter count follows the scale table in `references/genres.md`. In interviews and compilations, a new question is usually a new chapter.

Each chapter, in this order:

1. **Head**: marker lamp, "N of M", a link to the start second (`https://youtu.be/<id>?t=<seconds>`, or the platform's own deep-link form).
2. **Title**: a concrete phrase from the moment ("The same pothole"), not an abstraction ("Resilience").
3. **Narration**: 2 to 4 short paragraphs. Re-tell the scene and the argument in your own words. Keep the speaker's stories concrete: numbers, places, objects, the order things happened.
4. **Illustration** (most chapters): a watercolor of an object or place from the story. Caption adds meaning, it does not describe the picture.
5. **Quote** (at most one per chapter, only for the line that names the idea).
6. **Interactive** (count from the scale table in `references/genres.md`): only where the idea has a shape, a trade-off, a break-even, a distribution, or a before/after. A chart that only restates the paragraph is decoration. Cut it.
7. **Takeaway**: one short line in the takeaway form for the genre, plus an apply line (the label from the lens table) that applies it to the reader's world. Mark the apply lines as your interpretation in the footer.

After the last chapter, the template builds a filterable deck of all takeaways automatically.

## Lens system

Every chapter carries one marker: `go`, `yield` or `stop` in `data-s`. The marker is information. It drives the lamp, the rail, the top bar and the deck filter. What the marker states mean depends on the genre. Set the names in the `LENS` object in the template, using the lens table in `references/genres.md`.

- Use every marker state. A page where every chapter is `go` has no signal.
- If the video has its own central metaphor (tides, gears, seasons), rename the states to fit it. Keep the marker colors.
- Keep the apply label (`{{APPLY_LABEL}}`) the same on every chapter.

## Writing rules

- Lead every chapter with the story, then the idea. Readers remember the lawnmower, not the lesson.
- Active voice. Short sentences, varied length. Plain verbs.
- No em-dashes, no semicolons in page copy. Use periods, commas.
- No hype words, no filler openers, no "In this chapter, we will".
- Sentence case everywhere. No all-caps labels. The hero kicker is the only label above a heading.
- Political or contested remarks: report them neutrally as the speaker's view, attributed, in one or two sentences. Do not endorse or rebut.
- Fact-check any specific factual claim the speaker makes (a date, a statistic, a definition). Search once or twice. Show the result in a `.check` box with a verdict: Confirmed, Not confirmed, or Wrong. Never present an unchecked claim as fact.
- Label every invented number. Charts carry a `.note` that says "illustrative".

## Copyright and likeness rules

- Paraphrase the transcript. Never paste long runs of it into the page.
- Quotes: under 15 words each, at most one per chapter, always attributed.
- Do not reproduce song lyrics, poems or book passages the speaker reads aloud. Describe them.
- Illustrations are original. Paint objects, places and anonymous silhouettes. Never paint an identifiable real person, a film still, a logo, album art, or a known character.
- Do not embed remote images or historical photos. Published pages block remote images, and sandbox downloads are usually blocked. Say so to the user and offer original illustrations instead.
- Credit the source video, the original shows, and any fact-check sources in the footer.

## Design tokens

The template ships these. Change the palette only if the episode's world asks for it, and keep the marker colors distinct in both themes.

| Token | Light | Dark | Role |
|---|---|---|---|
| `--paper` | `#F3F2EC` | `#14171B` | Page |
| `--ink` | `#1E2125` | `#ECE9E1` | Text |
| `--go` | `#2F7D5B` | `#4FB487` | Green signal |
| `--yield` | `#C8901A` | `#E2AE3A` | Yellow signal |
| `--stop` | `#B5332E` | `#E0655C` | Red signal |
| `--sky` | `#3E6A8A` | `#7FA9C8` | Neutral data series |

Type: Libre Caslon Display (headlines, nuggets), Source Serif 4 (body, 20px, 1.62), Libre Franklin (figures, captions, UI). Body column 680px, art 1080px, figures 820px. Left aligned.

The one memorable element is the signal rail. Keep everything else quiet.

## Self-critique checklist

Run before publishing. Screenshot with `scripts/shoot.py` and look at the images.

- Hero image and headline read at a glance on a phone.
- Every chapter has a working timestamp link.
- No figure text smaller than about 11px on a 390px screen.
- Dark mode: charts readable, no hard-coded dark text on dark paper.
- No JS errors in the screenshot run.
- Every chart with made-up numbers has a note.
- Quotes under 15 words. No paragraph that mirrors the transcript word for word.
- The page tells the episode in order, start to finish. A reader who never watches it still gets the whole argument.
