---
name: landing-page-viral-grill
description: Audit a landing page against a fixed viral checklist, one verdict per check, then grill the gaps and plan the fixes. Scores every bullet in the checklist file in file order with verbatim quoted evidence, never inventing, merging, or skipping a check. Page-decidable checks are scored; checks about pricing model, positioning, or founder visibility are never scored from markup, they are deferred to a grill-me interview. Emits a gap report, then a remediation plan covering confirmed gaps only. Trigger phrases - "audit my landing page for virality", "run the viral checklist", "why won't this page get shared", "grill my landing page", "check this page against the viral principles". Do NOT use for conversion-rate optimization, SEO audits, accessibility review, or writing new copy. No composite score is ever computed.
---

# Landing Page Viral Grill

Audit a landing page against the checklist in [references/viral-criteria-original.md](references/viral-criteria-original.md), then drive the findings to a fix plan.

**The checklist file is the only source of criteria.** Do not supplement it, reorder it, or apply judgement it does not contain. If a consideration is not a bullet in that file, it is not part of this audit.

## Workflow

### 1. Accept the target

One of:
- pasted markdown / plain text of the page
- a local file path (read with the `Read` tool)
- a URL (delegate to the `defuddle` skill for clean markdown, do not use `WebFetch` directly)

Sanity-check it. If the input is empty, under ~150 words, or clearly not a landing page (README, blog post, docs), stop and ask. Never audit something you cannot see.

### 2. Load the checklist

Read the checklist file in full. Parse every `- ` bullet under every `## ` section into exactly one check, in file order.

Derive each check's ID from position: the section's first two letters uppercased, plus the bullet's index within that section. Pricing bullet 1 is `PR1`, Headline bullet 2 is `HE2`, Page structure bullet 3 is `PA3`. If two sections share their first two letters, append the section's file order (`PR1` vs `PR2-1`).

Hard rules:
- Every bullet becomes one check. Never merge two bullets into one.
- Never split one bullet into several checks.
- Never add a check the file does not contain.
- Never skip a check because it looks inapplicable. Classify it, do not drop it.
- Re-read the file every run. Never reuse a previous run's list.

### 3. Classify each check

Decide, from the check's own wording, whether the page can answer it:

- **page-decidable** — answerable from the target's text or markup. Headline wording, CTA count and labels, colors, `og:` tags, presence of a comparison table, testimonials, footer, whether a demo is shown.
- **deferred** — needs the founder. Anything about the business rather than the page: pricing model, subscription vs one-time, price relative to competitors, whether the product does one thing, trend timing, founder visibility, naming decisions.

Classify per run from the wording, not from a stored list, so the split follows the file if the file changes. Show the classification in the report.

### 4. Score the page-decidable checks

One verdict per check, in file order:

- `PASS` — met. Quote the evidence.
- `FAIL` — violated. Quote the evidence showing the violation.
- `UNPROVEN` — the page gives nothing to judge. State what you looked for.

Evidence rules:
- Quote verbatim from the target. Exact string, original casing.
- Name the location (headline, subhead, section 3 heading, `og:image` tag, footer).
- "The page feels generic" is not evidence. A quoted headline is.

### 5. Emit the gap report

Fill [assets/report-template.md](assets/report-template.md). Two parts:
- scored checks, in file order, never sorted by verdict
- deferred checks as interview questions under their own heading, explicitly marked not-gaps

No composite score, no percentage, no grade. Count verdicts instead.

### 6. Grill

Invoke the `grill-me` skill against the deferred checks plus every `UNPROVEN` finding. One question at a time. These are the answers the page cannot give. Do not guess them. A question the user declines stays open, it does not become a PASS or a FAIL.

### 7. Plan the fixes

Only after the grill, and only for confirmed gaps. Per fix:
- the check ID it closes
- the concrete change, showing the rewritten line where it is copy
- effort S / M / L
- expected impact

Skip any check the grill established is inapplicable to this product.

## Inputs

Required:
- `target` — pasted text, file path, or URL.

Optional:
- `checklist_path` — override the checklist. Defaults to [references/viral-criteria-original.md](references/viral-criteria-original.md). Any markdown file of `## ` sections and `- ` bullets works, so a project can audit against its own list.

## Non-negotiables

- The checklist file is the only source of criteria. Nothing added, merged, reworded, or skipped.
- Every check gets a verdict or a deferral. No sampling.
- No `FAIL` without quoted evidence. Absence of evidence is `UNPROVEN`, not `FAIL`.
- Business-level checks are never scored from markup. Deferred, always.
- No composite score. The sections are not commensurable and one number hides which axis is broken.
- Never invent testimonials, logos, metrics, or founder details. Use `[placeholder]` syntax.
- A high `UNPROVEN` count is itself the finding. It means the page gives a stranger nothing to grab.
