# Client Layout Template — GA4 Consent Management

This is the template for the cookie consent client component.

Replace all `{PLACEHOLDER}` values with user-provided parameters from Step 0.

## Full Component Template

```tsx
"use client"

import { useEffect } from "react"

export default function CookieConsent() {
  useEffect(() => {
    try {
      window.silktideCookieBannerManager.updateCookieBannerConfig({
        background: {
          showBackground: true,
        },
        cookieIcon: {
          position: "bottomLeft",
        },
        cookieTypes: [
          {
            id: "necessary",
            name: "Necessary",
            description:
              "<p>{NECESSARY_DESCRIPTION}</p>",
            required: true,
            onAccept: function () {},
          },
          {
            id: "analytics",
            name: "Analytics",
            description:
              "<p>{ANALYTICS_DESCRIPTION}</p>",
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
              "<p>{ADVERTISING_DESCRIPTION}</p>",
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
          banner: {
            description:
              "<p>{BANNER_DESCRIPTION}</p>",
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
              "<p>{PREFERENCES_DESCRIPTION}</p>",
            creditLinkText: "Get this banner for free",
            creditLinkAccessibleLabel: "Get this banner for free",
          },
        },
      })
    } catch (error) {
      console.error("Error loading Silktide Consent Manager", error)
    }
  }, [])

  return null
}
```

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
import CookieConsent from "./_components/CookieConsent"

// Inside <body>:
<CookieConsent />
```

Place it near the top of `<body>` so the consent manager initializes early.

## Without Advertising Category

If the user does not want the advertising consent category, remove the entire `{ id: "advertising", ... }` block from the `cookieTypes` array.
