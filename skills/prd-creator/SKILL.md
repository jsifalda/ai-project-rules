---
name: prd-creator
description: "Generate a lean Product Requirements Document (PRD) in Markdown from a feature idea, through a structured clarifying-questions interview. Built for planning your own indie side-hustle features, not corporate sign-off. Problem-first and outcome-focused, following a lean template (summary, problem and context, users and use cases, goals and success signals, scope in and out, solution outline with explicit functional requirements, risks and assumptions, open questions). Targets about one page yet stays detailed enough for you or an AI coding agent to build from. Saves each PRD to docs/prds/ and links it from the project README. Use when turning a feature idea into a buildable spec, gathering requirements through clarifying questions, or documenting a side-project feature."
---

# Product Requirements Document (PRD) Creator

This skill guides you through creating lean, buildable PRDs for your own side-hustle features. Each PRD is problem-first, yet detailed enough for you or an AI coding agent to build from.

## Core Workflow

1.  **Receive Initial Prompt**: Start with the user's brief description of the feature.
2.  **Ask Clarifying Questions**: Before writing, you MUST ask clarifying questions to gather missing details.
    - Use the guide in [references/clarifying-questions.md](references/clarifying-questions.md).
    - Provide options in lettered or numbered lists for easy user response.
    - Focus on the "what" and "why".
3.  **Generate PRD**: Once the user provides answers, generate the PRD.
    - Follow the structure defined in [references/prd-structure.md](references/prd-structure.md).
    - Use clear, unambiguous language. Avoid jargon.
4.  **Save PRD**: Save the output to `docs/prds/prd-[feature-name].md`.
    - Create the `docs/prds/` directory if it does not exist.
5.  **Link from README**: Make the PRD discoverable from the project's `README.md`.
    - Ensure a `README.md` exists at the project root; create a minimal one if it does not.
    - Maintain a `## PRDs` section: create it if missing, then add `- [Feature name](docs/prds/prd-feature-name.md)` with a short one-line summary.
    - Be idempotent: if an entry for this PRD already exists, update it rather than adding a duplicate.

## Quality Standards

- **Terse by default**: Fragments over sentences. Bullet points are the default format for every section (prose only when a bullet can't carry the point). One idea per line. Follow the per-section budgets in [references/prd-structure.md](references/prd-structure.md).
- **No filler**: Ban corporate buzzwords (leverage, robust, seamless, synergy, stakeholder, best-in-class, deliverable). No em-dashes, semicolons, or emojis. Use periods, commas, or arrows.
- **Lean**: ~1 page is the ceiling, not the target. This is for planning your own indie projects, not corporate sign-off. Cut any section that doesn't earn its place.
- **Outcome-first**: Start from the problem and who it's for, not from UI ideas.
- **Behavior, not pixels**: Describe what the system does. Keep visual design in a mockup and link it.
- **Success signals**: Define what "good" looks like. Add 1-2 signals only if useful. No baseline required.
- **Target Audience**: Write so you (or an AI coding agent) can build from it. Be explicit and unambiguous.
- **Independence**: Do NOT start implementing the feature; focus exclusively on the specification.

## Refinement

After generating the initial PRD, ask the user if they want any adjustments. Use their feedback to improve the document.

Treat the PRD as a living document — it is the single source of truth for the feature. Update it as decisions change instead of leaving it stale.
