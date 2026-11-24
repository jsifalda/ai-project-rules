# Planning

- Use plan mode for a task with an architectural decision or a change across several files.
- Something goes sideways → stop and re-plan.
- Plan an outage recovery one attempt at a time. Report each result before you plan the next attempt.
- Plan the verification steps, not only the building.
- Write detailed specs upfront.
- Start each design from an established product's solution. Name it in the plan, challenge it
  from first principles, and justify any deviation.
- Never close an open design question by calling it out of scope, in a plan or a grill. Ask the user.

## Agent delivery

- Name the current delivery bottleneck before you speed up a flow. Fix that one, then name the next.
- Make deploy and release fast and safe before you add agent throughput.
- Fix or delete wrong context before you add more, since it misleads an agent more than missing context.
- Give each unit of agent work a tracked issue with a done check. Never leave work only in chat.
- Trigger agent work from events, not from polling or a manual prompt.
- Let an agent propose a change. Keep the approval with a human who holds the context.
- Make each agent change carry its verification record. Review the record first, the diff only when the record is weak.
- Raise change quality and its proof before you cut review when approvals are slow.
- Point a loop at each signal source: errors, failed runs, stale flags, dropped findings. File what it finds as issues.
- Give the human one daily view of open agent work: the merges, answers and reviews it waits on.
- Plan agent work so human time goes to hard product calls, not routine work.
- Never set a throughput count as a goal. Use it to ask questions.
