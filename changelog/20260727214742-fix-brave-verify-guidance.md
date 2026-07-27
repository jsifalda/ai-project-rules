# Fix brave-submit-site indexing verification guidance

- Corrected the "Verifying indexing" section in `skills/brave-submit-site/`. It claimed Brave ignores the `site:` operator and that a `site:` query proves nothing about indexing.
- That was wrong. Brave documents `site:` as supported, and a positive control confirmed it filters correctly. The "search operators were not applied" message is Brave's zero-hit fallback, which is exactly the not-indexed-yet signal you want.
- The old text pointed future runs away from the only reliable check and told them to discard a true negative as meaningless.
- Also noted that Brave's crawler sends no distinctive user agent, so server logs cannot confirm a visit, and that it skips whatever Googlebot is blocked from.
