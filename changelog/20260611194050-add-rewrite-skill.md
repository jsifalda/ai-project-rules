# Add `rewrite` skill (DeepL Write clone)

- New `skills/rewrite/SKILL.md` — a DeepL Write style writing assistant that improves, corrects, or rephrases text in its own language.
- Modes: Improve (default) and Correct-only. Style presets: Simple, Business, Academic, Casual. Tone presets: Enthusiastic, Friendly, Confident, Diplomatic. Styles and tones combine.
- Default output mirrors DeepL: polished text first, a compact list of sentence/word alternatives, then a one-line preset menu.
- Description carries negative triggers so it does not collide with `write-like-human` (humanise), `translate-to-czech` (translate), `prompt-enhancer` (prompts), `summarise-*`, or `markdown`.
- Added a row to the README skills table.

Why: fills a gap — no existing skill does general-purpose, language-preserving text polishing with selectable style/tone presets.
