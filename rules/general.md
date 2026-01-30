---
type: "always_apply"
---

# Core Mandates

- Rigorously adhere to existing project conventions when reading or modifying code. Analyze surrounding code, tests, and configuration first.
- NEVER assume a library/framework is available or appropriate. Verify its established usage within the project (check imports, configuration files like 'package.json', 'Cargo.toml', 'requirements.txt', 'build.gradle', etc., or observe neighboring files) before employing it.
- Mimic the style (formatting, naming), structure, framework choices, typing, and architectural patterns of existing code in the project.
- When editing, understand the local context (imports, functions/classes) to ensure your changes integrate naturally and idiomatically.
- Add code comments sparingly. Focus on _why_ something is done, especially for complex logic, rather than _what_ is done. Only add high-value comments if necessary for clarity or if requested by the user. Do not edit comments that are separate from the code you are changing. _NEVER_ talk to the user or describe your changes through comments.
- Fulfill the user's request thoroughly, including reasonable, directly implied follow-up actions.
- Do not take significant actions beyond the clear scope of the request without confirming with the user. If asked _how_ to do something, explain first, don't just do it.
- Prioritize simplicity and minimalism in your solutions.

# RESTRICTIONS

- NEVER push to remote git unless the User explicitly tells you to
- you have no power or authority to install globally avaiable scripts/apps

# READING FILES

- always read the file in full, do not be lazy
- before making any code changes, start by finding & reading ALL of the relevant files
- never make changes without reading the entire file

# EGO

- do not make assumption. do not jump to conclusions.
- always consider multiple different approaches, just like a Senior Developer would

# FILE LENGTH

- ideally, keep all code files under 300 LOC
- files should be modular & single-purpose

# WRITING STYLE

- each long sentence should be followed by two newline characters
- use simple & easy-to-understand language. 
- be concise, use short sentences
- make sure to clearly explain your assumptions, and your conclusions

# CODING STANDARDS

## General Guidelines

- use/change absolute minimum code needed

## Naming Conventions

- Use camelCase for variables and functions
- Use PascalCase for classes and components

## GIT Commit Guidelines

- Use a descriptive commit message that:
- Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
- Summarizes what was accomplished, lists key changes and additions
- References the task number and task list file context
- Good example `git commit -m "feat(module): add payment validation logic, #GITHUB-ID" `

## Error Handling

- Always log errors (console.error) for debugging purposes

## Code Structure

- When generating new code, please follow the existing coding style.
- Prefer functional programming paradigms & principles where appropriate.
- Use pure functions whenever possible
- Avoid side effects in functions
- Use async/await for asynchronous code
- Don't use magic numbers in code. Numbers should be defined as constants or variables with meaningful names
- Use `fetch` for HTTP requests, not `axios` or `superagent` or other libraries.

## Testing

- Write unit tests a lot (aim at least for covering all user scenarios)!
- Prefer the Jest runner if possible (if not possible, ask the user to choice different runner - provide the best possible options to run tests in the context for the codebase)
- Never ever remove any tests if they are failing (only if there are no longer needed)

## Dependency Management

- use local package manager (if no present, prefer yarn instead of npm!)
- Always use the latest stable version of dependencies
- Avoid using deprecated, outdated and unsecured libraries
- Never ever install a global dependency (eg. npx install -g ...)!

## TypeScript Guidelines

- Use TypeScript for new code (if possible)
- Prefer immutable data (const, readonly)
- Use interfaces for data structures (if possible)
- Use TSX "node --import=tsx ..." to run typescript locally (for production code use tsc build)
- Strict TypeScript types with zero "any"
- Dont use "ts-nocheck" or "ts-ignore"

# Agent Mode
- ALWAYS read AGENTS.md file first
- use Context7 skill to get docs/wiki for any framework technology you gonna use, and build on top of that
- use sequentialthinking tool to break down complex tasks and planning
- dont remove any code, if not asked to (not even "dead code")
- Think carefully and only action the specific task I have given you with the most concise and elegant solution that changes as little code as possible.
- Always summarise changes you (agent) made into the changelog.md (create file if needed), with timestamp (eg, 202507192135) -> specifically I am interested in "why" you made changes that way + always include the name of the dependency you needed to add, use bullet points only, be concise (minimal words to deliver the message), latest changes summary should be at the top of the changelog file (prepend it, not append)

