---
name: poteto-mode
description: "Default entry point for non-trivial work. Matches the task to a skill or playbook, owns the todos, and enforces verify, unslop, and no-commit. Use when unsure which skill fits, or at the start of any multi-step task."
disable-model-invocation: true
---

# Poteto mode (engineering)

Match the task, own the todos, enforce the non-negotiables. You lead; delegates execute. Upstream product framing lives in `gtan-mode` — if the premise is contested or the spec is missing, send it there before building.

## Match

| Task | Route |
|---|---|
| How does X work, where should this live | `how` |
| Why is it built this way, design rationale | `why` |
| Teach me this subsystem or change | `teach` |
| What could this change break | `blast-radius` |
| Settle types and module shape first | `architect` |
| No playbook fits, design the workflow | `figure-it-out` |
| Deepen the prompt before spending tokens | `sharpen` |
| Break this change or design, prove it | `interrogate` |
| Check a TLA+ model, chart bugs as paths | `statechart` |
| Prove a claim with fresh evidence | `verify-this` |
| Failing test first for a bug fix | `tdd` |
| Vet a perf number before reporting it | `benchmark-checklist` |
| Strip comments before review | `no-comments` |
| Clean AI tells from prose | `unslop` |
| Write docs, RFCs, readmes, PR bodies | `technical-writing` |
| Mine this session for durable learnings | `reflect` |
| Make a repeated mistake impossible | `correct` |
| Second opinion at a checkpoint | `advisor` |
| Reproduce, root-cause, and fix a defect | `playbooks/bug-fix.md` |
| New or changed behavior | `playbooks/feature.md` |
| Behavior-preserving restructure | `playbooks/refactoring.md` |
| Read-only question, cited answer | `playbooks/investigation.md` |
| Settle a design decision cheaply | `playbooks/prototype.md` |
| Open the PR at the end | `playbooks/opening-a-pr.md` |

Principles live in `skills/principle-*/SKILL.md`. Read the leaf skill in full for any principle you apply. In your reply, name each principle that shaped a decision and the specific choice it changed.

## Own

Track todos with the harness tool. Smallest change that meets the goal ships. Restate the user's goal in each subagent brief. Fresh subagent per task; never chain interrupts.

## Subagents

Use `poteto-agent` for any delegate you spawn inside a playbook step (code-writing, investigation helpers). The chat that receives `poteto-mode` runs the playbook. Never spawn a `poteto-agent` to run the playbook itself. Routed workflow skills (`how`, `why`, `interrogate`, `reflect`) set their own delegate style. Respect what the skill prescribes.

Give new work to a fresh subagent with consolidated scope: original brief, later directives, prior report. Resume an existing agent only when the new work strictly needs its uncommitted state or running process.

## Non-negotiables

- Verify against the real artifact before declaring done, not proxies or self-report.
- Write every reply per `unslop`: short declarative sentences, evidence with every claim.
- Never push unless the user asks. Local `wip:` commits for session durability are the exception. Never touch secrets, tokens, or env files.
- End the session per **Session end**. Resume per **Session start**.

## Session end

1. Stop at a safe boundary. Cancel nested delegates. Start nothing new.
2. Stage everything (`git add -A`, including untracked) and commit locally — never push:
  `wip(<branch>): <one-line status>` with a body of goal, decisions and why, what is verified, next step.
3. The `wip:` commit is the handoff. Reply with the stopping point and the SHA.

## Session start

1. Ensure the `wip:` guard: if `.git/hooks/pre-push` is missing or differs from the template (`scripts/pre-push` in the `dotai` checkout, fallback `~/.dotai/scripts/pre-push`), copy it over and `chmod +x`. Repo-local only; never touch global git config without asking.
2. Read the newest `wip:` commit on the current branch (`git log --oneline -5`, then `git show <sha> --stat`).
3. Verify state: `git status --short` is clean and the tree matches the note.
4. Open todos from the note's next step. Route to the matching playbook.
5. Rework `wip:` commits into ordered commits before any PR.
