# Source playbooks

The why skill plans its sources per question, then spawns one investigator per chosen source. The playbooks below are examples for common tools, not a closed set. Adapt one for a different tool of the same kind.

| Source | Playbook | Example tool it documents |
|---|---|---|
| Source control history | [`code-archaeology.md`](./sources/code-archaeology.md) | git, `gh`, `glab` |
| Issue / ticket tracker | [`linear.md`](./sources/linear.md) | Linear (adapt for Jira, GitHub Issues, Plane, Shortcut) |
| Long-form documents | [`notion.md`](./sources/notion.md) | Notion (adapt for Confluence, Google Docs, Coda) |
| Real-time team chat | [`slack.md`](./sources/slack.md) | Slack (adapt for Discord, Microsoft Teams, Mattermost) |
| Infrastructure observability | [`datadog.md`](./sources/datadog.md) | Datadog (adapt for New Relic, Honeycomb, Grafana, Splunk) |
| Error / exception tracking | [`sentry.md`](./sources/sentry.md) | Sentry (adapt for Rollbar, Bugsnag, Airbrake) |
| Product analytics warehouse | [`databricks.md`](./sources/databricks.md) | Databricks SQL (adapt for Snowflake, BigQuery, ClickHouse, dbt) |

Cross-cutting:

- [`incident-postmortem.md`](./sources/incident-postmortem.md). Add this if the target code looks defensive (null checks, retry, timeout, rate limit, feature flag, egress guard, OOM handler).

No playbook fits the chosen tool → the investigator reads the tool's schema and server instructions first, then follows the Investigation Loop in [`investigator-prompt.md`](./investigator-prompt.md).
