# Angle examples — weak vs strong

Calibration for Steps 1 to 3. Each pair shows the weak version most wrap-ups settle for next to the stronger angle hiding in the same session. The pattern to internalize: the weak one is almost always a craft-process observation that is true but forgettable. The strong one teaches the reader something about the problem, or reverses an assumption they hold.

## Pair 1 — the case this skill was fixed on

Session: flipped a spend dashboard from counting only the "extra" overage to counting real gross AI usage. Employer work.

- **Weak (craft, what actually got surfaced):** "Test theater. My tests passed after a sort-key flip, but they would have passed without it because the fixture set both values equal." True, mildly interesting to engineers, forgettable to everyone else.
- **Strong (product domain, universal lesson):** "You are probably reading your AI spend wrong. If you only track the overage beyond your plan's included budget, you are blind to everything the plan absorbs. The real number is gross usage." Same session. A reader can check it on their own bill tonight.

Why the strong one wins: it is Lens B, it survives the employer-privacy filter because the lesson is universal (no org, no real numbers), and a stranger cares because they share the blind spot.

## Pair 2 — synthesis beats extraction

Session: built a tool that measures AI-tool spend, using a workflow that itself burned several model tiers and two AI code reviewers.

- **Weak (atomic):** "I used cheaper models for grunt tasks and kept the expensive one for hard reasoning." A generic, already-logged routing tip.
- **Strong (synthesized irony):** "I built a dashboard to measure AI spend with a workflow that was itself a heavy AI spend. The tool and the way I made it are the same story." Only visible if you synthesize in Step 2. Atomic extraction walks past it.

## Pair 3 — personal project, be specific

Session: shipped a new onboarding flow on your own indie app and conversion moved.

- **Weak:** "Refactored the signup form into smaller components." Craft, no one cares.
- **Strong (specific, because it is yours):** "Cut my signup from 3 screens to 1 and activation went from X percent to Y percent in a week." On your own project you name the app, the number, the result. That specificity is the post.

The repo rule: specificity like Pair 3 is allowed only when the project is yours. For employer or client work, reduce to the universal lesson, as in Pair 1.

## The resonance bar, worked

Run the three checks before an angle earns a slot.

Candidate: "A migration default silently answers two questions at once, what new rows get and what existing rows get."

- Teaches something usable? Yes. Readers write migrations and have hit this.
- Concrete reversal or surprise? Yes. "One default, two questions" is a genuine reframe.
- Would a stranger care? Yes. It is a trap they can now avoid.

Clears all three, so it is a candidate. Rank it against the others by how hard it clears, then dedup against the ledger.

Candidate: "Renamed a service file and updated its imports."

- Teaches something? No. Fails the first check and never reaches the shortlist.
