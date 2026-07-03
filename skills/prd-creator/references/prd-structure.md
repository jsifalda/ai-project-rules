# PRD Structure

Keep it lean — this PRD is for planning your own indie side-hustle features, not corporate sign-off. Target ~1 page. Link details out (a mockup, a doc) instead of inlining them. Skip any section that doesn't earn its place for a small feature.

The generated PRD should include these sections:

1.  **Summary**: 2-3 sentences — what you're building, for whom, and why it's worth doing.
2.  **Problem & Context**:
    - The user problem or opportunity in plain language (avoid solution talk).
    - Why it matters — to the user, and why it's worth your time.
    - How people solve this today, if at all.
3.  **Users & Key Use Cases**:
    - Who this is for (be specific, not "everyone").
    - 3-7 user stories: "As a [user], I want [action] so that [benefit]."
4.  **Goals & Success Signals**:
    - Goal statement: what "good" looks like after shipping.
    - Optional: 1-2 signals you'll actually watch (e.g. signups, first paying user, activation). No baseline required.
5.  **Scope (In / Out)**:
    - **In scope**: what this version delivers.
    - **Out of scope / Non-Goals**: what you're explicitly not doing yet.
6.  **Solution Outline & Requirements**:
    - High-level approach: 1-3 short paragraphs on the core idea and how it solves the problem. No pixel-level design.
    - **Functional Requirements**: a numbered list of specific behaviors. Use "The system must..." or "The user must be able to..." phrasing. Explicit enough to build from.
    - Key behaviors & edge cases: limits, failure modes, invalid input.
    - Design references: link a mockup if you have one. Do not inline pixel specs.
    - Technical notes: key external services or APIs you rely on (e.g. auth, payments), plus any real constraint.
7.  **Risks & Assumptions**:
    - Assumptions: what you're assuming is true (people want this, they'll pay, an API does X).
    - Risks: what could sink it (no demand, you won't finish, a key dependency breaks). Optionally flag the scary one.
8.  **Open Questions**: unresolved decisions. Keep this updated as you learn — the PRD is a living document.

## Format
- Use Markdown headers (#, ##).
- Use bulleted and numbered lists for readability.
- Maintain a clear hierarchy.
