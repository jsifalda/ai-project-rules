# Angle examples — weak vs strong, across archetypes

Calibration for Steps 1 to 3. Two things this file trains: how to lift a weak angle into a strong one, and how to keep the strong ones from all sounding the same.

The failure mode this skill keeps hitting: every angle comes out as the same shape — a contrarian reversal, *"X you thought was Y is actually Z."* Each one is fine alone. Five in a row read as a generic AI-thought-leader feed. So the examples below deliberately land in different archetypes. Match the archetype to what actually happened in the session, do not force everything into the reversal mold.

## The weak-to-strong lift

The weak version is almost always a craft-process observation that is true but forgettable. The strong one teaches the reader something about the problem, reverses an assumption they hold, or tells a story with real tension.

### Pair 1 — reversal archetype (the case this skill was fixed on)

Session: flipped a spend dashboard from counting only the "extra" overage to counting real gross AI usage. Employer work.

- **Weak (craft):** "Test theater. My tests passed after a sort-key flip, but they would have passed without it because the fixture set both values equal." True, mildly interesting to engineers, forgettable to everyone else.
- **Strong (reversal, Lens B):** "You are probably reading your AI spend wrong. If you only track the overage beyond your plan's included budget, you are blind to everything the plan absorbs. The real number is gross usage." Same session. A reader can check it on their own bill tonight.

Why it wins: it survives the employer-privacy filter because the lesson is universal (no org, no real numbers), and a stranger cares because they share the blind spot.

### Pair 2 — synthesis archetype

Session: built a tool that measures AI-tool spend, using a workflow that itself burned several model tiers and two AI code reviewers.

- **Weak (atomic):** "I used cheaper models for grunt tasks and kept the expensive one for hard reasoning." A generic, already-logged routing tip — and a banned cliché (see the novelty gate).
- **Strong (synthesized irony):** "I built a dashboard to measure AI spend with a workflow that was itself a heavy AI spend. The tool and the way I made it are the same story." Only visible if you synthesize in Step 2. Atomic extraction walks past it.

### Pair 3 — specific-story archetype (personal project, be specific)

Session: shipped a new onboarding flow on your own indie app and conversion moved.

- **Weak:** "Refactored the signup form into smaller components." Craft, no one cares.
- **Strong (story with a number):** "Cut my signup from 3 screens to 1 and activation went from X percent to Y percent in a week." On your own project you name the app, the number, the result. That specificity is the post.

The repo rule: specificity like Pair 3 is allowed only when the project is yours. For employer or client work, reduce to the universal lesson, as in Pair 1.

### Pair 4 — honest-failure archetype

Session: a concurrent agent session ran a git pull mid-task and moved uncommitted work onto main.

- **Weak (reversal, forced):** "Turns out running parallel agents on one repo is risky." A truism dressed as insight.
- **Strong (failure, told straight):** "Two Claude sessions, one repo. One of them checked out main and pulled while the other still had uncommitted work in the tree. My own pre-commit review caught it a second before it landed on main. Here is the exact guard I added." Names what broke, the near-miss, and the fix the reader can copy. Failure with a receipt beats a lesson with none.

### Pair 5 — useful-resource archetype

Session: found a no-auth way to pull a Google Doc as clean markdown.

- **Weak:** "Learned you can export Google Docs to markdown." Vague, sounds like a docs page.
- **Strong (resource, give the exact thing):** "Any Google Doc share link → clean markdown, no API, no auth: hit the `/export?format=md` endpoint on the doc id. Drops straight into a pipeline." The reader can paste it and use it in ten seconds. A resource post earns its slot by being immediately actionable, not by being a hot take.

## The novelty gate, worked

The originality check is the fourth bar, and it is where most generic angles die. Run it after the first three pass.

Candidate: "Built it, but never deployed it — you can max every 'done' axis and still have zero users because you never shipped."

- Usable? Sort of. Surprise? Mild. Stranger cares? Maybe.
- Original? **No.** This is "built ≠ shipped," the single most repeated maxim in the indie-hacker canon. Reject it — unless the session adds a twist that is genuinely new. Here the twist might be: "I had 126 passing tests, 8 ADRs, a vision doc, and an SEO plan — every proxy for done except the one that makes signal. The polish was the procrastination." That reframes the cliché into something specific and self-implicating. Without a twist that sharp, it does not ship.

The point: session-specific detail does not buy originality. A stale idea with fresh numbers is still stale. Find the twist or drop it.

## The resonance bar, worked (all four checks)

Candidate: "A migration default silently answers two questions at once, what new rows get and what existing rows get."

- Usable? Yes. Readers write migrations and have hit this.
- Surprise? Yes. "One default, two questions" is a genuine reframe.
- Stranger cares? Yes. It is a trap they can now avoid.
- Original? Yes. Not a canonical maxim, and the framing is not one you see repeated.

Clears all four, so it is a candidate. Rank it against the others by how hard it clears, then dedup against the ledger by theme.

Candidate: "Renamed a service file and updated its imports."

- Usable? No. Fails the first check and never reaches the shortlist.
