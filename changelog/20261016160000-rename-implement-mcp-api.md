# Rename add-mcp-api to implement-mcp-api

- Renamed the `add-mcp-api` skill to `implement-mcp-api` and bumped it to 2.0, since the trigger name changes.
- Reworded it so its plan is the input for plan mode, so that a user plans and implements the MCP API in one step.
- Scoped the no-code rule to the time before plan-mode approval, added execution guidance, and kept a separate ask before the directory submission and public copy.
- The skills connector tool changes from `skill_add_mcp_api` to `skill_implement_mcp_api`. A `SKILLS_ENABLED` list that names `add-mcp-api` must change too.
