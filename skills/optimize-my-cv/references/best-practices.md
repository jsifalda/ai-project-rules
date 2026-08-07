# CV best practices — tech reference

Distilled from `tech-resume-optimizer` in [Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills) (MIT).
Reframed from a rewriter's guidance into audit criteria. The upstream is IC-tech-focused;
the engineering-leadership calibrations in `rubric.md` are additions, not upstream material.

## Section order and what belongs where

Expected order for a tech CV: contact, professional summary (optional), technical skills,
work experience, projects, education, certifications (if relevant). A CV missing technical
skills near the top, or burying it below education, loses ATS keyword weight and recruiter
scan time — both parse top-to-bottom first.

A Projects section carries the most weight for four groups: junior engineers, career
changers, bootcamp graduates, and anyone with a work-history gap. For these candidates,
a missing or thin Projects section is a bigger gap than a missing certification — it is
often the only evidence of hands-on technical work the CV can offer.

## Contact block

Required: email, phone, city/state (not full street address), GitHub. GitHub is effectively
required for SWE roles — its absence is a flag, not a neutral omission, since it is the
primary way a recruiter or hiring engineer verifies real code. Portfolio/personal site,
LinkedIn, and a tech blog (if one exists) strengthen the block but are not mandatory.

Must be absent: full street address, a photo, and unrelated social media links. Any of
these present is a miss — they add no signal for a technical hire and, for address and
photo, introduce a bias-review problem the CV does not need.

## Technical skills section

Three organization strategies, each with a different cost:

- **By category** (Languages / Frameworks / Databases / Cloud-Infrastructure / Tools) —
  most legible to a human reviewer, costs more space.
- **By proficiency** (Expert / Proficient / Familiar) — signals depth but is easy to overclaim;
  use carefully, since a mismatch surfaces fast in an interview.
- **Flat list** — most ATS-friendly (simplest to keyword-match), costs nuance — a reviewer
  cannot tell primary stack from tools touched once.

Audit the exclude list. Presence of any of these is a defect, not a stylistic choice:

- Microsoft Office (assumed baseline, wastes a line)
- Operating systems, unless the target role is DevOps/SRE
- Outdated tech, unless the role specifically calls for it
- Skill bars or star ratings — subjective, and they break ATS parsing (ATS reads text, not graphics)
- Any technology touched exactly once with no supporting bullet elsewhere on the CV

## The bullet formula

Every experience bullet should resolve to:

`[Action Verb] + [Technical What] + [Scale/Impact] + [Technology Used]`

A bullet missing the Scale/Impact or Technology Used component reads as vague — it tells a
reviewer *that* work happened, not what it was worth or how it was done. Weak-vs-strong pairs
from the upstream:

- Weak: "Worked on backend services"
  Strong: "Architected microservices migration from monolith, reducing deployment time from
  2 hours to 15 minutes and enabling independent team deployments"
- Weak: "Helped improve system performance"
  Strong: "Optimized PostgreSQL queries and implemented Redis caching, reducing API latency
  by 60% (from 500ms to 200ms) for 100K daily active users"
- Weak: "Built features for the product"
  Strong: "Built real-time notification system using WebSockets and AWS SNS, handling 1M+
  messages daily with 99.9% delivery rate"

## The four metric families

A CV with no quantified bullets across any of these four families is under-evidenced,
regardless of how senior the role titles look:

- **Scale** — users ("serving 500K DAU"), requests ("handling 10K requests/second"), data
  volume ("processing 50TB daily"), uptime ("maintaining 99.99% availability").
- **Performance** — latency before-and-after ("reduced from 500ms to 200ms"), percentage
  speedups ("improved by 40%"), load-time cuts ("decreased by 2 seconds").
- **Efficiency** — cost reduction ("reduced AWS costs by 40%"), deployment time ("cut from
  2 hours to 15 minutes"), resource usage ("reduced memory usage by 30%").
- **Business** — revenue ("features drove $2M revenue"), conversion ("improved checkout by
  15%"), engagement ("increased DAU by 20%").

A candidate does not need all four, but a bullet claiming impact without a number in any of
these families is a claim, not evidence.

## Projects

Expected format: `Project Name | Technologies | Link`, followed by bullets describing what
it does, the technical challenges solved, and scale/usage metrics if available.

A project belongs on the CV if it has real users, is open source, won a hackathon, or is a
personal project with genuine complexity. A project is a liability, not neutral padding, if
it is a tutorial follow-along, a to-do app, incomplete, or ordinary coursework (unless the
coursework result is exceptional) — these read as evidence of *following instructions*, not
of independent engineering, and a reviewer who spots one starts discounting the rest of the
section.

## ATS versus the technical recruiter

The two audiences want different things, and the tension is real, not imagined:

- **ATS** wants exact keyword matches against the job description, standard section headers
  it can parse, and no tables or graphics — anything visually clever gets silently dropped
  or garbled on ingest.
- **A technical recruiter** wants depth, scale, and evidence of problem-solving — the same
  things that make a CV interesting to a human make it harder for a parser.

Where they conflict: creative formatting (tables, columns, icons for skill levels) helps a
human skim but breaks ATS parsing. The resolution is not a compromise on one axis — satisfy
both by using plain structure (standard headers, no tables/graphics) to pass the parser, and
carrying the depth and scale signal inside the bullet text itself, where a human reads it
and a parser is indifferent to it.

## Stack mismatch

When the CV's demonstrated stack doesn't match the target role's stack, the diagnostic
question is what it leads with, not whether the technologies overlap:

- Lead with transferable framework experience, not a bare list of unrelated technologies.
- Show ramp-up evidence — prior instances of picking up a new stack quickly are worth more
  than aspirational skill claims.
- Never pad with technologies the candidate cannot discuss. Example of the right move:
  "Django" experience for a Flask role becomes "Extensive Python web framework experience
  (Django); quick to ramp on new frameworks" — not a bare addition of "Flask" to the skills
  list.

A skills list padded with unfamiliar technology to chase a keyword match is a defect, even
though it may pass ATS — it fails the very next stage.

## The interview-consistency test

The binding constraint on every claim: only what the candidate can discuss deeply belongs
on the CV. Every bullet must be defensible under questioning. Every listed project must be
explainable at an architecture level — what it does, why it was built that way, what broke.

A CV that overclaims does not fail at the resume screen — it fails in the interview, which
is the more expensive place to fail. Screening out an overclaim costs a reviewer minutes;
surfacing it in an interview costs both sides a full interview slot and damages the
candidate's credibility on everything else they said. When auditing, treat "impressive but
unverifiable" claims as a higher-risk finding than "modest but concrete" ones.
