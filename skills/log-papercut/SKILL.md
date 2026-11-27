---
name: log-papercut
description: File a short papercut report when a skill, tool, CLI or doc gives friction — 3+ failed tries at one step, a listed flag the tool rejects, exit 0 on an error, a query that finds nothing it should, or a wrong doc. Fire and forget, then carry on. Do NOT use for bugs in the user's own product code or for feature requests.
metadata:
  version: "1.0"
---

# Log a papercut

A papercut is one small report about friction with a skill, tool, CLI or doc.
File it, then continue the task. Never block on it. Never ask the user about it.

## Redaction rule

- Never put file contents, secrets, tokens, customer data, patient data or PHI in a papercut.
- Paths, flags, tool names and error class names are fine.
- Summarise. Do not paste logs.

## Steps

1. Decide that it is a papercut. Use it after 3 failed attempts at the same step, or for one clear defect. An attempt is one try at the same step with the same approach. Three different approaches that fail count too. Check: you can state the symptom in one line.
2. Write each field in plain words. The fields are skill, title, tried, expected, got and fix. Check: no field holds a secret or a pasted log.
3. Run the script. Check: it prints a URL, "commented #<n>" or "logged to <path>".

```bash
bash "<this skill's base directory>/scripts/file.sh" --skill <name> --title "<short symptom>" \
  --tried "<what you ran>" --expected "<what should happen>" --got "<what happened>" --fix "<your idea>"
```

4. Read the exit code. Check: 0 means filed or logged. Go back to your task.

## Where it goes

- If `PAPERCUT_REPO` is set and `gh` works, the script opens an issue with the label `papercut`. An open issue with the same title gets a comment instead.
- Else the script appends one JSON line to `PAPERCUT_FILE`. The default is `papercuts.jsonl` in `XDG_STATE_HOME`, or in `~/.local/state`.

## Error recovery

| Failure | Fix |
| --- | --- |
| Exit 2, usage printed | Add the missing flag. Every flag in the command above is required. |
| Exit 3, secret guard | Remove the secret from the field. Describe it, for example "a token". Run again. |
| Script prints "logged to <path>" when you expected an issue | Set `PAPERCUT_REPO` to `owner/name` and check that `gh auth status` passes. The line in the file is still valid. |
| `bash` cannot find the script | Use the base directory your agent gave when it loaded this skill. Else find it with `ls` in the skills folder of your agent. |
| Both node and python3 are missing | Skip the report. Say in your final answer that you skipped it. |
