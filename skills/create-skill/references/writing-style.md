# Writing Style

How to write skill instructions that actually change Claude's behavior.

Claude is smart. A skill's job is to tell it the non-obvious stuff — not to restate what it already knows. Longer is not better; over-stuffed skills measurably hurt performance.

## Use directives, not narration

Directives are instructions. Narration is trivia that the model reads and ignores.

- ✅ *"Always use `interactions.create()`."*
- ❌ *"The Interactions API is the recommended approach."*

- ✅ *"Do not call the v1 endpoint — it returns 410 Gone."*
- ❌ *"The v1 endpoint has been deprecated."*

If the sentence doesn't tell Claude what to *do*, cut it or rewrite it.

## Lead with a code example

A 5-line snippet beats a 5-paragraph explanation. Put the canonical example first, then add the surrounding prose only if the example doesn't stand on its own.

## Explain the why when the rule matters

A bare rule gets memorized. A rule with reasoning generalizes to edge cases.

- ❌ *"Use model X."*
- ✅ *"Use model X. Model Y is deprecated and returns errors."*

The *why* lets Claude make the right call in situations you didn't anticipate.

## Don't overfit

If you only test with three prompts, you'll write a skill that passes those three prompts and fails on everything else. "Fiddly" fixes — adding a clause for one specific phrasing, special-casing a filename — usually mean the skill is over-tuned.

Write for the millions of ways Claude might invoke the skill, not the handful you happened to try.
