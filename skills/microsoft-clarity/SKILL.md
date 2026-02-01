---
name: microsoft-clarity
description: Implement Microsoft Clarity analytics tracking in Next.js applications. Use when user wants to add Microsoft Clarity, set up heatmaps and session recordings, add analytics tracking to a Next.js app, or integrate Clarity for user behavior insights.
---

# Microsoft Clarity

Add Microsoft Clarity tracking to a Next.js application with App Router.

## Prerequisites

**Obtain the Clarity Project ID from the user before proceeding.** Do not use placeholder values.

## Implementation Steps

1. **Install the package** using the project's package manager:
   ```bash
   npm install react-microsoft-clarity
   # or: yarn add react-microsoft-clarity
   # or: pnpm add react-microsoft-clarity
   ```

2. **Create the client component** at `src/components/MicrosoftClarity.tsx`:
   ```tsx
   'use client';

   import { useEffect } from 'react';
   import { clarity } from 'react-microsoft-clarity';

   export function MicrosoftClarity() {
     useEffect(() => {
       clarity.init('PROJECT_ID'); // Replace with actual project ID
     }, []);

     return null;
   }
   ```

3. **Add to root layout** (`src/app/layout.tsx`):
   ```tsx
   import { MicrosoftClarity } from '@/components/MicrosoftClarity';

   export default function RootLayout({ children }) {
     return (
       <html lang="en">
         <body>
           <MicrosoftClarity />
           {children}
         </body>
       </html>
     );
   }
   ```

## Requirements

- Must only run on the client side (not during SSR)
- Must be compatible with React 19 and Next.js App Router
- Minimal and non-intrusive implementation
