# Drop the Bash file-read ban from general.md

- Removed "Never `cat`, `sed -n`, `head` or `tail` a file in Bash." from `# READING FILES`. The `Read` with `offset` and `limit` guidance stays.
- Why: agents ignored it routinely, and it conflicted with the harness prompt. A Bash read costs about the same as `Read`, so the sentence cost always-loaded tokens for no effect.
- Phase 3 now says "`code-review` subagent". Claude Code renamed the Task tool to Agent.
