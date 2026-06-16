# rewrite Improve mode now loads write-like-human first

- `rewrite` skill: in Improve mode (the default) it now loads the `write-like-human` ruleset before changing any text and keeps it active while rewriting.
- Reversed the old guardrail that pushed humanising to a separate skill — default polish now reads human (no AI-tells, hype, em-dashes, semicolons) by default.
- Carve-outs unchanged: Correct-only and any explicit style/tone preset skip the human-writing pass, so formal/Academic output is unaffected.
- Why: default rewriting should produce human-sounding prose, not preset-neutral DeepL output.
