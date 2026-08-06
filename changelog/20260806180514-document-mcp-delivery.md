# Document the MCP delivery path for skills

- Added a README section explaining that these skills also reach Claude's chat surfaces
  (iOS, Desktop, web) through a self-hosted remote MCP connector, one tool per skill, in
  addition to the existing symlink hook for CLI tools.
- Why: the README described only the filesystem hook, so a reader had no idea the second
  delivery path existed or that skill frontmatter `description` is what drives implicit
  tool selection there.
- Included a brief description of the deployment shape so a reader can stand up their own
  instance — transport, configuration surface, reverse-proxy placement, and the two traps
  that fail silently (allowlists, and a connector URL missing the `/mcp` path).
- No hostname, credential, or machine-specific detail is included — the section describes
  the setup rather than pointing at a repo, and states that self-hosting is required.
