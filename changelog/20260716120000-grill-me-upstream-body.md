# Adopt upstream grilling body in grill-me

- Replaced the `grill-me` skill body with the upstream `mattpocock/skills` `productivity/grilling` content, keeping the local skill name and description triggers.
- Upstream adds three things the local version lacked: ask one question at a time and wait for the answer, separate facts (look them up) from decisions (always ask the user), and don't act until the user confirms shared understanding.
- Kept the `grill-me` name deliberately — `better-plan` and `prd-creator` both depend on it by name, so a rename to `grilling` would break them.
- Not tracked by `sync-mattpocock-skills`: that script keys the local directory off the upstream skill name and has no rename mapping, so this copy is a manual fork. A future `sync.sh grilling` would create a separate `skills/grilling/` rather than refresh this one.
