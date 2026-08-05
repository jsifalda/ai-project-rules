# Port the i-have-adhd skill from upstream

- Added `skills/i-have-adhd/` — an output-style skill that reshapes every response for an ADHD reader: action first, numbered steps, restated state, concrete time estimates, no preamble or closers. Manual-invoke only (`/i-have-adhd`), off with "stop adhd mode".
- Copied verbatim from `ayghri/i-have-adhd` (MIT). One deliberate change: the frontmatter `description` colon became an em-dash, because this repo bans `": "` there. The body is byte-identical to upstream.
- Skipped the upstream plugin wrapper — the always-on SessionStart hook, the Gemini and OpenAI adapters. The skill's own Persistence section already keeps the rules alive for a whole session, so nothing outside the skill folder was needed.
- Added the README skills-table row with `ayghri/i-have-adhd` as Origin.
