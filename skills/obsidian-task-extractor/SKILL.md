---
name: obsidian-task-extractor
description: Extract atomic tasks from source notes and add them to To Remember.md with proper formatting. Use when the user wants to extract tasks from a note, create tasks from note content, or add note-based tasks to a recurring tasks file. Triggers on phrases like "extract tasks from note", "add tasks to To Remember", "create tasks from this note", or any request to convert note content into actionable recurring tasks.
---

# Obsidian Task Extractor

Extracts atomic tasks from source notes and appends them to `To Remember.md` with proper formatting, due dates, and recurring intervals.

## When to Use This Skill

Use this skill when:
- User wants to extract tasks from a note
- Converting note content into actionable recurring tasks
- Adding tasks to `To Remember.md`
- Processing book notes, article highlights, or any content into spaced repetition tasks

## Process

### Step 1: Understand the Source Note
- Search for the source note in the current folder/vault
- Read and understand the content thoroughly
- Identify actionable insights or atomic tasks

### Step 2: Identify Tasks
- Find atomic notes that can be converted to tasks
- Each task should be a single, actionable insight
- Don't modify the original meaning (only shorten if necessary)
- Don't add your own ideas - only extract from the source

### Step 3: Format Tasks
For each task:
- Shorten to max 3 sentences, max 200 characters
- Convert to one line (no newlines within task)
- Remove all hashtags from task text
- If Czech: remove diacritics (čšžáíéůř etc.), keep English otherwise
- Preserve existing uppercase letters, convert others to lowercase
- Reference source note: `[[source_note_name]]`
- Tag with `#task #task-recurring`
- Due date: random date between now and 4 weeks
- Recurrence: `🔁 every 8 weeks`

### Task Format Template
```
- [ ] #task #task-recurring <task text> [[source_note]] 📅 YYYY-MM-DD 🔁 every 8 weeks
```

### Example Output
```
- [ ] #task #task-recurring pokud jste nervozni, najdete si v obecenstvu jednoho cloveka, ktery se usmiva a prikyvuje. zamerte se nasledne na nej → vypravejte to vsichno jemu [[Hidden Potential]] 📅 2025-09-16 🔁 every 8 weeks
```

### Step 4: User Confirmation
- Present identified tasks to user
- Ask for confirmation before adding
- Allow user to edit/remove tasks

### Step 5: Append to File
- Add confirmed tasks to `To Remember.md`
- Append only (don't modify existing content)
- Ensure proper formatting

## Bundled Resources

### Scripts
- `scripts/extract_tasks.py` - Python script for formatting tasks (optional helper)

## Important Guidelines

1. **Ultrathink mode**: Think deeply about the source content
2. **No hallucination**: Only extract tasks from the source, don't invent
3. **Preserve meaning**: Shorten but don't change meaning
4. **Language handling**:
   - Czech text: remove diacritics, keep structure
   - English text: lowercase except existing uppercase
5. **One line per task**: No newlines within task text
6. **Due dates**: Random between today and 4 weeks out
7. **Always confirm**: Show tasks to user before modifying file
8. **Append only**: Never delete or modify existing tasks