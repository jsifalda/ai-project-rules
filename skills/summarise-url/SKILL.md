---
name: Summarise URL
description: Fetch link content, understand context, and return a concise, actionable summary with a reading recommendation and a 1–5 relevance score.
---

purpose
• Fetch a URL (or provided text), extract the main idea, list key takeaways, produce an actionable checklist formatted as Markdown checkboxes, and give a clear recommendation whether the user should read the content now plus a relevance score (1–5).

inputs
• url (required) — the webpage or resource URL to summarise  
• text (optional) — raw text to summarise instead of a URL  
• context (optional) — short description of the user's current project/goal/role (if omitted, consult USER.md and recent memory when available)  
• length (optional) — short | medium | long (default: short)  
• include_actionables (optional) — true|false (default: true)  
• language (optional) — default: english

output (Markdown)
1) Title / URL header  
2) Main idea — 1–2 sentence summary  
3) Key takeaways — 3–8 concise bullets  
4) Actionable checklist — markdown checkboxes (- [ ]) with atomic steps, optional owner/estimate, and a confidence tag  
5) Read recommendation — Yes/No + one-line rationale  
6) Relevance score — integer 1–5 and short explanation of the scoring factors (context match, novelty/value, credibility, urgency)  
7) Sources — list of links used and the last sentence of the fetched content (for user verification)

Quality rules
• Actionable checklist MUST use Markdown checkboxes. Each item must be atomic, actionable, and short (max 12–14 words). Example item:
  - [ ] Draft 2-sentence TL;DR for landing page (owner: you, est: 15m) — confidence: high
• Relevance scoring (1–5): compute via weighted factors
  • Context match (40%) — how closely the content maps to the provided context/USER.md  
  • Novelty/value (30%) — new actionable info vs. repetition of known facts  
  • Credibility (20%) — source authority / corroboration  
  • Urgency (10%) — time-sensitive relevance
• Read recommendation rule:
  • If relevance >= 4 → Recommend: Read now  
  • If relevance = 3 → Recommend: Skim (focus on takeaways)  
  • If relevance <= 2 → Recommend: Skip (or archive)  
  Always include a one-line rationale for the recommendation.
• If context is missing or unclear, state "context: unknown" and use conservative scoring (default 2–3) and include a clarifying question.
• Always include Sources and the page's last sentence (per USER.md web_fetch rules) so the user can verify fetch completeness.
• Keep output concise and in English. Prefer bullet lists over paragraphs.
• When fetching pages, follow USER.md rules (show last sentence and confirm completeness). For X.com links prefer jina.ai text fetch method if needed.
• Keep SKILL.md under 200 lines; move long examples to references/ if necessary.

Format example (exact output structure)
# Title or domain — URL
## Main idea
- One or two sentences.

## Key takeaways
- Short bullet 1
- Short bullet 2
- Short bullet 3

## Actionable checklist
- [ ] Do X (owner: you, est: 15m) — confidence: high
- [ ] Do Y (owner: team, est: 1d) — confidence: medium

## Read recommendation
- Read? Yes
- Relevance: 4/5 — Strong match to your [project-name] and contains practical steps you don't already have.

## Sources
- [1] https://example.com/article — Last sentence: "...final sentence of page."
- (any other sources used)

Prompt template (internal)
system: role: senior summariser + product strategist (user-psychology aware)  
user: Summarise URL: {url}  
context: {short context or omit}  
length: {short|medium|long}  
include_actionables: {true|false}

Notes for implementers
• Consult USER.md and memory files to compute context match when available (follow the required memory_search step). If you cannot access these, ask a clarifying question.  
• When fetching pages, follow USER.md rules (show last sentence and confirm completeness). For X.com links prefer jina.ai text fetch method if needed.  
• Keep SKILL.md under 200 lines; move long examples to references/ if necessary.

End
