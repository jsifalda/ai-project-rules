# Silktide Cookie Banner Manager Setup

## What is Silktide?

Silktide Cookie Banner Manager is a free, self-hosted cookie consent solution.

It consists of two static files that you host yourself — no external dependencies or CDN required.

## How to Get the Files

**Preferred: Use the bundled assets from this skill:**

```bash
cp <path-to-this-skill>/assets/csm.js <project>/public/csm.js
cp <path-to-this-skill>/assets/csm.css <project>/public/csm.css
```

**Alternative: Download fresh versions:**

1. Visit [Silktide Consent Manager](https://silktide.com/tools/cookie-consent/consent-manager/)
2. Download the latest `csm.js` and `csm.css` files

## File Placement

Place both files in the project's `public/` directory:

```
public/
├── csm.js      # ~32KB, the consent banner JavaScript
└── csm.css     # ~15KB, the consent banner styles
```

## Integration in Next.js Layout

Add these two references to your root layout (`src/app/layout.tsx` or `app/layout.tsx`):

### In `<head>`:

```tsx
<link rel="stylesheet" href="csm.css" />
```

### At the end of `<body>`:

```tsx
<script src="csm.js" async></script>
```

## Important Notes

- The files are **vendored** (self-hosted). There is no npm package for Silktide.
- The `async` attribute on the script tag is important — it prevents blocking page load.
- The CSS file should be in `<head>` to avoid flash of unstyled banner.
- The `csm.js` script exposes `window.silktideCookieBannerManager` globally.
- Configuration is done via JavaScript (see `client-layout-template.md`), not via HTML attributes.
- If the project uses ESLint with `@next/next/no-css-tags` rule, you may need to disable it for the layout file with `/* eslint-disable @next/next/no-css-tags */`.

## Updating Silktide

To update, simply replace `public/csm.js` and `public/csm.css` with newer versions from the Silktide website.

No configuration changes are needed — the JavaScript API is stable.
