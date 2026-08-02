---
name: break-into-tasks
description: Break one task into ridiculously small, atomic steps of under a minute each, ending with the exact first move and where to put your hands. Use when the user is stuck starting something, says 'I can't start', 'I'm staring at this', 'this is too big', 'break this down', 'break this into tasks', 'micro steps', 'atomic steps', or 'what is the very first thing I do'. Works for any task, coding, admin, writing, or errands, and reads the repo when the task names code so steps cite real paths and commands. Refuses to run without a task, never invents one, asks until the task is concrete, then sharpens it through a one-question-at-a-time interview before splitting. Do NOT use for a multi-day project needing milestones and one-day tasks, for scheduling or calendar work, for habit systems with no finish line, or to write an implementation plan.
---

# Break Into Tasks

One task in. Steps so small that starting is easier than avoiding, out.

This is a paralysis-breaker, not a planner. The user is frozen in front of one thing. Every step must be small enough that refusing it feels absurd, and the last line tells them exactly where to put their hands.

Four gates, in order. No skipping ahead.

## Gate 1, task required

Hard gate. No task in the invocation and none in the conversation, then ask this and stop:

`What task are you staring at?`

- STOP after asking. Do not continue in the same turn.
- Never infer a task from surrounding context, open files, git state, or the last thing discussed.
- Never invent a task. Never offer a menu of guesses.
- No task, no output. There is nothing to break down.

## Gate 2, clarity

Test the task with one question. Can the first step name a specific object, file, app, or surface?

- Passes -> "add rate limiting to the login endpoint", "cancel the gym membership".
- Fails -> "sort out the backend", "get on top of admin".

Fails, then ask targeted questions until it passes. Ask about the target, not about how it feels.

Anything the environment can answer, look it up. Does the file exist, what is the function called, is there a script for it already. Never ask what you can read.

## Gate 3, sharpen

Invoke the `grill-me` skill against the task.

- One question at a time, each with your recommended answer.
- Decisions go to the user. Facts get looked up.
- Stop the moment the task is one sentence the user agrees with.

The exit condition is that sentence, not a quota of questions. Do not grill for its own sake.

## Gate 4, decompose

Feed the sharpened task into this prompt, verbatim, substituting it for `[Task]`.

```
I am staring at [Task] and can't start. Break this down into 'Ridiculously Small' steps that take less than 1 minute each. Give me the first step and tell me exactly where to put my hands to begin
```

Codebase awareness:

- Task names code, then read the relevant files first. Every step cites a real path, symbol, or command.
- Task does not name code, then stay conversational and never touch the filesystem.

## Output format

Full list, first step called out. Chat only. No file, no save prompt, no offer to put it anywhere.

```
# [Sharpened task]

## Steps
1. [verb-first action, under 60 seconds]
2. ...

## Start here
Step 1. [exactly where the hands go, what to open, click, type, or touch]
```

## Rules that make the list startable

- Every step is a physical, observable action. Banned openers -> "think about", "consider", "plan", "decide", "figure out".
- Under 60 seconds each. A step that could run longer gets split.
- The first step never requires a decision. Decisions get their own step, later in the list.
- Steps name concrete targets. "Open `src/auth/login.ts`", not "open the file". "Open the banking app", not "check your account".
- Verb first, every line.

## Examples

Coding task, sharpened to a 5-per-minute limit on login. Note the title names the ramp, not the finished job. Steps stop where momentum takes over.

```
# Get moving on the login rate limit

## Steps
1. Open `src/auth/login.ts`.
2. Run `grep -rn "rateLimit" src/` and read the hits.
3. Open `package.json` and check whether a rate-limit package is already listed.
4. Scroll to the `POST /login` handler, put the cursor on its first line.
5. Type the comment `// rate limit, 5 per minute`.
6. Save the file.
7. Add one empty test named `blocks the 6th login in a minute`.

## Start here
Step 1. Editor, open the file finder, type `login.ts`, Enter.
```

Non-coding task, same shape.

```
# Start cancelling the gym membership

## Steps
1. Pick up your phone.
2. Open the gym app, or the gym website if there is no app.
3. Tap Account.
4. Screenshot the next billing date.
5. Find the Cancel or Membership link, tap it.
6. Read the notice period out loud.
7. Tap through the first cancellation screen.

## Start here
Step 1. Phone. In your hand. Screen on.
```
