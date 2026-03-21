# Client Layout Template — GA4 Consent Management

This is the template for the cookie consent client component.

Replace all `{PLACEHOLDER}` values with user-provided parameters from Step 0.

## Full Component Template

```tsx
"use client"

import { useCallback } from "react"
import Script from "next/script"

export function CookieConsent() {
  const handleScriptLoad = useCallback(() => {
    try {
      window.silktideConsentManager.init({
        icon: {
          position: "bottomLeft",
        },
        consentTypes: [
          {
            id: "necessary",
            name: "Necessary",
            description:
              "{NECESSARY_DESCRIPTION}",
            required: true,
            onAccept: function () {},
          },
          {
            id: "analytics",
            name: "Analytics",
            description:
              "{ANALYTICS_DESCRIPTION}",
            defaultValue: true,
            onAccept: function () {
              if (typeof window.gtag === "function") {
                window.gtag("consent", "update", {
                  analytics_storage: "granted",
                })
              }
              if (typeof window.dataLayer !== "undefined") {
                window.dataLayer.push({
                  event: "consent_accepted_analytics",
                })
              }
            },
            onReject: function () {
              if (typeof window.gtag === "function") {
                window.gtag("consent", "update", {
                  analytics_storage: "denied",
                })
              }
            },
          },
          // CONDITIONAL: Only include this block if user wants advertising consent
          {
            id: "advertising",
            name: "Advertising",
            description:
              "{ADVERTISING_DESCRIPTION}",
            onAccept: function () {
              if (typeof window.gtag === "function") {
                window.gtag("consent", "update", {
                  ad_storage: "granted",
                  ad_user_data: "granted",
                  ad_personalization: "granted",
                })
              }
              if (typeof window.dataLayer !== "undefined") {
                window.dataLayer.push({
                  event: "consent_accepted_advertising",
                })
              }
            },
            onReject: function () {
              if (typeof window.gtag === "function") {
                window.gtag("consent", "update", {
                  ad_storage: "denied",
                  ad_user_data: "denied",
                  ad_personalization: "denied",
                })
              }
            },
          },
        ],
        text: {
          prompt: {
            description:
              "{BANNER_DESCRIPTION}",
            acceptAllButtonText: "{ACCEPT_ALL_TEXT}",
            acceptAllButtonAccessibleLabel: "{ACCEPT_ALL_TEXT}",
            rejectNonEssentialButtonText: "{REJECT_TEXT}",
            rejectNonEssentialButtonAccessibleLabel: "{REJECT_TEXT}",
            preferencesButtonText: "{PREFERENCES_TEXT}",
            preferencesButtonAccessibleLabel: "Toggle preferences",
          },
          preferences: {
            title: "{PREFERENCES_TITLE}",
            description:
              "{PREFERENCES_DESCRIPTION}",
            creditLinkText: "Get this banner for free",
            creditLinkAccessibleLabel: "Get this banner for free",
          },
        },
      })
    } catch (error) {
      console.error("Error loading Silktide Consent Manager", error)
    }
  }, [])

  return (
    <>
      <link rel="stylesheet" href="/csm.css" />
      <Script
        src="/csm.js"
        strategy="afterInteractive"
        onLoad={handleScriptLoad}
      />
    </>
  )
}
```

## Key Design Decisions

### Why `next/script` with `onLoad` instead of `useEffect`?

The `csm.js` script loads asynchronously. If you use `useEffect`, it fires on component mount — before the script has loaded. This causes `Cannot read properties of undefined (reading 'init')` because `window.silktideConsentManager` doesn't exist yet.

Using `next/script` with `onLoad` guarantees the callback only fires after the script has fully loaded and executed, so `window.silktideConsentManager` is available.

### Why does the component render `<link>` and `<Script>` instead of returning `null`?

In Next.js App Router, raw `<link rel="stylesheet">` tags added to the layout's `<head>` may be converted to `<link rel="preload">` — meaning the CSS is never applied as a stylesheet. By including the `<link>` in the client component's return, it renders correctly in the document.

## Placeholders Reference

| Placeholder | Step 0 Parameter | Default |
|---|---|---|
| `{NECESSARY_DESCRIPTION}` | Necessary cookies description | "These cookies are necessary for the website to function properly and cannot be switched off." |
| `{ANALYTICS_DESCRIPTION}` | Analytics cookies description | "These cookies help us improve the site by tracking which pages are most popular and how visitors move around the site." |
| `{ADVERTISING_DESCRIPTION}` | Advertising cookies description | "These cookies provide extra features and personalization to improve your experience. They may be set by us or by partners whose services we use." |
| `{BANNER_DESCRIPTION}` | Cookie banner description | (no default — user must provide) |
| `{ACCEPT_ALL_TEXT}` | Accept all button label | "Accept all" |
| `{REJECT_TEXT}` | Reject button label | "Reject non-essential" |
| `{PREFERENCES_TEXT}` | Preferences button label | "Preferences" |
| `{PREFERENCES_TITLE}` | Preferences dialog title | "Customize your cookie preferences" |
| `{PREFERENCES_DESCRIPTION}` | Preferences dialog description | "We respect your right to privacy. You can choose not to allow some types of cookies. Your cookie preferences will apply across our website." |

## Usage in Root Layout

```tsx
import { CookieConsent } from "@/components/CookieConsent"

// Inside <body>:
<CookieConsent />
```

Place it near the top of `<body>` so the consent manager initializes early.

## Without Advertising Category

If the user does not want the advertising consent category, remove the entire `{ id: "advertising", ... }` block from the `consentTypes` array.
