---
name: prompt-enhancer
description: Transform simple prompts into high-quality, structured prompts that produce better AI results. Use when the user wants to improve a prompt, make it more effective, optimize prompt quality, or enhance prompt clarity. Triggers on requests like "enhance this prompt", "make this prompt better", "optimize this prompt", "improve my prompt", or when the user pastes a prompt and wants it refined.
---

# Prompt Enhancer

Transforms user prompts into optimized versions that produce higher-quality AI outputs.

## When to Use This Skill

Use when the user:
- Asks to enhance/improve/optimize a prompt
- Pastes a prompt and wants it better
- Says "make this more effective" or "upgrade this prompt"
- Wants clearer, more structured instructions for AI

## Enhancement Process

### Step 1: Analyze the Input
Read the user's prompt carefully. Identify:
- What task they want accomplished
- What's unclear or vague
- What's missing (context, format, constraints)
- The intended audience/use case

### Step 2: Apply Enhancement Principles

**1. Clarity & Specificity**
- Remove ambiguity
- Define exact expectations
- Specify scope and boundaries
- Be concise (minimal words, maximum clarity)
- NO questions in the output

**2. Structure**
- Add clear sections when needed
- Use numbered steps for sequential tasks
- Include format specifications

**3. Context**
- Add relevant background
- Define target audience
- Specify use case

**4. Role Definition**
- Assign clear persona/expertise level
- Define perspective to take

**5. Constraints & Parameters**
- Set length/depth expectations
- Define tone and style
- List what to include AND exclude

**6. Quality Criteria**
- Define what "good" looks like
- Add success metrics if applicable

**7. Examples (when helpful)**
- Include input/output examples
- Show edge cases if relevant

### Step 3: Generate Enhanced Prompt

Create the improved version following these rules:
- Start with a clear role definition
- Use imperative/commands (not questions)
- Structure with headers/bullets/numbers
- Be specific, not generic
- Remove fluff
- Focus on the prompt text only

## Output Format

**Enhanced Prompt only** — the improved version, ready to use.
- No explanations
- No "Here's the enhanced version" wrapper
- No markdown code blocks around the output (unless the prompt itself needs them)
- Just the clean, enhanced prompt text

## Example

**Input:**
```
Write about climate change
```

**Output:**
```
You are an environmental science writer. Write a comprehensive 500-word article about climate change impacts.

Structure:
1. Opening hook with startling statistic
2. Three major impacts (environmental, economic, social)
3. Call to action for individuals

Requirements:
- Accessible to general audience (no jargon without explanation)
- Include 2-3 specific data points with years
- Optimistic but realistic tone
- End with actionable steps readers can take

Exclude:
- Political blame or partisan language
- Technical scientific processes
- Predictions beyond 2050
```