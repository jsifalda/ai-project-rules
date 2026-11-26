# Archive the obsidian skills in favour of the obsidian plugin

- Archived `defuddle`, `json-canvas`, `obsidian-bases`, `obsidian-cli`, `obsidian-headless` and `obsidian-markdown`, and retired `scripts/sync-obsidian-skills.sh` to `archive/scripts/`.
- Why: the claude.ai obsidian plugin now loads the same skills as `obsidian:<name>`, so every session listed each skill twice.
- `landing-page-copy`, `landing-page-viral-grill` and `summarise-url` now call `obsidian:defuddle`, with the `defuddle` CLI as the fallback when the plugin is absent.
- The local "use instead of WebFetch" defuddle description is gone. The three skills above still route URLs to defuddle.
