# Fix check-universality.sh directory-arg crash

- The universality scanner now accepts directory arguments (recurses into them), not just individual files.
- Passing a directory previously left the file list empty and crashed with `files[@]: unbound variable` under `set -u` on bash 3.2 (macOS default). Added an empty-array guard so empty/nonexistent input reports clean instead of crashing.
- Why: the `create-skill` skill documents `bash scripts/check-universality.sh skills/<your-skill>/`, but that directory form was broken on macOS. Now the documented form works.
- Pre-commit hook unaffected (it passes explicit, non-empty file lists).
