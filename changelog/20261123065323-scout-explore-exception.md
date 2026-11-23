# Keep the Explore exception for web, MCP or skill searches

- `rules/general.md` now sends a broad search to `Explore` when it needs web, MCP or a skill, or when `scout` is not installed.
- Why: `scout` has only Read, Grep, Glob and Bash. The rule now matches `agents/scout.md` and `op`.
