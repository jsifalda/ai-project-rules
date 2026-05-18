# Distillation Prompt (Step 3)

The exact procedure for turning the gathered transcripts into `<slug>-principles.md`. Follow it in order.

## 1. Clean attribution

For each transcript in working memory (do **not** rewrite the source files):

- Strip timestamps (`00:14:32`, `[12:05]`, etc.).
- Restore sentence punctuation where the transcript machine-broke it.
- Mark who is speaking. If the transcript already labels speakers, keep those labels. If not, infer host vs. leader from context and tag every paragraph (`HOST:` / `<NAME>:`).
- Keep the leader's words verbatim — do not rephrase. Cleaning is for readability, not editorialising.

## 2. Extract candidate ideas

Across all transcripts, list every distinct:

- **Principle** — a normative claim about how to operate ("hire for slope, not y-intercept").
- **Mental model** — a named framework or distinction ("Type 1 vs Type 2 decisions", "regret minimisation").
- **Decision-making framework** — a sequence or test the leader applies repeatedly when choosing.

For each candidate idea, note which interview(s) it came from. You will use these counts in step 3.

## 3. Apply the recurring-pattern bar

A candidate idea is promoted to a **principle** only if it appears in **≥2 interviews**. Single-interview ideas are demoted to "Context-only observations" at the end of the document — they may still be interesting, but they are not load-bearing for the persona.

If you find yourself stretching to fit a one-off remark into "two interviews", it does not qualify. Be strict.

## 4. Group by domain

Default headings (use these unless the material clearly demands otherwise):

- **Decision-making** — how they decide, what makes a decision good/bad, reversibility, speed-vs-quality tradeoffs.
- **People** — hiring, firing, growing reports, managing managers, feedback.
- **Product** — taste, prioritisation, user research, shipping, quality.
- **Strategy** — moats, focus, sequencing, market choice, time horizons.

Add an extra domain (e.g. **Communication**, **Capital allocation**) **only if ≥2 principles fit it cleanly**. Do not pad domains for symmetry.

## 5. Output structure

Use exactly this skeleton for `<slug>-principles.md`:

```markdown
# <Name> — Distilled Principles

Source material: <N> interviews
- <filename 1> (<source / host, if known>)
- <filename 2> (<source / host, if known>)
- ...

## <Domain>

### <Principle name>

<One-line gist in the leader's own framing where possible.>

**Recurring evidence:** <filename 1>, <filename 2> (+ count if more).

> "<verbatim quote 1>" — <filename 1>

> "<verbatim quote 2>" — <filename 2>

### <Next principle>
...

## Mental models

### <Model name>

<One-line definition.> Used to <when/why they reach for it>.

> "<verbatim quote>" — <filename>

## Context-only observations

Single-interview claims that are interesting but do not meet the recurring-pattern bar. Kept for completeness; not load-bearing for the persona.

- <claim> — <filename>
- <claim> — <filename>
```

## 6. Specificity rule

Do **not** supplement with material from books, articles, training data, or web research, even if you "know" what this leader believes. The persona's value comes from being grounded in *these specific transcripts*. If a principle is not in the transcripts, it does not go in the document. If the user wants broader coverage, the right move is to gather more transcripts, not to extrapolate.
