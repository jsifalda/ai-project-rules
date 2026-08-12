# Add an opt-in skill-discovery module to `setup-aiengineering`

- New Step 6c offers to search the public skills registry for skills that fit the target repo, and
  delegates to `find-skills` once per topic the user picks.
- Opt-in, default off. Every other module writes the project's own policy into the project's own
  repo. This one reaches the public internet and lands third-party code, so it must be chosen
  deliberately.
- `setup-aiengineering` infers the search topics, because `find-skills` takes a topic query and has
  no codebase-scan mode. Topics come from the dependency manifest, the Step 2 stack detection, and
  the repo's stated purpose — each shown with the signal that produced it.
- Approval, security review, and transport failures stay with `find-skills`. This skill supplies
  topics, never consent. Step 6c deliberately does not pre-flight the network, so `find-skills` can
  offer its own approval-gated fallback.
- Baseline checklist gains the concern at `Since: v11`; skill version bumped v10 → v11, so a re-run
  offers the module to repos stamped at v10.
- `find-skills` itself is unchanged — it is synced from upstream, so local divergence costs more
  than it buys.
