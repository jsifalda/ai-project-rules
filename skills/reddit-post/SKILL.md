---
name: reddit-post
description: Create high-engagement Reddit posts (title + body) that follow proven patterns from top-performing posts. Walks the user through a questionnaire to gather context before generating the post. Use when the user wants to create a Reddit post, write content for a subreddit, or needs help crafting viral-worthy Reddit content.
---

# Reddit Post Creator

Creates complete Reddit posts (title + body) optimized for engagement using proven patterns from top-performing posts.

## When to Use

Use when the user:
- Wants to create a Reddit post for any subreddit
- Needs help writing viral-worthy content
- Says "write a reddit post about..." or "create a post for r/..."
- Wants to share something on Reddit and needs it formatted properly

## Process

### Step 1: Gather Context via Questionnaire

Ask the user these questions ONE BY ONE. Do not generate the post until all are answered:

1. **Which subreddit?** (e.g., r/ObsidianMD, r/programming, r/startups)
2. **What's the topic?** (what are you sharing?)
3. **What pain point does it solve?** (or what value does it provide?)
4. **Personal angle?** (your journey, struggles, funny story?)
5. **Any visuals?** (screenshots, GIFs, graphs you can include?)
6. **Want engagement?** (asking for feedback, beta testers, questions?)
7. **Niche or impressive scale?** (thousands of users, specialized use case?)
8. **Relevant trends?** (tying to recent news, updates, migrations?)

### Step 2: Apply Reddit Success Principles

Based on analysis of top posts, incorporate:

**Offer tangible value**
→ Share tools, workflows, or solutions to common problems

**Include visual hooks**
→ Suggest screenshots, GIFs, or graphs that demonstrate the setup

**Be relatable and personal**
→ Use humor, share your journey, address frustrations people feel

**Encourage interaction**
→ Ask for feedback, beta testers, or community input

**Highlight impressive applications**
→ Showcase scale (thousands of users) or specialized uses

**Time with trends**
→ Reference recent updates, migrations, or ecosystem news

**Keep it concise yet detailed**
→ Short paragraphs, specific steps, minimal fluff

### Step 3: Generate Post

Create TWO options:

**Option A: The Direct Value Post**
- Clear title stating what you're sharing
- Bullet points for easy scanning
- Specific details (numbers, tools, steps)
- Direct call to action

**Option B: The Story/Journey Post**
- Hook with personal experience
- Build narrative arc (problem → discovery → solution)
- End with question or invitation
- More conversational tone

## Output Format

```
**Subreddit:** r/[subreddit]
**Topic:** [topic summary]

---

**OPTION A: Direct Value Post**

**Title:** [title]

[body text with proper formatting]

---

**OPTION B: Story/Journey Post**

**Title:** [title]

[body text with proper formatting]

---

**Suggested Visuals:**
• [what to screenshot/GIF]
• [what to screenshot/GIF]

**Best Posting Time:** [day/time recommendation for the subreddit]
```

## Rules

- No clickbait titles — deliver on the promise
- No walls of text — use line breaks and bullets
- Match the subreddit's tone (check recent top posts first if unsure)
- Include specific numbers/data when possible
- End with a question or clear CTA to drive comments
