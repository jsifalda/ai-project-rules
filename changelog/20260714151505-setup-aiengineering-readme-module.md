# Add a project-README module to setup-aiengineering

- New Step 8 scaffolds a root `README.md` with a confirmed goal statement and a `## Documentation`
  index linking the doc systems that actually landed (ADRs, `ARCHITECTURE.md`, changelog, scenarios).
  Runs after delegation so the index reflects reality, not the module menu.
- Why: `file-organization.md` already told agents to link new docs from "README.md's documentation
  section" — a section nothing ever created. The rule pointed at nothing.
- New `references/readme-guide.md` owns goal capture (infer from the repo, propose, confirm), the
  scaffold template, and a merge-not-clobber algorithm for repos that already have a README.
- Amended two injected blocks so the README stays current: file organization now names
  `## Documentation` and fires on docs-only changes (the verification protocol is exempt for those,
  so an ADR-only session would never have linked its own ADR); the docs-alignment gate now checks the
  goal statement and index against the implementation.
- Baseline checklist bumped to v3. Added a `(revised vN)` convention — `Since` could only express
  "new concern", so an amended block had no way to reach older repos deterministically.
- The module owns `## Documentation` only. `## PRDs` (`prd-creator`) and `## Codebase Guide`
  (`create-codebase-docs`) stay untouched, so no other skill needed changing.
- Guide validated by four blind agent passes against scratch fixtures, fixing defects that would have
  duplicated links, asked questions whose answers could not change the output, and left a stale README
  unfixed.
