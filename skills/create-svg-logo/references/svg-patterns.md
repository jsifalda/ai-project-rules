# Design Patterns & Examples

Reusable starting points for the four most common logo constructions. Adapt shapes, colors, and text — do not ship them unchanged.

## Wordmark Logo

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 80">
  <defs>
    <style>
      .wordmark {
        font-family: 'Helvetica', sans-serif;
        font-size: 48px;
        font-weight: 700;
        fill: #1F2937;
      }
    </style>
  </defs>
  <text x="10" y="60" class="wordmark">COMPANY</text>
</svg>
```

## Geometric Icon

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4F46E5" />
      <stop offset="100%" style="stop-color:#7C3AED" />
    </linearGradient>
  </defs>

  <!-- Hexagon shape -->
  <polygon
    points="50,5 95,27.5 95,72.5 50,95 5,72.5 5,27.5"
    fill="url(#grad)"
    stroke="#312E81"
    stroke-width="2"
  />

  <!-- Inner element -->
  <circle cx="50" cy="50" r="20" fill="#FFFFFF" />
</svg>
```

## Abstract Mark

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <!-- Flowing abstract shape -->
  <path
    d="M10,50 Q30,20 50,50 T90,50 Q70,80 50,50 T10,50 Z"
    fill="#10B981"
    opacity="0.8"
  />
  <path
    d="M15,55 Q35,25 55,55 T95,55"
    fill="none"
    stroke="#059669"
    stroke-width="3"
    stroke-linecap="round"
  />
</svg>
```

## Combination Mark

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80">
  <!-- Icon -->
  <g id="icon">
    <circle cx="40" cy="40" r="30" fill="#4F46E5" />
    <path d="M30,35 L35,45 L50,25" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  </g>

  <!-- Text -->
  <g id="text">
    <text x="85" y="45" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#1F2937">
      COMPANY
    </text>
  </g>
</svg>
```
