---
name: plan-eng-review
description: "Eng-manager plan review. Locks architecture, data flow, diagrams, edge cases, and tests. Forces hidden assumptions open. Runs last so the shipping gate reviews the final amended plan."
---

# Gtan plan eng review

## Scope gate first

Hard stop: if the plan is vague, underspecified, or missing the design doc, send it back to `office-hours` or `plan-ceo-review`. Do not review vapor.

## Checklist

- Architecture: components, data flow (ASCII diagrams), state machines, error paths.
- Edge cases and failure modes enumerated.
- Test matrix: what is verified, how, on which surface.
- Security concerns flagged (hand to `security-review` if deep).
- Docs impact noted.

## Output

Locked plan with diagrams, test plan, and explicit assumptions. Hands to `spec`, then `poteto-mode`.

Source: `~/code/gstack/plan-eng-review/SKILL.md` (551 lines).
