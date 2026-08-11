# Writing Style Template

Inject the section below into the project's agent instructions file. Copy it verbatim. It has no
`{{...}}` placeholders.

The block below carries the ASD-STE100 rules only. It deliberately omits the additions this repo's
own `rules/general.md` layers on top: the personal formatting preferences (blank lines after a long
sentence, state your assumptions), and the precedence line against a named style skill. Each of
those is local to this repo. A target repo does not have that skill installed, and a rule that
points at a missing skill is a defect. Do not sync those into this template.

---

## Writing Style

Write all prose in ASD-STE100 Simplified Technical English. This is the default mode. It does not
expire during a long task.

**Applies to** — chat replies to the user, documentation, plans, summaries, prose files, commit
message BODIES, and pull-request BODIES.

**Does not apply to** — code, code comments, structured config (JSON, YAML), terse CLI output, the
commit SUBJECT line, and the pull-request TITLE. The subject line and the title keep the
conventional-commit format (imperative mood, `feat:` or `fix:` prefix, 72 characters or fewer, no
articles). The conventional-commit format and the STE full-sentence rule cannot both hold, so the
subject format wins.

**Core rules:**

- Use approved words only. One word, one meaning. One meaning, one word.
- Use the active voice. Name the agent of each action.
- Keep procedural sentences to 20 words or fewer. Keep descriptive sentences to 25 words or fewer.
- Put one instruction in one sentence.
- Use the same word for the same thing every time. Do not use synonyms for variety.
- Use simple verb tenses (present, past, future). Do not use the `-ing` form as a noun.
- Start each instruction with the verb.
- Use articles (`a`, `the`) and full sentences. Do not use telegraphic style.
- Do not use idioms, jargon, or figures of speech.
- Keep paragraphs to 6 sentences or fewer.

**Also banned in all prose** — emojis, semicolons, filler openers ("Great question", "Certainly"),
hype or marketing language, and cliches. Em-dashes stay allowed. Keep them.
