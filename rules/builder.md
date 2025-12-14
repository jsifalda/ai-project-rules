---
type: "manual"
---

## New Applications

**Goal:** Autonomously implement and deliver a visually appealing, substantially complete, and functional prototype. Utilize all tools at your disposal to implement the application.

1. **Understand Requirements:** Analyze the user's request to identify core features, desired user experience (UX), visual aesthetic, application type/platform (web, mobile, desktop, CLI, library, 2D or 3D game), and explicit constraints. If critical information for initial planning is missing or ambiguous, ask concise, targeted clarification questions.
2. **Propose Plan:** Formulate an internal development plan. Present a clear, concise, high-level summary to the user. This summary must effectively convey the application's type and core purpose, key technologies to be used, main features and how users will interact with them, and the general approach to the visual design and user experience (UX) with the intention of delivering something beautiful, modern, and polished, especially for UI-based applications. Ensure this information is presented in a structured and easily digestible manner.

- When key technologies aren't specified, prefer the following:
- reactjs
- typescript
- shadcn ui components with tailwind css
- lucide lib for react-compatible icons
- microsoft clarity for analytics
- nextjs as server (hosted on vercel)
- SWR lib for data fetching with nextjs, otherwise native “fetch” method
- nextauth.js for authentication (only with nextjs, otherwise auth.js)
- sentry for error tracking
- jest for unit testing, together with playwright for integration tests (alternative nodejs tests runner for api/server tests)
- eslint for static linting
- husky precommit hooks (for linting etc)
- Tauri if multi-platform/hybrid apps are needed (eg. mobile & desktop apps)
- silktide consent manager for cookies banner

3. **User Approval:** Obtain user approval for the proposed plan.
4. **Implementation:** Autonomously implement each feature and design element per the approved plan utilizing all available tools. When starting ensure you scaffold the application. Aim for full scope completion.
5. **Verify:** Review work against the original request, the approved plan. Fix bugs, deviations, and all placeholders where feasible, or ensure placeholders are visually adequate for a prototype. Ensure styling, interactions, produce a high-quality, functional and beautiful prototype aligned with design goals. Finally, but MOST importantly, build the application and ensure there are no compile errors.
6. **Solicit Feedback:** If still applicable, provide instructions on how to start the application and request user feedback on the prototype.
