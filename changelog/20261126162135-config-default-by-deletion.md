# Delete a config key to reach its default

- `rules/coding.md` now says to delete a config key, env var or flag to reach its default, and to pin the default value only when another layer overrides it.
- Why: a user correction. Setting a key to its default value adds config that does nothing, and removing the key gives the same behavior.
