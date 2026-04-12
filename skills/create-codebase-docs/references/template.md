# STARTHERE.md Template

Use this template as a starting structure. Adapt sections to fit the project — skip sections that don't apply, add sections that do. The tone should feel like a knowledgeable colleague walking you through the codebase over coffee.

---

```markdown
# Welcome to [Project Name]

> One-line pitch: what this project does and why it exists.

## What This Project Does

2-3 paragraphs explaining the project in plain language. No jargon. Use an analogy if it helps.
Think: "If I were explaining this to a smart friend who's never seen the code, what would I say?"

## Architecture Overview

High-level description of how the system is structured. Follow with a Mermaid diagram.

### System Diagram

Use flowchart TD or C4-style diagrams. Label clearly.

` ` `mermaid
flowchart TD
    A[Client] --> B[API Gateway]
    B --> C[Service A]
    B --> D[Service B]
    C --> E[(Database)]
    D --> E
` ` `

### Key Components

For each major component/module:
- **What it does** (one sentence)
- **Where it lives** (directory path)
- **What it talks to** (dependencies / connections)

## Directory Structure

Show the top 2-3 levels with annotations:

` ` `
project/
├── src/              # Application source code
│   ├── api/          # REST/GraphQL endpoints
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   └── utils/        # Shared utilities
├── tests/            # Test suites
├── config/           # Environment and app config
└── docs/             # Additional documentation
` ` `

## Tech Stack & Why

| Layer | Technology | Why We Chose It |
|-------|-----------|----------------|
| Frontend | React + TypeScript | Type safety, ecosystem |
| Backend | Node.js / Express | Team familiarity, async I/O |
| Database | PostgreSQL | Relational data, JSONB support |
| Infra | AWS / Docker | Scalability, team experience |

Don't just list technologies — explain the "why" behind each choice.

## How Things Connect

Explain the data flow for 1-2 key user journeys. Walk through what happens when a user does X:

1. User clicks "Submit"
2. Frontend sends POST to `/api/orders`
3. API validates input, calls OrderService
4. OrderService writes to DB, emits event
5. NotificationService picks up event, sends email

## Getting Started (Developer)

Quick-start for a new developer:
1. Clone the repo
2. Install dependencies: `npm install` / `pip install -r requirements.txt`
3. Set up env: `cp .env.example .env`
4. Run: `npm run dev` / `python manage.py runserver`
5. Verify: open `http://localhost:3000`

## Lessons Learned & Pitfalls

This is the most valuable section. Be honest and specific.

### Bugs We Hit

- **[Bug title]**: What happened, why it happened, how we fixed it. What to watch out for.

### Decisions We'd Reconsider

- **[Decision]**: Why we made it, what we know now, what we'd do differently.

### Things That Surprised Us

- **[Surprise]**: Something non-obvious about the codebase, a library, or the domain.

### Best Practices We Adopted

- **[Practice]**: What it is, why it matters, how to follow it.

## Common Tasks

Quick reference for things developers do regularly:

| Task | Command / Steps |
|------|----------------|
| Run tests | `npm test` |
| Add a migration | `npm run migrate:create` |
| Deploy to staging | `git push origin staging` |
| Check logs | `kubectl logs -f deployment/api` |

## Want to Learn More?

- [README.md](./README.md) — project overview and setup
- [CONTRIBUTING.md](./CONTRIBUTING.md) — how to contribute
- [Architecture Decision Records](./docs/adr/) — why we made key decisions
- [API Docs](./docs/api/) — endpoint reference
```

---

## Writing Guidelines

- **Analogies**: Compare complex systems to familiar things ("Think of the message queue like a post office...")
- **Anecdotes**: Share real stories ("We once deployed without running migrations and...")
- **Questions**: Use rhetorical questions to guide the reader ("Why not just use a single database?")
- **Humor**: Light humor is welcome — avoid forced jokes
- **Honesty**: Admit tradeoffs and mistakes. It builds trust and prevents repeat errors
- **Diagrams**: At least one Mermaid diagram. More for complex systems. Keep them readable (max 15 nodes per diagram, split if needed)

## Section Priority

If the project is small, focus on these (in order):
1. What This Project Does
2. Architecture Overview (with diagram)
3. Tech Stack & Why
4. Lessons Learned & Pitfalls

Skip or condense other sections for smaller projects.
