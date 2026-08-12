# TODO-backlog filing is now on-request only

- An agent files a TODO-backlog entry only when the user asks for one. Proactive filing is gone.
- Removed the approval gate, six generic triggers, the `{{PROJECT_TRIGGERS}}` placeholder, the setup step that gathered project-specific triggers, the unattended-session exception marker, and the rule forbidding subagent filing.
- The end-of-session sweep is close-only. It keeps its override of the markdown-only exemption because docs-only changes can close docs-only entries.
- Defects found but not fixed appear as plain findings in the session report. The earlier prompting interrupted the actual work report with a queue of findings the user never requested.
- The TODO-backlog module remains opt-in and default off. The baseline skill version stays v10.
