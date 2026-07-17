# Sweep frameworks before allocating highlight slots

- Split `highlight-key-takeaways` Step 3 into inventory-only and Step 4 into allocate-then-apply, with a dedicated framework sweep that runs before every other tier.
- Raised the Tier 1 framework cap to 3 and dropped the requirement that a framework be explicitly named.
- Added handling for frameworks whose name and claim live in separate sentences, where the memorability test rejects both halves.
- Why: picking highlights while reading let salient stats and directives eat every slot before the note's organizing model was ever surveyed, so the spine of the note kept getting dropped.
