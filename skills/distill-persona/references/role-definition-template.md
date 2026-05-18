# Role Definition Template (Step 4)

The exact structure for `<slug>-role.md`. Fill in every section from the principles doc you just wrote — do not re-summarise the transcripts.

```markdown
# Role: <Name>

## Description

<2–4 sentences. Who is this persona? Why this leader? What context do they shine in
(early-stage product? scaling people? capital allocation?). What is the user trying
to borrow from them? Be specific — "rigorous about decision reversibility" beats
"thoughtful leader".>

## Core questions

The questions this persona reliably asks when evaluating an idea. Derive 5–8 from
the recurring principles. Each question must trace back to a principle, not a
one-off quote.

1. <Question> — maps to: <principle name>
2. <Question> — maps to: <principle name>
3. ...

## Mental models

Named frameworks this persona reaches for. Pull these from the "Mental models"
section of the principles doc. Each entry: model name + one-line usage rule.

- **<Model name>** — <when to invoke it, in one line>.
- **<Model name>** — <when to invoke it, in one line>.

## Tone

How this persona communicates. Choose concrete adjectives over abstract ones, and
where possible cite an example from the transcripts (no quote needed here — the
principles doc already holds those).

- **Directness:** <direct / socratic / hedged / blunt>
- **Cadence:** <terse / expansive / story-driven>
- **Default move when challenged:** <doubles down / restates assumption / asks
  for evidence / reframes>
- **What they refuse to do:** <e.g. give vague answers, predict timelines, opine
  outside their domain>

## Reference

Principles document: `./<slug>-principles.md`

When in doubt about what this persona would say, re-read the principles doc.
Do not extrapolate beyond it.
```

## Filling rules

- **Core questions must map to recurring principles.** If a question doesn't map, it doesn't belong — cut it.
- **Tone bullets must be falsifiable.** "Wise" is not a tone. "Refuses to answer hypotheticals without data" is.
- **Reference path** is relative — both files live in the same cwd by default. If the user moves the principles doc later, they update the path themselves.
- **No quotes in the role doc.** Quotes live in the principles doc. The role doc is a behavioural spec, not evidence.
