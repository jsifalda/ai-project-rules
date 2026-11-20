---
name: statechart
description: Model a system that moves between states as a TLA+ spec, explore every reachable state, check each rule, and draw a Mermaid statechart with the shortest path to each broken rule. Publishes the chart and report as a page. Use for /statechart, or to show a bug as a path through states. Do NOT use for a plain flowchart or sequence diagram with no rules to check, or for a model too large to explore without a model checker.
license: MIT
disable-model-invocation: true
metadata:
  version: "1.0"
  upstream: "https://github.com/backnotprop/pstack"
---

# Statechart

## Reader

- Let the reader decide if the behavior is right. Write every label in the reader's words, never a variable or action name.
- Work in a scratch folder outside the repo. Use the same folder when you run again on the same model.

## Write the spec

- Write the model as a TLA+ spec and a config in the scratch folder. A human can check it with TLC later.
- Write each rule the reader agrees to as an invariant when it must hold in every state. Add a variable when a rule needs one.
- Write a rule that something must happen eventually as a temporal property, never as an invariant.
- Never weaken a rule to make it hold.
- Write `Next` as a disjunction of named actions, one per thing that can happen.
- Add a `Done` action, true only in correct end states, that changes nothing. A correct end state then is not a deadlock.
- Keep the constants small, because exploration continues past a broken state.

## Explore and check

- Explore breadth-first from each state `Init` allows, so the first path found to each state is a shortest one.
- Treat two states as the same only when every variable is equal.
- About 15 states or fewer → explore by hand, as a numbered state table with the values, the parent state and the action.
- Larger model → write a throwaway explorer script in the scratch folder, on a runtime the host already has.
- Never install a runtime, package or tool for it.
- Too large for either → shrink the constants, or report the check as incomplete and name the rules not checked.
- Check each invariant in each state. Continue past a broken state, so the chart shows the states after a bug.
- Check each state for deadlock: no action, `Done` included, is enabled.
- For a temporal property, find a lasso: a path into a loop that repeats forever and never satisfies the property.
- Count a loop only when the fairness the spec states allows it to repeat forever.
- Count staying in one state forever as a loop too, unless fairness forces an enabled step out of it.
- State fairness only for steps the system must take, such as a reply, never for a choice the user makes.
- Replay each bug path step by step against the spec before you report it.

## Pick the chart

- Use a flat chart, parent states for nested phases, or parallel regions for parts that change independently.
- Name Mermaid states `s1`, `s2` and so on, with labels via `state "Label" as s1`.
- Label each state with what the reader can see or cares about.
- Label each step as the user sees it happen. Never name the code or the TLA+ action.
- Give two actions that go from the same chart state to the same chart state one label, so they share one arrow.
- End a step label with its condition in brackets, in the reader's words, when the step occurs only in some conditions.
- In a regions chart, bracket a condition on another region only with that region's state labels, never your own words.
- Name the result in the step label when a value that no label shows decides where the step goes.
- Never draw a step that stays in one chart state. Split the label when the reader must see that step.
- Put each chart state in a group, one per phase, and give each group one of the color classes in the `classDef` list below.
- Give no group class to a chart state whose model states are in different groups.
- Give the chart a title of 2 to 4 words.

## Keep it readable

- Aim for about 20 arrows or fewer.
- Coarsen labels first. Give one label to values that act the same, and drop details the reader does not need.
- Keep each state of a bug path and each mark.
- Avoid a merge that turns a `breaks` state into `mayBreak`, because it hides where the rule breaks.
- Never merge two states that break different rules.
- Then hide steps the reader does not need, such as a reset that every state has.
- Keep each chart state reachable from a start state when you hide steps.
- Keep at least one arrow out of each chart state that has a step out in the model.
- Hide all steps of an arrow or none, because hiding some narrows its condition.
- Above 500 distinct states, chart only the paths to broken rules. With no broken rule, draw no chart.

## Marks

- Mark a chart state `breaks` when every model state behind it breaks a rule.
- Mark it `mayBreak` when only some model states behind it break a rule.
- Mark each state before the broken state on the shortest path to it `bugPath`. The broken state keeps only `breaks` or `mayBreak`.
- Mark each state in the loop of a property lasso `repeats`.
- In a regions chart, mark a state when each combination of region states that includes it can break a rule.
- In a regions chart, mark each state of a combination that can break a rule when none of its states has a mark.
- Write a legend that names the rules behind each mark, as a list in the report. The page already draws the mark swatches.
- When one mark covers more than one rule, say which state breaks which.
- Write one `classDef` line per class used, then `class` lines for each state's group and marks.
- Give a `breaks` or `mayBreak` state no `bugPath`. A state can carry `repeats` with any other mark.

```
classDef blue fill:#c3e0ff
classDef orange fill:#f0d3bf
classDef purple fill:#e3d5ff
classDef yellow fill:#f0dcbf
classDef teal fill:#bfe3df
classDef tan fill:#e5d9ce
classDef pink fill:#ffcbe6
classDef breaks fill:#ffecee,stroke:#e72e3b,stroke-width:2.5px,color:#cd2834
classDef mayBreak fill:#fff3e6,stroke:#e8730c,stroke-width:2.5px,color:#b85a06
classDef bugPath stroke:#1680f3,stroke-width:2.5px
classDef repeats stroke:#9b35d6,stroke-width:2.5px,stroke-dasharray:6 3
```

## Publish

- Copy `references/page.html` from this skill folder to `statechart.html` in the scratch folder.
- Load each skill the Artifact tool's own instructions name before you write the page. Keep the template design unchanged, because it already meets the page contract.
- Publish the filled template as is. Add no `<html>` or `<head>` wrapper.
- Replace every occurrence of each placeholder, per the table below.

| placeholder | content | escaping |
|---|---|---|
| `{{TITLE}}` | the chart title | HTML-escape `&`, `<`, `>` |
| `{{SUMMARY}}` | one `<p>` verdict line, then a `<ul>` with one `<li>` per broken rule | HTML-escape `&`, `<`, `>` in the text you put in the markup |
| `{{MERMAID}}` | the Mermaid `stateDiagram-v2` text, empty when no chart is drawn | HTML-escape `&`, `<`, `>` |
| `{{REPORT}}` | rules and results, the legend, each bug path as an `<ol>`, hidden steps, what the model leaves out, the exploration method | HTML-escape `&`, `<`, `>` in the text you put in the markup |
| `{{SPEC}}` | the TLA+ spec text, then its config | HTML-escape `&`, `<`, `>` |

- Ask first when the model or its labels hold private or regulated data, such as non-public code, customer data, health data or a secret.
- In Claude Code, publish `statechart.html` with the Artifact tool, icon `chart`, with no confirm step. Give the link.
- Publish a re-run on the same model from the same file path, so the link stays.
- On a host with no Artifact tool, give the file path. The page needs network access to draw the chart.

## Hand off

- When you drew a chart, show the Mermaid text as a `mermaid` code block in the reply.
- Add one line per bug: the rule, the reader's sentence for it, and the path as the report numbers it.
- Say which steps the chart hides and what the model leaves out.
- Name the exploration method and the state count. Say the spec was not machine-checked, and give the paths of the spec and its config.
- When the model describes code, replay each bug path against the real code as a test or a live repro.
- Treat the model as wrong when a bug does not occur in the code, until you show otherwise.
