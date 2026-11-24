---
name: defuddle
description: Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page. Do NOT use for URLs ending in .md — those are already markdown, use WebFetch directly.
metadata:
  version: "1.1"
  upstream: "https://github.com/kepano/obsidian-skills"
---

# Defuddle

Use Defuddle CLI when the user wants clean Markdown extracted from a web page. It removes navigation, ads, and other page clutter.

Check availability with `defuddle --help`. If it is missing, explain the dependency and offer installation with `npm install -g defuddle`. Do not claim extraction succeeded if the tool is unavailable or returns an error.

## Usage

Always use `--md` for markdown output:

```bash
defuddle parse <url> --md
```

Save to file:

```bash
defuddle parse <url> --md -o content.md
```

Extract specific metadata:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with both HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |
