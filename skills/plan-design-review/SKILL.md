---
name: plan-design-review
description: "Designer's-eye plan review. Rates each design dimension 0-10, shows what 10 looks like, then edits the plan. AI-slop detection. Use for any user-facing surface before code."
---

# Gtan plan design review

## Scope gate first

Hard stop: no UI scope, no review. Route non-visual plans to eng/DX reviews.

## Checklist

- Initial design rating per dimension (0–10), with what 10 looks like.
- AI-slop detection: generic layouts, stock patterns, lorem-equivalent choices.
- Interactive: one question per design choice; record decisions.
- Amend the plan to reach 10 on the dimensions that matter.

## Output

Amended plan with ratings, decisions, and required design fixes. Visual build follows via `poteto-mode` feature playbook.

Source: `~/code/gstack/plan-design-review/SKILL.md` (874 lines).
