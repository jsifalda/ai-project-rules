---
name: nextjs-ga-tracking
description: Implements Google Analytics 4 tracking with GDPR-compliant Silktide cookie consent in Next.js projects. Use when the user wants to add GA tracking, implement Google Analytics, set up analytics with cookie consent, or add GDPR-compliant tracking to a Next.js app.
---

# GA4 + Silktide Cookie Consent for Next.js

## Overview

This skill adds Google Analytics 4 (GA4) tracking to a Next.js project with GDPR-compliant cookie consent via Silktide Cookie Banner Manager.

It covers:
- GA4 integration using `@next/third-parties/google`
- Silktide cookie consent banner with gtag consent mode
- Three consent categories: Necessary, Analytics, Advertising
- TypeScript type declarations for global window objects

## Step 0: Gather Required Parameters

**CRITICAL: Ask the user for these parameters BEFORE making any code changes.**

### Required parameters (MUST ask):

1. **GA4 Measurement ID** — format: `G-XXXXXXXXXX` (found in Google Analytics > Admin > Data Streams)
2. **Cookie banner description** — the main text shown on the consent banner (e.g. "We use cookies on our site to enhance your experience, provide personalized content, and analyze our traffic.")

### Optional parameters (ask, but provide defaults if user skips):

3. **Cookie type descriptions** (defaults below):
   - Necessary: "These cookies are necessary for the website to function properly and cannot be switched off."
   - Analytics: "These cookies help us improve the site by tracking which pages are most popular and how visitors move around the site."
   - Advertising: "These cookies provide extra features and personalization to improve your experience. They may be set by us or by partners whose services we use."
4. **Button labels** (defaults below):
   - Accept all: "Accept all"
   - Reject non-essential: "Reject non-essential"
   - Preferences: "Preferences"
5. **Preferences dialog** (defaults below):
   - Title: "Customize your cookie preferences"
   - Description: "We respect your right to privacy. You can choose not to allow some types of cookies. Your cookie preferences will apply across our website."
6. **Include advertising consent category?** (default: yes)

## Step 1: Install dependency

```bash
# Using yarn (preferred if yarn.lock exists):
yarn add @next/third-parties

# Using npm (if package-lock.json exists):
npm install @next/third-parties
```

Check which package manager the project uses by looking for `yarn.lock` or `package-lock.json`.

## Step 2: Add GoogleAnalytics component to root layout

Edit `src/app/layout.tsx` (or `app/layout.tsx` depending on project structure).

### Add import at the top:

```tsx
import { GoogleAnalytics } from "@next/third-parties/google"
```

### Add component inside `<body>`, typically at the end:

```tsx
<GoogleAnalytics gaId="{USER_GA_ID}" />
```

Replace `{USER_GA_ID}` with the user's GA4 Measurement ID.

## Step 3: Add Silktide Cookie Manager files

Copy the bundled assets from this skill into the project's `public/` directory:

```bash
cp <path-to-this-skill>/assets/csm.js <project>/public/csm.js
cp <path-to-this-skill>/assets/csm.css <project>/public/csm.css
```

The asset files are located in the `assets/` directory of this skill.

See `references/silktide-setup.md` for more details about Silktide.

## Step 4: Add Silktide assets to layout

In the root layout (`src/app/layout.tsx` or `app/layout.tsx`):

### Inside `<head>`:

```tsx
<link rel="stylesheet" href="csm.css" />
```

### At the end of `<body>`:

```tsx
<script src="csm.js" async></script>
```

## Step 5: Create ClientLayout component with consent management

See `references/client-layout-template.md` for the full template.

Summary:
1. Create a `"use client"` component (e.g. `src/app/_components/CookieConsent.tsx`)
2. Implement Silktide consent config with gtag consent calls
3. Use all user-provided wordings from Step 0
4. Import and render in the root layout inside `<body>`

## Step 6: Add TypeScript declarations

Create or update `src/types/global.d.ts` (or a similar declarations file):

```typescript
declare global {
  interface Window {
    gtag: (...args: unknown[]) => void
    dataLayer: Record<string, unknown>[]
    silktideCookieBannerManager: {
      updateCookieBannerConfig: (config: Record<string, unknown>) => void
    }
  }
}

export {}
```

If the project already has a global declarations file, append to it rather than creating a new one.

## Step 7: Verify

Run the project's build command to ensure no errors:

```bash
yarn build
# or
npm run build
```

Check that:
- Build succeeds with zero errors
- No TypeScript type errors related to `window.gtag` or `window.dataLayer`
- The GA script loads in the browser (check Network tab for `gtag/js`)
- The cookie banner appears on page load

## Common Issues

### "window is not defined" error
The consent management code MUST run in a `"use client"` component, wrapped in a `useEffect` hook. Never access `window` at module scope or in server components.

### GA not sending data
Check that:
1. The GA4 Measurement ID format is correct (`G-XXXXXXXXXX`)
2. The consent banner grants `analytics_storage: "granted"` when accepted
3. Ad blockers are not blocking the gtag.js script

### Silktide banner not appearing
Check that:
1. `csm.js` and `csm.css` are in `public/` directory
2. The `<script>` and `<link>` tags reference the correct paths
3. `updateCookieBannerConfig` is called after the script loads (use `useEffect`)

### TypeScript errors with window.gtag
Ensure the global type declarations file is included in `tsconfig.json`'s `include` array. Usually `src/**/*.ts` covers it.
