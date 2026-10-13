# Add Claude directory readiness to add-mcp-api

- `add-mcp-api` plans now include a directory submission phase by default. The plan marks it skipped only when the user states the connector stays private.
- A new `directory-readiness.md` reference holds the Claude directory rules: tool annotations, descriptions, prompt-injection bans, errors, payload limits, listing assets, the reviewer seed, verification, portal limits, and compliance. It cites the Anthropic sources, reviewed 2026-10-11.
- The protocol reference gains the Claude client authorization facts. The tool contract record makes the title and every hint mandatory. The traps table gains the failures found while a real connector was prepared for the directory.
- Why: a real connector prepared for the directory showed gaps in the old plan, in annotations, descriptions, errors, verification, and listing assets.
