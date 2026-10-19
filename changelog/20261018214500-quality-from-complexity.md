# Pick quality tooling by the dominant complexity

- `rules/builder.md`: name the dominant complexity (domain, scale or accidental) before picking quality tooling, with one approach per type.
- `rules/testing.md`: make invalid states unrepresentable where possible, and still test valid error outcomes through the public interface.
- `rules/builder.md`: merged two overlapping stack bullets and removed the rationale bullet under Related rules.
- Why: Will Larson's "How to create software quality" shows that a quality playbook works only in the context it came from. A rollout strategy that fits a high-traffic app does little for a low-traffic, domain-heavy one.
