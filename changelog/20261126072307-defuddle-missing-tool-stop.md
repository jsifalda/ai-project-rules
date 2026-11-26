# Stop when the defuddle fetch cannot run

- `landing-page-copy`, `landing-page-viral-grill` and `summarise-url` now stop and tell the user when the fetch tool is missing or the fetch errors, and never report a fetch that did not run.
- Why: archiving the local `defuddle` skill dropped its availability check, so an agent without the plugin or the CLI had no allowed path and could summarise a page it never read.
