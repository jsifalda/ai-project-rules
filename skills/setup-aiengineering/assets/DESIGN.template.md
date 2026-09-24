---
version: alpha
name: <Project name>
description: <one line describing the product>
colors:
  primary: "<#hex or oklch>"
  secondary: "<#hex or oklch>"
  accent: "<#hex or oklch>"
  background: "<#hex or oklch>"
  surface: "<#hex or oklch>"
  text: "<#hex or oklch>"
  muted: "<#hex or oklch>"
  border: "<#hex or oklch>"
  danger: "<#hex or oklch>"
typography:
  display: { fontFamily: "<font stack>", fontSize: "<size>", fontWeight: "<weight>", lineHeight: "<line-height>" }
  heading: { fontFamily: "<font stack>", fontSize: "<size>", fontWeight: "<weight>", lineHeight: "<line-height>" }
  body: { fontFamily: "<font stack>", fontSize: "<size>", fontWeight: "<weight>", lineHeight: "<line-height>" }
  mono: { fontFamily: "<font stack>", fontSize: "<size>", fontWeight: "<weight>", lineHeight: "<line-height>" }
spacing:
  xs: "<4px>"
  sm: "<8px>"
  md: "<16px>"
  lg: "<24px>"
  xl: "<32px>"
rounded:
  sm: "<2px>"
  md: "<6px>"
  lg: "<12px>"
  full: "<9999px>"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.background}"
    rounded: "{rounded.md}"
    padding: "<12px>"
  button-primary-hover:
    backgroundColor: "<darker or lighter shade of {colors.primary}>"
---

# <Project name> design

<!--
Replace every <...> placeholder with a real value.
Keep the canonical sections in this exact order.
Delete a section only when the product has no such concern.
Keep this file compact. Move per-component detail to separate docs and link them from Components.
Mark any value inferred from existing code as (inferred).
Never leave a placeholder in a shipped file.
Delete this comment before you write the file.
-->

## Overview
<2-3 sentence product brief. State who uses it and what it does.>
Aesthetic reference: <one real-world object, era, or publication, not a list of adjectives>.

## Colors
- primary: <value> — <intent> — do not use for <context>
- secondary: <value> — <intent> — do not use for <context>
- accent: <value> — <intent> — do not use for <context>
- background, surface, text, muted, border, danger: <value + intent for each>
- Rule: one dominant colour with sharp accents. Not an evenly spread palette.

## Typography
- display: <when to use, e.g. hero and marketing headlines only>
- heading: <when to use, e.g. section and page titles>
- body: <when to use, e.g. paragraph and UI copy>
- mono: <when to use, e.g. code and numeric data>
- Pair a distinctive display face with a refined, readable body face.

## Layout
- Spacing base unit: <value, e.g. 4px>
- Grid: <columns, gutters>
- Breakpoints: <list, e.g. 375, 768, 1024, 1440>
- Responsive behaviour: <how layout adapts across breakpoints>

## Elevation & Depth
- Shadow levels: <name each level and its value, e.g. sm/md/lg>
- Z-index levels: <name each layer and its value, e.g. base/dropdown/modal/toast>

## Shapes
- Radius scale: <exact values for sm, md, lg, full>

## Components
- <component name>: use when <case>, versus <alternative>. Import: `<path>`
- <component name>: use when <case>, versus <alternative>. Import: `<path>`
- Add one entry per reusable component so agents reuse it instead of rebuilding it.

## Do's and Don'ts
Do:
- Name one concrete aesthetic reference and design toward it.
- Route every colour, size, radius, shadow, and font through a token.
- Use a dominant colour with sharp accents.
- Pair a distinctive display face with a refined body face.
- Check every layout at 320, 375, 414, and 768 px wide.
- Write honest copy. No invented metrics, logos, or testimonials.
- Meet WCAG AA contrast, 4.5:1 for body text.
- Show a visible focus state on every interactive element.
- Respect `prefers-reduced-motion`.

Don't:
- Use Inter, Roboto, Arial, or a system font as the display face.
- Use a purple gradient on white.
- Default to a centered hero plus a 3-column feature-card grid.
- Default to a cream or off-white background, italic accent words in headlines, numbered "01/02/03" section labels, monospace labels, or pill-shaped buttons.
- Ship a generic nav or footer copied from a template.
- Re-draw browser, phone, or code-window chrome.
- Use colour alone to carry meaning.
- Add a raw hex, px, or font value outside the token source.
- Rebuild a component the Components section already names.
- <project-specific rule>

## Motion
- Durations: <value per speed, e.g. fast/base/slow>
- Easing: <curve name or values>
- Prefer one orchestrated entrance over scattered micro-interactions.
- Respect `prefers-reduced-motion`: disable or shorten non-essential motion.

## Accessibility
- Contrast floor: <value, e.g. 4.5:1 body, 3:1 large text>
- Focus style: <visible outline spec>
- Minimum target size: <value, e.g. 44x44px>
- Never use colour alone to convey state or meaning.

## Source of truth
Token source: <path to the code token file, or "none yet">
- <file> generates <what, e.g. CSS variables, Tailwind config>
- Rule: this file governs. Code implements it. A visual change updates this file in the same change.

## Known inconsistencies
<off-scale values found in code, listed as debt. Do not copy them.>
