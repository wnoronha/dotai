---
name: no-comments
description: "Strip comments before review: a fresh reviewer flags what to delete, keeps survive only with proof, and real constraints get encoded as lint, types, or tests."
disable-model-invocation: true
---

# No comments

Strip comments before review. A comment that restates the code, narrates history, or guards what a check could enforce is deleted. A keep survives only with proof it is about something the code cannot change.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Spawn a fresh reviewer subagent with the scope and this brief: flag every comment that restates adjacent code, narrates history better kept in git, disables a lint or type check without a reason, or guards behavior a test or type could enforce. For each flag give the file, line, and one-line reason: delete or encode. Do not restate these rules back.
2. Triage the report. Reject flags on comments that document something the code cannot say: public API contracts, format invariants, ordering guarantees. A keep survives only with proof it is about something unchangeable. Reshape the rest into deletions.
3. Delete accepted flags. For constraint comments (`do not remove`, `talk to X before changing`), offer the cheapest in-scope enforcement instead: a type, a runtime check, a test, or a CI lint. If approved, encode then delete. Otherwise delete and report the constraint open.
4. Fix the smallest root-cause change the deletions expose, staying in scope. Never bolt on symptom guards. Fix root causes, not instances outside the fence.
5. Report the deletion count, restored comments, encodings, unenforced constraints, and other open work.
