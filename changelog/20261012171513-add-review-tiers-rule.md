# Add review tiers to scale review depth

- Added `rules/review-tiers.md`: classify each change as Tier 0, 1 or 2 before any gate, print one override line, then continue.
- Tier 0 runs local gates only, Tier 1 runs each lens once, Tier 2 adds the re-review round and runtime verification.
- CodeRabbit errors are skipped and reported, never retried.
- The Verification Protocol now classifies the tier first, and the README lists the new rule.
- Why: trivial changes paid the full review pipeline, and risky ones got no runtime check.
