---
name: seo-keyword-generator
description: Generate comprehensive SEO keyword strategies for side project ideas. Walks through a structured questionnaire to understand the project, then produces categorized keywords based on strategic analysis. Use when user wants keywords, SEO strategy, or organic traffic planning for a product or side project.
---

# SEO Keyword Generator

Generate a comprehensive keyword strategy for side projects by combining SEO expertise with user psychology analysis.

## When to Use

- user asks for "keywords" for a project or idea
- user wants SEO strategy or organic traffic planning
- user says "help me find keywords for..."
- user mentions driving organic traffic to a side project

## Process

### Phase 1: Gather Project Description

Ask the user to describe their project. If they haven't provided one, prompt with:

> describe your project in 2-3 sentences: what it does, who it's for, and what problem it solves.

If the description is vague, ask follow-up questions (max 3) to clarify:
- what specific problem does it solve?
- who is the target user? (developer, marketer, small business owner, etc.)
- are there existing tools/competitors? which ones?

Do NOT proceed to analysis until you have a clear project description.

### Phase 2: Strategic Analysis

Perform a chain-of-thought analysis before generating any keywords. Cover all four areas described in `references/strategic-analysis.md`. Present the analysis as a summary to the user for validation.

**Output format for analysis:**
```
**project definition:** [refined value proposition]
**key components:** [purpose, use case, tech, versatility, comparisons]
**target audience:** [proficiency level, pain points]
**emotional drivers:** [frustrations, desired feelings]
```

Ask: *does this capture your project accurately? anything to adjust?*

### Phase 3: Keyword Generation

Based ONLY on the validated analysis, generate keywords in 6 categories. Follow the format and guidance in `references/keyword-categories.md`.

**Output rules:**
- minimum 8 keywords per category
- no generic terms (avoid "best tool", "free app" without qualifier)
- include search intent signals
- mix volume levels (head terms + long tail)
- format as structured bullet lists (no tables)

### Phase 4: Prioritization

After generating keywords, add a "top 10 priority keywords" section:
- rank by estimated impact (intent + reachability for a new project)
- explain WHY each keyword is prioritized
- suggest which to target first (low competition + high intent = quick wins)

## References

- `references/strategic-analysis.md` — detailed analysis framework
- `references/keyword-categories.md` — category definitions and examples
