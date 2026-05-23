# Fix template-bias bugs in user-scenarios-setup skill

- Step 3 no longer hardcodes `AUTH`/`BILLING` example titles — uses a domain-agnostic placeholder so seeded scenarios match whatever domains the user picked in Step 2.
- Step 5 confirmation message now echoes the user's actual domain list instead of the hardcoded `AUTH, BILLING, ADMIN`.
- Both fixes align Steps 3 and 5 with the skill's own rule: "Never invent product- or domain-specific scenario copy."
