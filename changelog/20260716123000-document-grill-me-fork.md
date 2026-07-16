# Document the grill-me fork in sync-mattpocock-skills

- Added a "Forked skills" section to `sync-mattpocock-skills` recording that local `grill-me` carries the upstream `productivity/grilling` body under a deliberately different name.
- Why: the sync script derives the local directory from the upstream name and has no rename map, so `sync.sh grilling` would create a duplicate `skills/grilling/` instead of refreshing the fork — and no skip warning fires, because the differing names never collide. That trap was undocumented.
- Documented the hand-refresh procedure and noted a rename map in `scripts/sync.sh` as the durable fix if upstream starts changing often.
- Dropped `grill-me` as the native-collision example in step 3; it can never collide, so it was a misleading illustration.
