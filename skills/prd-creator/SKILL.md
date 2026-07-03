---
name: prd-creator
description: "Generate a Product Requirements Document (PRD) in Markdown from a feature idea, through a structured clarifying-questions interview. Problem-first and metric-driven, following a best-practice template (summary, problem and context, users and use cases, goals and success metrics, scope in and out, solution outline with explicit functional requirements, risks and dependencies, rollout). Targets 1-2 pages yet stays detailed enough for a junior developer to implement. Saves each PRD to docs/prds/ and links it from the project README. Use when transforming a feature idea into a spec, gathering requirements through clarifying questions, or documenting a feature for a developer to build."
---

# Product Requirements Document (PRD) Creator

This skill guides you through creating clear, actionable PRDs. Each PRD is problem-first and metric-driven, yet detailed enough for a junior developer to implement.

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

- **Outcome-first**: Start from the user problem and measurable goals, not from UI ideas.
- **Behavior, not pixels**: Describe what the system does. Keep visual design in Figma and link it.
- **Metrics**: Every primary metric needs a baseline and a target direction. Add guardrail metrics where relevant.
- **Length**: Target 1-2 pages, using minimal words. Link details out (design, tech design, tracking) rather than inlining them.
- **Target Audience**: Write for a **junior developer**. Be explicit and unambiguous.
- **Tone**: Professional, technical, and objective.
- **Independence**: Do NOT start implementing the feature; focus exclusively on the specification.

## Refinement

After generating the initial PRD, ask the user if they want any adjustments. Use their feedback to improve the document.

Treat the PRD as a living document — it is the single source of truth for the feature. Update it as decisions change instead of leaving it stale.
