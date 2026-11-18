# Pin test clocks in the past and tighten rule lines

- Added a testing rule: pin a fake clock to a fixed date years before today.
- Why: a fake clock near today hid a leak to the real clock until a 30-day TTL passed. A clock in the future hides it for ever.
- Rewrote the coding and testing lines that the prompt audit flagged into one-rule lines with no rationale. The rules stay the same, except the TDD commit step now defers to the repo or user commit policy.
