#!/usr/bin/env python3
"""
Obsidian Task Extractor Script

Extracts atomic tasks from a source note and appends them to To Remember.md
with proper formatting, dates, and recurring intervals.
"""

import re
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

def shorten_task(text: str, max_chars: int = 200, max_sentences: int = 3) -> str:
    """Shorten task to max 3 sentences and 200 chars, one line."""
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    # Take max 3 sentences
    sentences = sentences[:max_sentences]
    
    # Join and truncate if needed
    result = ' '.join(sentences)
    if len(result) > max_chars:
        result = result[:max_chars-3].rsplit(' ', 1)[0] + '...'
    
    # Clean up whitespace
    result = ' '.join(result.split())
    
    return result

def remove_diacritics(text: str) -> str:
    """Remove Czech/Slovak diacritics while preserving uppercase letters."""
    diacritic_map = {
        'á': 'a', 'Á': 'A',
        'č': 'c', 'Č': 'C',
        'ď': 'd', 'Ď': 'D',
        'é': 'e', 'É': 'E',
        'ě': 'e', 'Ě': 'E',
        'í': 'i', 'Í': 'I',
        'ň': 'n', 'Ň': 'N',
        'ó': 'o', 'Ó': 'O',
        'ř': 'r', 'Ř': 'R',
        'š': 's', 'Š': 'S',
        'ť': 't', 'Ť': 'T',
        'ú': 'u', 'Ú': 'U',
        'ů': 'u', 'Ů': 'U',
        'ý': 'y', 'Ý': 'Y',
        'ž': 'z', 'Ž': 'Z',
    }
    
    result = ''
    for char in text:
        if char in diacritic_map:
            result += diacritic_map[char]
        else:
            result += char
    
    return result

def normalize_case(text: str) -> str:
    """Preserve existing uppercase, convert other letters to lowercase."""
    result = ''
    for char in text:
        if char.isupper():
            result += char
        else:
            result += char.lower()
    return result

def remove_hashtags(text: str) -> str:
    """Remove any hashtags from the task text."""
    # Remove hashtags but keep the word
    return re.sub(r'#(\w+)', r'\1', text).strip()

def generate_due_date() -> str:
    """Generate a due date randomly between now and 4 weeks from now."""
    days_ahead = random.randint(0, 28)
    due_date = datetime.now() + timedelta(days=days_ahead)
    return due_date.strftime('%Y-%m-%d')

def format_task(task_text: str, source_note: str, is_czech: bool = False) -> str:
    """Format a single task according to the template."""
    # Clean the task
    task_text = remove_hashtags(task_text)
    task_text = shorten_task(task_text)
    
    # Process case
    task_text = normalize_case(task_text)
    
    # Remove diacritics if Czech
    if is_czech:
        task_text = remove_diacritics(task_text)
    
    # Generate due date
    due_date = generate_due_date()
    
    # Format the task line
    formatted = f"- [ ] #task #task-recurring {task_text} [[{source_note}]] 📅 {due_date} 🔁 every 8 weeks"
    
    return formatted

def append_tasks_to_file(tasks: list, target_file: str):
    """Append tasks to the target file."""
    target_path = Path(target_file)
    
    # Ensure file exists
    if not target_path.exists():
        target_path.write_text("# To Remember\n\n")
    
    # Read existing content
    existing = target_path.read_text(encoding='utf-8')
    
    # Append tasks
    new_content = existing.rstrip() + '\n' + '\n'.join(tasks) + '\n'
    
    # Write back
    target_path.write_text(new_content, encoding='utf-8')

def is_czech_text(text: str) -> bool:
    """Detect if text contains Czech/Slovak diacritics."""
    czech_chars = 'áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ'
    return any(char in czech_chars for char in text)

def main():
    if len(sys.argv) < 3:
        print("Usage: extract_tasks.py <source_note_name> <tasks_file>")
        sys.exit(1)
    
    source_note = sys.argv[1]
    tasks_file = sys.argv[2]
    
    # Read tasks from stdin or file
    if sys.stdin.isatty():
        # Read from tasks file
        tasks_path = Path(tasks_file)
        if not tasks_path.exists():
            print(f"Error: Tasks file not found: {tasks_file}")
            sys.exit(1)
        tasks_content = tasks_path.read_text(encoding='utf-8')
    else:
        # Read from stdin
        tasks_content = sys.stdin.read()
    
    # Split into individual tasks (one per line, or by bullet points)
    raw_tasks = [t.strip() for t in tasks_content.strip().split('\n') if t.strip()]
    
    # Detect language from first task
    is_czech = any(is_czech_text(t) for t in raw_tasks)
    
    # Format each task
    formatted_tasks = []
    for task in raw_tasks:
        # Skip lines that look like headers or empty
        if task.startswith('#') or not task:
            continue
        # Remove bullet markers if present
        task = re.sub(r'^[-*•]\s*', '', task)
        formatted = format_task(task, source_note, is_czech)
        formatted_tasks.append(formatted)
    
    # Output formatted tasks for confirmation
    print("=" * 60)
    print("TASKS TO BE ADDED:")
    print("=" * 60)
    for task in formatted_tasks:
        print(task)
    print("=" * 60)
    print(f"\nTotal: {len(formatted_tasks)} tasks")
    
    # Save to temp file for confirmation step
    output_path = Path('/tmp/formatted_tasks.txt')
    output_path.write_text('\n'.join(formatted_tasks), encoding='utf-8')

if __name__ == '__main__':
    main()