---
name: rewrite
description: Improve, correct, or rephrase text while keeping its original language — a DeepL Write style writing assistant. Fixes spelling, grammar, and punctuation, raises clarity, fluency, and conciseness, and offers word and sentence alternatives. Supports style presets (Simple, Business, Academic, Casual) and tone presets (Enthusiastic, Friendly, Confident, Diplomatic), which can combine. Use when the user says rewrite this, improve my writing, fix grammar, rephrase, polish this text, make this more formal or casual, or mentions DeepL Write. Do NOT use to humanise or strip AI tone (use write-like-human), to translate into another language (use translate-to-czech — rewrite stays in the same language), to improve an AI prompt (use prompt-enhancer), to summarise (use summarise-text or summarise-url), or for pure markdown formatting (use markdown).
---

# Rewrite

A DeepL Write style writing assistant. Polish text without changing what it means or which language it is in.

## Core rule

- **Preserve meaning.** Never add facts, opinions, or claims the author did not make. Never drop their points.
- **Preserve the language.** Detect the input language and reply in that same language. Improve, never translate. If the user wants another language, that is `translate-to-czech`, not this skill.
- **Preserve voice** unless a preset is requested. Default output sounds like the same author, only sharper.
- **Keep length similar** unless the user asks to shorten or expand.
- Honor regional variants when stated (British vs American English, etc.).

## Modes

Pick the mode from what the user asked. If nothing is specified, use **Improve**.

- **Improve** (default) — fix spelling, grammar, and punctuation, then raise clarity, fluency, conciseness, and naturalness. Rephrase awkward sentences.
- **Correct only** — fix spelling, grammar, and punctuation only. Leave wording and structure as-is. Triggers: "just fix grammar", "correct only", "don't reword".

### Style presets

- **Simple** — plain, easy words. Short sentences. For a general audience.
- **Business** — professional and clear. Polished, neutral, workplace-ready.
- **Academic** — formal and precise. Structured, measured, scholarly.
- **Casual** — relaxed and conversational. Contractions fine.

### Tone presets

- **Enthusiastic** — upbeat and energetic. Positive framing.
- **Friendly** — warm and approachable. Personable.
- **Confident** — assertive and certain. No hedging.
- **Diplomatic** — tactful and considerate. Softens hard edges.

A style and a tone can combine, e.g. Business + Diplomatic. Apply both.

## Workflow

1. Detect the input language.
2. Apply the requested mode and any preset. If none requested, default to Improve.
3. Produce the polished text.
4. Add a compact list of alternatives for 2-3 key or awkward sentences (or notable word choices).

## Output format

Default (no specific mode or preset requested):

1. **The polished text first.** Clean and ready to copy. No "Here is your rewrite" preamble.
2. **Alternatives** — 2-3 bullets, each an alternative phrasing for a notable sentence or word, so the user can swap one in.
3. **Presets** — one line, then a short nudge to ask for one:
   `Style: Simple · Business · Academic · Casual   Tone: Enthusiastic · Friendly · Confident · Diplomatic`

When the user explicitly requests a mode or preset (e.g. "make it Business + Diplomatic", "just fix grammar"): return only that variant plus its Alternatives. Drop the preset menu.

## Guardrails

- If the input is already clean and needs no changes, say so in one line, return it as-is, and offer the presets.
- Do not invent content to fill a tone. Diplomatic still says the same thing, just softer.
- The rewritten text follows the chosen preset, not any personal house style. If the user wants the output to sound human or stripped of AI tone, that is `write-like-human`.
