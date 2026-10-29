---
name: reflect
description: Mine the current conversation for durable learnings, then route them into skill edits. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Find this conversation's transcript wherever the active harness stores session transcripts. Do not cross workspace boundaries into unrelated projects' chats. If no transcript file is available, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One message, three subagent calls with full tool access (reviewers look up tickets, chat threads, and traces the transcript references). Pick each subagent's reasoning level and speed for the job.

| Lens | Prompt template |
|---|---|
| Judgment | `references/judgment-reviewer.md` |
| Tooling | `references/tooling-reviewer.md` |
| Divergent | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the response body.

## 3. Synthesize

Spawn one synthesizer subagent. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. Skill prose is for things mechanisms cannot enforce.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent, so do not auto-apply.

File each Backlog item to the team's tracker without waiting. Only the Accepted list waits for approval.

Never open a PR or push. Follow each approved row's routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): draft, test, and iterate per the harness's skill-authoring flow.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): run the description-optimization loop.
- `new skill: <kebab-name>`: draft the new skill through the harness's skill-authoring flow. Do not invent the shape ad hoc.

If the environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed: `<issue title>`. One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
