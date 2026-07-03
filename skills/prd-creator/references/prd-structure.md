# PRD Structure

Target 1-2 pages. Link details out (Figma, tech design, tracking plan) rather than inlining them. Scale sections 7 and 8 to feature size — a few bullets for a small feature.

The generated PRD must include the following sections:

1.  **Summary**: 2-3 sentences — what we're building, for whom, and why now.
2.  **Problem & Context**:
    - The user problem or opportunity in plain language (avoid solution talk).
    - Supporting evidence: top support issues, funnel drop-offs, competitor gaps, or other data.
    - Why it matters — to the user and to the business.
    - Existing behavior/workaround: how users solve this today, if at all.
3.  **Users & Key Use Cases**:
    - Primary users named by segment/role/JTBD (not "everyone"). Note any secondary or admin users.
    - 3-7 user stories: "As a [user], I want [action] so that [benefit]."
4.  **Goals & Success Metrics**:
    - Goal statement: what "good" looks like after shipping.
    - 2-3 primary metrics, each with a baseline and a target direction (or magnitude).
    - 1-2 guardrail metrics that must NOT degrade (e.g. latency, error rate, support tickets).
5.  **Scope (In / Out)**:
    - **In scope**: 5-10 bullets of capabilities or flows this iteration will deliver.
    - **Out of scope / Non-Goals**: 5-10 bullets explicitly excluded for now, to manage scope.
6.  **Solution Outline, Requirements & Constraints**:
    - High-level approach: 1-3 short paragraphs on the core idea and how it solves the problem. No pixel-level design.
    - **Functional Requirements**: a numbered list of specific behaviors. Use "The system must..." or "The user must be able to..." phrasing. Be explicit and unambiguous — a junior developer implements from these.
    - Key behaviors & edge cases: permissions, limits, failure modes, invalid input.
    - Design references: link Figma/Miro for flows and interaction detail. Do not inline pixel specs.
    - Technical constraints & dependencies: integration points, performance budgets, legal/data constraints.
7.  **Risks, Assumptions & Dependencies**:
    - Assumptions: 3-7 things we assume are true (user behavior, data quality, partner availability).
    - Risks: 3-7 major risks (execution, UX, adoption, legal). Optionally label severity/likelihood.
    - Dependencies: other teams, services, vendors, or decisions this depends on — each with an owner.
8.  **Rollout & Measurement**:
    - Rollout plan: high-level stages (internal dogfood → beta cohort → GA), rough dates, gating criteria.
    - Tracking & analytics: events to fire, dashboards/alerts to watch impact and health.
    - Launch checklist (optional): comms, docs, training, support updates.
9.  **Open Questions**: unresolved decisions or areas needing clarification. Keep this updated as the PRD evolves — it doubles as the living-document tracker.

## Format
- Use Markdown headers (#, ##).
- Use bulleted and numbered lists for readability.
- Maintain a clear hierarchy.
