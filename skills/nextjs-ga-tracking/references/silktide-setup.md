# Silktide Consent Manager Setup

## What is Silktide?

Silktide Consent Manager is a free, open-source, self-hosted cookie consent solution.

It consists of two static files that you host yourself — no external dependencies or CDN required.

## How to Get the Files

**Preferred: Use the bundled assets from this skill:**

```bash
cp <path-to-this-skill>/assets/csm.js <project>/public/csm.js
cp <path-to-this-skill>/assets/csm.css <project>/public/csm.css
```

**Alternative: Download the latest version from GitHub:**

The official repository is [github.com/silktide/consent-manager](https://github.com/silktide/consent-manager).

The files are named `silktide-consent-manager.js` and `silktide-consent-manager.css` in the repo. Rename them to `csm.js` and `csm.css` when placing in your project.

## File Placement

Place both files in the project's `public/` directory:

```
public/
├── csm.js      # ~54KB, the consent manager JavaScript
└── csm.css     # ~12KB, the consent manager styles
```

## Integration in Next.js

**Do NOT add raw `<script>` or `<link>` tags to the layout.** In Next.js App Router, raw tags in the layout may not render as expected (stylesheets get converted to preloads, scripts create race conditions).

Instead, the CookieConsent client component handles loading both files internally:
- CSS via `<link rel="stylesheet" href="/csm.css" />` in the component's JSX
- JS via `next/script` with `strategy="afterInteractive"` and `onLoad` callback

See `client-layout-template.md` for the full component template.

## Important Notes

- The files are **vendored** (self-hosted). There is no npm package for Silktide.
- The `csm.js` script exposes `window.silktideConsentManager` globally with these methods:
  - `init(config)` — Initialize with a configuration object
  - `update(config)` — Deep-merge new config into existing and re-initialize
  - `getInstance()` — Get the current consent manager instance
  - `resetConsent()` — Clear all consent choices and show the prompt again
- Configuration is done via JavaScript (see `client-layout-template.md`), not via HTML attributes.
- The config requires a `consentTypes` array (each with `id`, `name`, `description`, and optional `onAccept`/`onReject` callbacks).
- Text customization uses `text.prompt.*` for the banner and `text.preferences.*` for the preferences dialog.

## Updating Silktide

To update, download the latest `silktide-consent-manager.js` and `silktide-consent-manager.css` from [github.com/silktide/consent-manager](https://github.com/silktide/consent-manager) and replace `public/csm.js` and `public/csm.css`.

**Note:** Check the GitHub repo for any API changes when updating. The API was significantly changed between earlier versions (which used `silktideCookieBannerManager.updateCookieBannerConfig()`) and the current version (which uses `silktideConsentManager.init()`).
