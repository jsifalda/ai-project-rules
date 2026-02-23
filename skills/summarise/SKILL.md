---
name: Summarise Link
description: Fetch link content, understand context, and return correctly summarised version
---

## IMPORTANT: Use Wrapper Script for Model Control

When user asks to summarize a URL, ALWAYS use the wrapper script instead of direct fetching:

```bash
bash /root/.openclaw/workspace/scripts/summarise-url.sh <URL>
```

This ensures:
- Uses `openrouter/google/gemini-3.1-pro-preview` (cheaper model)
- Consistent output format
- Proper timeout handling

## Manual Instructions (only if wrapper fails)

If you must run directly:
- Use model: `openrouter/google/gemini-3.1-pro-preview`
- get content of URL
- fully understand the context
- provide the main idea, followed by key practical takeaways, and then actionable step by step plan to use it in my context

Other guidelines to follow:
- reason from first principles and explain your thought process; if you're making assumptions, state them clearly
- write like a human, no fluff, no cringe, & prefer bullet points
- be concise (use minimal words to deliver the message)