---
name: generate-prd-tasks
description: Generates a detailed, step-by-step developer task list in Markdown format from a Product Requirements Document (PRD). Use when you have a PRD and need to break it down into high-level parent tasks and granular sub-tasks for implementation. Triggers on requests like "generate tasks from PRD", "create task list for this PRD", or when an implementation plan is needed from a PRD.
---

# Generate PRD Tasks

## Overview

This skill guides you through transforming a PRD into an actionable task list for developers. It follows a two-phase process: high-level parent tasks first, then detailed sub-tasks upon confirmation.

## Workflow

### 1. Research & Analysis
- **Analyze PRD:** Read and understand functional requirements, user stories, and technical constraints.
- **Assess Current State:** Review the codebase to identify existing infrastructure, architectural patterns, and reusable components. Note files that need modification.

### 2. Phase 1: Parent Tasks
Generate approximately 5 high-level tasks based on the PRD and current state assessment. 

**Interaction Protocol:**
Present the high-level tasks to the user and stop. 
Inform the user: "I have generated the high-level tasks based on the PRD. Ready to generate the sub-tasks? Respond with 'Go' to proceed."

### 3. Phase 2: Detailed Sub-Tasks
Once the user confirms with "Go", break down each parent task into smaller, actionable sub-tasks.

- Ensure sub-tasks follow existing codebase patterns.
- Cover all implementation details implied by the PRD.

### 4. Finalizing Output
Combine all sections into the final Markdown structure and save it.

**File Location:** `./_tasks/`
**Filename:** `tasks-[prd-file-name].md` (matches the PRD's base name).

## Output Format

The task list must follow this structure:

```markdown
## Relevant Files

- `path/to/potential/file1.ts` - Brief description of why this file is relevant.
- `path/to/file1.test.ts` - Unit tests for `file1.ts`.
- `lib/utils/helpers.ts` - Utility functions needed for calculations.

### Notes

- Unit tests should be placed alongside the code files.
- Use `npx jest [optional/path/to/test/file]` to run tests.

## Tasks

- [ ] 1.0 Parent Task Title
  - [ ] 1.1 [Sub-task description 1.1]
  - [ ] 1.2 [Sub-task description 1.2]
- [ ] 2.0 Parent Task Title
  - [ ] 2.1 [Sub-task description 2.1]
- [ ] 3.0 Parent Task Title
```

## Target Audience
The output should be tailored for a **junior developer** who needs clear, sequential steps to implement the feature while maintaining consistency with the existing codebase.
