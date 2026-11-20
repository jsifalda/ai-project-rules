# Port statechart skill

- Added the `statechart` skill, adapted from the MIT-licensed upstream pstack skill, with its license file.
- Rewrote it as instructions only: the agent explores the states itself, because the upstream checker needs Java, which this setup does not allow.
- Removed every link to the upstream renderer and docs, and added a page template so the skill publishes the chart and report as an Artifact.
