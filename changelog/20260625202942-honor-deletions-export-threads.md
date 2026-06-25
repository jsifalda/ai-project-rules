# Add --honor-deletions tombstones to apple-mail-thread-export

- `export_threads.py`: new `--honor-deletions` / `--no-honor-deletions` flag. When a thread's `.md` was deleted from the output folder, the script tombstones it (records `conversation_id` + ROWIDs in `excluded_threads`, drops it from `threads`) and never re-downloads it.
- New activity on a tombstoned thread prints `[tombstoned+new]` instead of restoring it, so curation is honored while corrections are still surfaced.
- The choice is persisted in `.manifest.json` and inherited on later runs, same pattern as `--trim-quotes`.
- Why: lets you curate an exported archive by deleting files, with the deletion itself as the signal, instead of maintaining a subject-pattern blocklist.
