# SVG Patterns Reference

Reusable SVG building blocks. Pick and combine as needed.

## Dimensions by Image Type

| Type | viewBox | Use case |
|------|---------|----------|
| Banner / OG image | `0 0 1200 630` | Social sharing, sponsor cards, blog headers |
| Card | `0 0 800 400` | Thumbnails, preview cards |
| Hero | `0 0 1440 800` | Full-width hero sections |
| Square | `0 0 600 600` | Social avatars, app icons |
| Badge | `0 0 200 60` | Status badges, labels |

## Backgrounds

### Dark gradient (modern SaaS)
```xml
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#0f172a"/>
    <stop offset="100%" stop-color="#1e293b"/>
  </linearGradient>
</defs>
<rect width="W" height="H" fill="url(#bg)"/>
```

### Light gradient (clean, editorial)
```xml
<rect width="W" height="H" fill="#fafafa"/>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#f1f5f9"/>
  </linearGradient>
</defs>
<rect width="W" height="H" fill="url(#bg)"/>
```

### Vibrant gradient
```xml
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#7c3aed"/>
    <stop offset="100%" stop-color="#2563eb"/>
  </linearGradient>
</defs>
<rect width="W" height="H" fill="url(#bg)"/>
```

## Decorative Elements

### Floating circles (depth / atmosphere)
```xml
<circle cx="X" cy="Y" r="R" fill="#6366f1" opacity="0.06"/>
```
Place 2–3 at varying positions and sizes. Keep opacity between 0.03–0.08.

### Accent bar (left-side emphasis)
```xml
<rect x="80" y="200" width="5" height="120" rx="2.5" fill="url(#accent)"/>
```

### Dot grid (tech/data feel)
```xml
<pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse">
  <circle cx="15" cy="15" r="1.5" fill="#ffffff" opacity="0.1"/>
</pattern>
<rect width="W" height="H" fill="url(#dots)"/>
```

### Wave line (signal/flow feel)
```xml
<path d="M0 40 Q20 0 40 40 Q60 80 80 40" fill="none" stroke="#818cf8" stroke-width="3" stroke-linecap="round"/>
```

## Typography

Always use system font stack for maximum portability:
```
font-family="system-ui, -apple-system, 'Segoe UI', sans-serif"
```

### Title (large, prominent)
```xml
<text x="X" y="Y" font-family="system-ui, -apple-system, 'Segoe UI', sans-serif"
      font-size="64" font-weight="700" fill="#f8fafc" letter-spacing="-1">
  Title Text
</text>
```

### Subtitle / tagline
```xml
<text x="X" y="Y" font-family="system-ui, -apple-system, 'Segoe UI', sans-serif"
      font-size="24" fill="#94a3b8" letter-spacing="0.5">
  Tagline text
</text>
```

### Badge / label
```xml
<rect x="X" y="Y" width="W" height="36" rx="18" fill="#6366f1" opacity="0.15"/>
<text x="X+20" y="Y+24" font-family="system-ui, -apple-system, 'Segoe UI', sans-serif"
      font-size="14" fill="#a5b4fc" font-weight="600" letter-spacing="1.5">
  LABEL TEXT
</text>
```

### Stat block (number + label)
```xml
<g transform="translate(X, Y)">
  <text x="0" y="0" font-size="32" font-weight="700" fill="#818cf8">42k+</text>
  <text x="0" y="24" font-size="13" fill="#64748b">metric label</text>
</g>
```

## Color Palettes

### Dark mode (indigo accent)
- Background: `#0f172a` → `#1e293b`
- Title: `#f8fafc`
- Subtitle: `#94a3b8`
- Accent: `#6366f1` / `#818cf8`
- Muted: `#64748b`

### Dark mode (emerald accent)
- Background: `#022c22` → `#064e3b`
- Title: `#f0fdf4`
- Subtitle: `#86efac`
- Accent: `#10b981` / `#34d399`

### Dark mode (amber accent)
- Background: `#1c1917` → `#292524`
- Title: `#fef3c7`
- Subtitle: `#d97706`
- Accent: `#f59e0b` / `#fbbf24`

### Light mode (blue accent)
- Background: `#ffffff` → `#f1f5f9`
- Title: `#0f172a`
- Subtitle: `#475569`
- Accent: `#2563eb` / `#3b82f6`

## Layout Patterns

### Left-aligned content (banner)
```
┌────────────────────────────────┐
│                        ○  ○   │  ← decorative circles
│  ▌ Title                      │  ← accent bar + title
│    Tagline line 1             │
│    Tagline line 2             │
│    [BADGE]                    │
│                               │
│    42k+    <15m    94%        │  ← stat blocks
│    label   label   label      │
│         signalseek.cc         │  ← URL footer
└────────────────────────────────┘
```

### Centered content (card/hero)
```
┌────────────────────────────────┐
│                               │
│          Title                │
│       Tagline text            │
│                               │
│    [stat]  [stat]  [stat]     │
│                               │
│         domain.com            │
└────────────────────────────────┘
```

### Minimal (badge/icon)
```
┌──────────────┐
│  Icon + Text │
└──────────────┘
```
