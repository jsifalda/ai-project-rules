---
name: create-svg-image
description: Generate production-quality SVG images (banners, cards, heroes, badges, posters) from a text description. Optionally enriches content by fetching a URL to extract branding, copy, and stats. Asks targeted clarifying questions one-at-a-time for missing info, then outputs a hand-crafted SVG file. Use when the user asks to "create an SVG", "generate a banner image", "make a card image", "create an OG image", "design a badge", or needs a vector image created from a description. Do NOT use for raster images (PNG/JPG), photo editing, or complex illustrations with many detailed shapes.
---

# Create SVG Image

Generate hand-crafted SVG images from user descriptions. The output is a single `.svg` file — no external dependencies, no build step, no raster conversion.

## Workflow

1. **Gather intent** — Determine image type, purpose, and where it will be used
2. **Extract content** (optional) — If a URL is provided, fetch it and extract brand name, tagline, key stats, color palette, audience
3. **Ask clarifying questions** — One at a time, only for missing critical info (see Required Inputs below)
4. **Generate SVG** — Compose the image using patterns from [references/svg-patterns.md](references/svg-patterns.md)
5. **Save** — Write to the user-specified path (or suggest a reasonable default)

## Required Inputs

Gather these before generating. Ask one question at a time for any that are missing:

| Input | Ask when missing | Default if not asked |
|-------|-----------------|---------------------|
| **Image type** | Always — determines dimensions and layout | — |
| **Title text** | Always | — |
| **Tagline / subtitle** | When type is banner, hero, or card | Skip for badges |
| **Output path** | Always — where to save the file | `./output.svg` |
| **Color mood** | When no URL or brand colors provided | Dark + indigo accent |
| **Stats / metrics** | Only suggest if URL content contains numbers | Skip |

Do NOT ask about: font choices (always use system fonts), SVG internals, or technical details.

## Content Extraction from URL

When the user provides a URL, fetch it and extract:
- **Brand name** — from `<title>`, `<h1>`, or OG meta
- **Tagline** — from hero text, meta description, or first prominent heading
- **Key stats** — any numbers with labels (e.g., "12k+ users", "99.9% uptime")
- **Color scheme** — infer mood from the site (dark/light, accent color family)
- **Audience** — from copy like "for developers", "for founders", etc.

Present extracted info to the user for confirmation before generating.

## SVG Generation Rules

- Always set `xmlns="http://www.w3.org/2000/svg"` and explicit `width`, `height`, `viewBox`
- Use system font stack: `system-ui, -apple-system, 'Segoe UI', sans-serif`
- Use `<defs>` for gradients and patterns — keep markup clean
- Add decorative elements for visual depth (circles, accent bars, patterns) — never leave flat backgrounds
- Escape XML entities in text content (`&amp;`, `&lt;`, `&gt;`)
- Keep file size under 10KB — SVGs should be lean

Consult [references/svg-patterns.md](references/svg-patterns.md) for reusable building blocks: backgrounds, typography, decorative elements, color palettes, and layout patterns.

## Example

**User**: "Create a banner for SignalSeek — it's a Reddit growth tool for solo founders. Here's the site: signalseek.cc"

**Flow**:
1. Fetch signalseek.cc → extract: name "SignalSeek", tagline "Turn Reddit into a growth channel that actually sounds like you", stats (12k+ subreddits, <15m setup, 94% matches), audience "solo founders"
2. Ask: "Where should I save the banner?" → user says `public/signalseek-banner.svg`
3. Ask: "Color mood — the site uses a dark theme with indigo accents. Should I match that?" → user confirms
4. Generate 1200×630 SVG with dark gradient background, indigo accents, title, tagline, stat blocks, "FOR SOLO FOUNDERS" badge, and URL footer
5. Save to `public/signalseek-banner.svg`
