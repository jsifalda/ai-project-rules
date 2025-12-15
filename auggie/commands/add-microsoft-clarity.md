---
description: Implement Microsoft Clarity tracking in Next.js application.
---

IMPORTANT: Before proceeding, ask the user for their Microsoft Clarity project ID. Do not continue or use placeholder values until the user provides the actual ID.

Once the user provides the Clarity project ID:

1. Install the `react-microsoft-clarity` package using the project's package manager
2. Create a new client component at `src/components/MicrosoftClarity.tsx` with:
   - 'use client' directive at the top
   - Import `clarity` from `react-microsoft-clarity`
   - Initialize Clarity inside a `useEffect` hook with the provided project ID
   - Return `null` (no DOM output)
3. Import and add the `<MicrosoftClarity />` component to the root layout (`src/app/layout.tsx`) inside the `<body>` tag, before `{children}`

Requirements:
- Must only run on the client side (not during SSR)
- Must be compatible with React 19 and Next.js App Router
- Minimal and non-intrusive implementation


$ARGUMENTS