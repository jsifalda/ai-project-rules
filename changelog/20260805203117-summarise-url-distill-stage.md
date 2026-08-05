# summarise-url now distills as well as summarises

- One link now returns two things instead of one. A summary of what the piece says, and a distilled maxim set for what actually transfers.
- Distillation reads the fetched page, not the summary, so it can keep an idea the summary chose to drop. Running it off the summary would only compress what already survived.
- `distill-notes` normally asks two questions (target bullet count, save to file). Both are suppressed here so the skill stays one link in, one reply out. `distill-notes` itself is unchanged.
- Fetching moved to the `defuddle` skill. It was the last URL-consuming skill in the repo that named no fetch mechanism, so it burned tokens on nav and page furniture that the others already strip.
- Fetched content is now explicitly marked untrusted, because step 3 feeds a web page into a second skill's control flow.
- The `description` frontmatter had no trigger phrases and no anti-triggers, so routing between this skill and `summarise-text` only worked in one direction. Rewrote it and added the missing return pointer.
