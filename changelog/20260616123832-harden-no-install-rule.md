# Tighten the no-install rule in general.md

- Broadened the RESTRICTIONS install ban: now forbids installing any package, library, tool, or binary anywhere (global, `--user`, venv, one-off) for any purpose — explicitly closing the "it's just `--user` / just this once" loophole.
- Added a "prefer no-install paths first" bullet (use already-available tools, e.g. native `Read` reads PDFs) before the ask-first step.
- Renamed the ask-first protocol from "required binaries" to "any required package, library, or binary," added a one-off-library example, and made explicit that on the user's approval the agent runs that one install command.
- Updated the Dependency Management bullet to match (no global/`--user`/one-off installs).
- Why: an agent installed `pypdf` via `pip install --user` despite the rule being present and loaded. Root cause was a soft-enforcement failure — rule buried, loophole open, ask-first framed around binaries not libraries. This hardens the prose layer (no hook, per user's choice).
