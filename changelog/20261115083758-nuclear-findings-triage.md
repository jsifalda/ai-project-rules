# Route nuclear structural findings through the shared triage

- `setup-aiengineering` 1.7: the Nuclear structural review lens no longer skips the triage step. A relevant finding inside the session's changed code is fixed after the defect findings. A broad rewrite, a new dependency or a public-interface change still goes to the user.
- Why: the exemption sent every structural finding to the user, also the small in-scope ones. The "Bigger than the change under review" verdict already guards large rewrites.
- Forward-only per the baseline-checklist maintainer loop: new setups get it, no checklist version bump.
