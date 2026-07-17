<!--
The appendix that follows the page. Skeleton only — fill and return, never show this file's
commentary to the user. Collapse it in a <details> block so the page stays the headline.
-->

<details>
<summary>Score trail — {r1_total} → {r2_total} → {final_total} / {achievable}</summary>

| # | Section | R1 | R2 | R3 | Final | Notes |
|---|---|---|---|---|---|---|
| 1 | Navbar | {n} | {n} | {n} | {n}/3 | {— / NEW / BLOCKED — needs …} |
| 2 | Hero | {n} | {n} | {n} | {n}/3 | {…} |
| 3 | Trust Logos | {n} | {n} | {n} | {n}/3 | {…} |
| 4 | Problem | {n} | {n} | {n} | {n}/3 | {…} |
| 5 | How It Works | {n} | {n} | {n} | {n}/3 | {…} |
| 6 | Features | {n} | {n} | {n} | {n}/3 | {…} |
| 7 | Benefits Recap | {n} | {n} | {n} | {n}/3 | {…} |
| 8 | Testimonials | {n} | {n} | {n} | {n}/3 | {…} |
| 9 | Vision | {n} | {n} | {n} | {n}/3 | {…} |
| 10 | About | {n} | {n} | {n} | {n}/3 | {…} |
| 11 | Pricing | {n} | {n} | {n} | {n}/3 | {…} |
| 12 | FAQ | {n} | {n} | {n} | {n}/3 | {…} |
| 13 | Final CTA | {n} | {n} | {n} | {n}/3 | {…} |
| 14 | Footer | {n} | {n} | {n} | {n}/3 | {…} |

**{final_total} / {achievable}** · stopped after round {n} because {every section in the stop test reached 3 | no section improved | round cap}.

<!--
achievable = 42 − 3×(fully blocked) − 1×(capped-only). Report against achievable, NOT 42.

A `Blockable: yes` section the user confirmed they cannot fill is NOT SCORED. Its row
reads "—", never a number, and it drops 3 from the denominator. Scoring it punishes the
user twice: once for the missing fact, again for every must-have that fact poisons — no
real quotes also fails "lead with strongest quote", "vary length", and "role matches ICP".

A `capped at 2` section IS scored, ceiling 2, and drops 1 from the denominator.

A trail reading "39/42" makes a perfect score look like a failure and punishes the user
for not having customers yet. Put the raw number in the footnote, never the headline.

Drop the R2/R3 columns if the loop stopped earlier. Never pad them.
Notes column: NEW = the section did not exist on the input page (improve mode only).
-->

**Blocked on you** — {n} sections are unscored until you supply a fact I will not invent. Biggest lift first:

1. **{Testimonials}** — {paste 3–5 real quotes with name + role}. {Placeholders are the weakest thing on this page; real quotes before Pricing is the single biggest lift available.}
2. **{Trust Logos}** — {real customer or press logos, plus the real count for the context line}.
3. **{About}** — {your founder story, what you built before, any press or community mentions}.

**Converged short** — {Section} finished at {n}/3 and is **not** blocked. {The loop could not fix it: state the failing must-have or fired anti-pattern plainly.}

**Unchanged** — {the page already scored at ceiling; nothing was rewritten. This is a valid outcome, not a failure.}

</details>

<!--
Every one of the four blocks above is conditional. Emit only what fired.
Never invent a round-over-round delta to make the trail look productive.
No P0/P1/P2 labels, no S/M/L effort estimates — the loop applies its own fixes,
so priority tiers and effort guesses are ceremony. Order by impact and say the impact.
-->
