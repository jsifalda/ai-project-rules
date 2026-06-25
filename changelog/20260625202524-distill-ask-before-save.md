# distill-notes / distill-notes-v2 ask before saving a file

- Both skills no longer auto-write the `outputs/<slug>-distilled.md` file. They now print the result
  in chat, then prompt the user and save only on a yes.
- Why: the skills created a file on disk every run whether the user wanted it or not. The file is now
  opt-in. Save location and naming logic are unchanged, only the trigger.
- Updated the frontmatter descriptions and README rows to match.
