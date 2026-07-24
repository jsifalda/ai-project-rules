# Fix Copilot skill-load failure and harden validation guidance

- Fixed `setup-notifications` frontmatter: a `": "` (colon+space) inside the `description` (`(optionally: also ...)`) terminated the YAML plain scalar, so Copilot CLI's strict parser rejected the skill at load time. Changed it to a comma.
- Renamed three skills' `name:` fields to hyphen-case to match their directories: `markdown`, `summarise-text`, `translate-to-czech`. They were flagged by the repo validator and are invoked by directory name, so behavior is unchanged.
- Why: the whole repo now passes `quick_validate.py` (was 4 of 70 invalid), and the reported Copilot load error is gone.
- Hardened guidance in `create-skill/SKILL.md` and the repo `CLAUDE.md`: validate after editing an existing skill too, not just when adding one, because the pre-commit hook is per-clone and `--no-verify`-bypassable. The bad edit had slipped through exactly that gap.
