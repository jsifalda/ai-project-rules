---
name: prd-creator
description: "Comprehensive tool for generating detailed Product Requirements Documents (PRDs) in Markdown format. Use when Claude needs to: (1) Transform a feature idea into a detailed technical specification, (2) Gather requirements from a user through structured clarifying questions, (3) Create documentation suitable for junior developers to implement a feature."
---

# Product Requirements Document (PRD) Creator

This skill guides you through creating clear, actionable PRDs suitable for implementation by junior developers.

## Core Workflow

1.  **Receive Initial Prompt**: Start with the user's brief description of the feature.
2.  **Ask Clarifying Questions**: Before writing, you MUST ask clarifying questions to gather missing details. 
    - Use the guide in [references/clarifying-questions.md](references/clarifying-questions.md).
    - Provide options in lettered or numbered lists for easy user response.
    - Focus on the "what" and "why".
3.  **Generate PRD**: Once the user provides answers, generate the PRD.
    - Follow the structure defined in [references/prd-structure.md](references/prd-structure.md).
    - Use clear, unambiguous language. Avoid jargon.
4.  **Save PRD**: Save the output to `./_prds/prd-[feature-name].md`.
    - Ensure the `./_prds/` directory exists or create it.

## Quality Standards

- **Conciseness**: Be thorough but use minimal words to deliver the message.
- **Target Audience**: Write for a **junior developer**. Be explicit and unambiguous.
- **Tone**: Professional, technical, and objective.
- **Independence**: Do NOT start implementing the feature; focus exclusively on the specification.

## Refinement
After generating the initial PRD, ask the user if they want any adjustments. Use their feedback to improve the document.
