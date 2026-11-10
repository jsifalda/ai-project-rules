---
name: brainstorm
description: Generate many distinct ideas for any problem, then shortlist the best. Use when the user says brainstorm, ideas for, ideate, what could I do about X, or explore options. Do NOT use to judge one idea (use council-v2), attack a plan (use grill-me), or plan execution (use goal-breakdown).
metadata:
  version: "1.0"
---

# Brainstorm

0. Rephrase.
   - Say in one line: "Running /rephrase to confirm what you want to brainstorm."
   - Then invoke the `rephrase` skill.
   - If the skill is not available, restate in your own words the user's goal and the problem they are trying to solve.
   - After that, restate it as one "How might we..." question.
   - Ask the user to confirm or correct. Stop and wait for the answer.
1. Diverge. Generate 5 ideas per lens below. No judging.
   - Inversion: how would we make this worse? Flip each answer.
   - Analogy: how does another industry solve this?
   - Constraint: what if we had 1 day, zero money, or 10x budget?
2. Mark the obvious ideas. Replace each with a stranger one.
3. Converge.
   - Score each idea on impact (1-5) and effort (1-5).
   - Show the top 3 with one line each: what it is, why it might work, the riskiest assumption.
4. Give one next step under 1 hour for the top idea.

## Rules

- No filtering during step 1.
- Each idea gets a name and one specific sentence.
- No technique jargon in the output.
- Explain your reasoning for the scores and the top 3.
