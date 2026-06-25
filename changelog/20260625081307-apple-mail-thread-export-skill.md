# Add apple-mail-thread-export skill

- New skill that exports Apple Mail conversation threads from a given sender into one markdown file per thread.
- Groups by the native `conversation_id`, extracts `.emlx` bodies with the Python stdlib, names files from the (de-prefixed, ASCII-transliterated) subject, and optionally trims quoted reply history.
- Keeps a `.manifest.json` in the output folder so re-runs only write new or changed threads (incremental sync).
- Why: recurring need to archive a sender's correspondence locally as readable, searchable notes without re-downloading what's already saved.
- Self-contained (stdlib only, no installs, no cross-skill references); generic over sender + output dir so it carries no personal data. Verified universal (scanner clean), which is why it lives in the public repo while the exported email data stays local.
