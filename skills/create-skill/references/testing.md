# Testing a Skill

Structural validation (`quick_validate.py`) confirms a skill is well-formed. It does *not* confirm the skill works. Before distribution, run a behavioral eval.

## The 5-step eval loop

### 1. Write down what "success" looks like — per prompt

Each test prompt gets its own success criterion. Grade outcomes, not paths:

- Did the output compile / parse / match the schema?
- Did Claude use the right API / pattern / file?
- Did the skill trigger at all?

Don't grade on "did Claude follow my steps." Claude may reach the right outcome a different way — that's fine.

### 2. Mix 10–20 prompts across three buckets

- **Positive triggers** — prompts the skill *should* handle.
- **Negative triggers** — prompts the skill *should not* fire on (guards against description hijack).
- **Edge cases** — ambiguous phrasing, missing context, adversarial inputs.

Skipping the negative and edge buckets optimizes the skill in one direction — it starts firing on everything.

### 3. Run 3–5 trials per prompt

Claude's output is nondeterministic. A single pass/fail tells you nothing. Look at the distribution across 3–5 runs — a skill that passes 2/5 is not the same as one that passes 5/5, even if both "work."

### 4. Isolate each run

Run each trial in a clean session. Context bleeding between runs masks real failures — Claude may "remember" the right answer from an earlier prompt and appear to succeed on a prompt the skill would otherwise fail.

### 5. Fix the description first

When a skill misbehaves, the first suspect is almost always the description, not the body. Triggers are the highest-leverage piece of a skill. Check in this order:

1. Is the skill triggering when it shouldn't? → Tighten description, add negative triggers.
2. Is the skill *not* triggering when it should? → Broaden description, add specific keywords.
3. Is the skill triggering but doing the wrong thing? → *Then* look at the body.

Most "the skill doesn't work" bugs are fixed by rewriting two lines of frontmatter.
