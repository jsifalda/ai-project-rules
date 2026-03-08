---
name: keyword-strategy-generator
description: Generate comprehensive, psychologically-informed keyword strategies for side-projects. Use when you need a step-by-step SEO keyword plan that (1) analyzes a project, (2) reasons about user pain points and emotional drivers, and (3) returns categorized keywords (informational, transactional, tail lengths, niche, question-based, and emotional). Trigger by providing a {project_description} and asking for "keyword strategy" or "generate keywords".
---

# keyword-strategy-generator

purpose
• produce high-quality keyword lists grounded in a short strategic analysis and user psychology. Designed for side-project ideation, SEO planning, and product marketing.

inputs
• project_description (required): short paragraph describing the project, core feature(s), users, and primary goal.
• optional: target_region, language (defaults to english), priority_goals (traffic|conversions|brand|support).

output
• a two-part result:
  1) step-1 strategic analysis (concise summaries for project definition, key components, target audience, emotional drivers)
  2) step-2 categorized keyword lists: Informational, Transactional, Short/Medium/Long tail, Niche & Low-Competition, Question-Based, Emotional & Psychological

quality rules
• follow the two-step process exactly: analysis must be produced first and used as the only basis for keyword generation.
• avoid generic single-word keywords (e.g., "product", "app"). prefer specific, intent-rich phrases.
• include a mix of head terms and long-tail phrases — annotate each category with example search intent when helpful.
• provide at least 8–15 keywords per major category; fewer for very niche projects is acceptable but explain why.
• label which keywords are short/medium/long tail.

prompt template (to use when triggering this skill)
```
system: role: senior seo strategist + product marketing manager (user psychology expert)

context: need comprehensive keyword strategy for organic traffic—focus functional needs + emotional drivers

input:
{project_description}

instructions:
1) run Strategic Analysis: produce concise summaries for Project Definition, Key Components, Target Audience, Emotional Drivers
2) based only on Step-1, generate categorized keywords: Informational, Transactional, Short/Medium/Long Tail, Niche & Low-Competition, Question-Based, Emotional & Psychological
3) output: Step-1 analysis then Step-2 lists. keep language: english. format: bullet lists.
```

examples
• example invocation: "generate keywords for: a lightweight habit-tracking web app that uses micro-habits and gamification to help busy professionals build morning routines. target: english, conversions."
• expected first line of analysis: "project definition: a lightweight habit-tracking web app that helps busy professionals create and sustain morning routines through micro-habits and gamification. core value: quick, low-friction habit formation with tangible streak rewards."

implementation notes for Codex
• this skill is primarily text-driven; no scripts required. if repeated automation is desired, add `scripts/generate_keywords.py` to accept project_description and output JSON.
• keep SKILL.md concise. move heavy examples to references/ if needed.

when to use
• use this skill for brainstorming SEO-aware keywords, preparing landing page copy, PPC negative keyword hunting, content calendar planning, or validating product-market fit via search demand signals.

end
