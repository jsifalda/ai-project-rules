---
name: qmd-ask
description: Answer questions about THIS folder's markdown using its local on-device qmd semantic index instead of reading files one by one. Runs hybrid keyword plus vector search with reranking, pulls full documents when a snippet is thin, and answers grounded only in what the files actually say, citing the source paths. Use when the user asks something that should be answered from this folder's contents, for example what do my notes say about X, according to these docs, search my notes for Y, ask the docs about Z, summarize what's here on W, or runs /qmd-ask. Do NOT use to rebuild or refresh the index, to search the global qmd index, or for questions unrelated to this folder.
---

# qmd-ask

Answer the user's question from this folder's local qmd index (`__QMD_INDEX__`). Retrieve first, then answer only from what you retrieved. Never answer this folder's questions from outside knowledge.

## Scoped qmd wrapper

All qmd calls go through the bundled wrapper, which finds the project root and sets the folder-local scope automatically:

```bash
.claude/skills/qmd-ask/scripts/ask.sh <qmd-subcommand> [args]
```

It is equivalent to `INDEX_PATH=.qmd/__QMD_INDEX__.sqlite QMD_CONFIG_DIR=.qmd/config qmd --index __QMD_INDEX__ <...>`. Works from any subdirectory of the project.

## Workflow

1. **Retrieve.** Run the user's question through hybrid search (auto-expand + rerank):
   ```bash
   .claude/skills/qmd-ask/scripts/ask.sh query "<the user's question>"
   ```
   For a known exact term or identifier, use a structured query instead. The first line gets 2x weight in fusion, so lead with your best guess:
   ```bash
   .claude/skills/qmd-ask/scripts/ask.sh query $'lex: <keywords>\nvec: <natural question>'
   ```
   Results come back as ranked snippets with `qmd://__QMD_INDEX__/<path>` ids and scores.

2. **Read full context when a snippet is central but truncated.** Pull the whole document:
   ```bash
   .claude/skills/qmd-ask/scripts/ask.sh get "qmd://__QMD_INDEX__/<path>"
   .claude/skills/qmd-ask/scripts/ask.sh multi-get "<glob>"
   ```

3. **Answer.** Synthesize from the retrieved passages only. Cite the source file(s) by path. If the index returns nothing relevant, say so plainly and stop. Do not fill gaps with outside knowledge.

4. **Match the user's writing style.** Concise, active voice, certain language, no em-dash or semicolon, use `→`.

## Notes

- If a `qmd` MCP `query` tool is available this session, you may use it for structured multi-search (lex/vec/hyde in one call). The CLI wrapper always works without a restart, so prefer it when unsure.
- If `ask.sh` reports the index is not found, this folder has not been indexed yet. Tell the user the index must be built before questions can be answered, then retry once it exists.
- After files change, refresh with `.claude/skills/qmd-ask/scripts/ask.sh update && .claude/skills/qmd-ask/scripts/ask.sh embed` (also happens automatically on session start).
