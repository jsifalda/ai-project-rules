# Archive Apple Mail skills, make brave-submit-site slash-only

- Moved `apple-mail-query` and `apple-mail-thread-export` to `archive/skills/` and moved their README rows to the Archive table. They are no longer in use, so the sync hook should not load them.
- Set `disable-model-invocation: true` on `brave-submit-site` and bumped it to 2.0, a breaking change, because natural-language requests no longer trigger it. It submits sites to an external form, so it should run only when the user types the slash command.
