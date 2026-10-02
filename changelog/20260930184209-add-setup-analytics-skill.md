# Add setup-analytics skill

- Added `setup-analytics`, which creates a Microsoft Clarity project and a GA4 property in the user's logged-in Chrome through the claude-in-chrome extension, then installs both tags.
- Next.js projects hand off to `microsoft-clarity` and `nextjs-ga-tracking`. Other stacks get a head snippet with an inline consent banner.
- README Skills row added.
- Why: adding analytics to a new project took two manual console sessions plus copying IDs by hand.
