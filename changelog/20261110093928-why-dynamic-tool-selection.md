# why skill picks its own investigation tools

- Replaced the fixed category-based MCP discovery in `why` with per-question source planning, an availability probe, and fallbacks.
- Kept the old categories as examples, and added guard rails for read-only calls, public-identifier egress, and billable calls.
- Why: the closed category set ignored useful tools such as web search, package registries, CI logs and CLIs.
