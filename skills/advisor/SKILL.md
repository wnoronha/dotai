---
name: advisor
description: "Advisor mode. Consult a stronger (or different) model at key checkpoints: before major decisions, when stuck on an error, and before declaring a task done. Use when the user asks for a second opinion, picks an advisor model, or turns the advisor on or off. Never enable it on your own."
---

# Advisor

You are the main model. Advisor mode adds a second, stronger model that you consult at a few key points. The advisor gets your briefing (and the transcript when available), thinks hard, and returns a verdict with guidance. It does not edit files. You still do the work and make the final call.

State lives in `.ai/tmp/advisor-state.json`. When that file exists with `"enabled": true`, advisor mode is on for this session.

## Commands

The text after the invoke selects the action. `/advisor`, `advisor on`, and "turn the advisor on" all enable.

| Input | Action |
| --- | --- |
| enable | Enable with the default advisor: the strongest model available to subagents at its highest reasoning effort. |
| `advisor <model>` | Same, with the given model. Resolve names against the subagent models available to you; on no match, name two or three close options and keep the current model. |
| `advisor off` | Disable: delete the state file. |
| `advisor status` | Report model and consult count. Changes nothing. |
| `advisor ask <question>` | Consult now about the current work, regardless of checkpoint. |

If the message also contains a task, enable first, then do the task under advisor mode.

## Enabling

1. Resolve the model as described above and write `.ai/tmp/advisor-state.json`, creating the directory if needed: `{"enabled": true, "model": "<slug>", "consults": 0}`. If a state file already exists, keep its `model` unless this command names one, and reset `consults` to 0.
2. Confirm in one line: `Advisor on: <model>. I'll consult it before major decisions, when I'm stuck, and before I call the task done.` Then continue with any task in the same message.

## Checkpoints

Consult at these points and nowhere else. Each consult is a strong-model call; the value comes from using it selectively.

1. **Before a major decision.** Choosing between architectures or approaches; changes that are hard to reverse or have a wide blast radius (schema or data migrations, deleting or rewriting a module, public API or config format changes, dependency swaps, auth, payments, or other security-sensitive code); or a request that is ambiguous in a way that would change the work materially. Consult once you have a concrete plan and the options in hand, not before you understand the problem. One consult covers the plan; do not re-consult per file.
2. **When stuck.** The same error or failing test after two genuine fix attempts; behavior you cannot explain from the code; or when you are about to reach for a workaround: a retry loop, a `sleep`, a broad `try/except`, skipping a test, or disabling a check to get past something.
3. **Before declaring done.** Any task that changed logic or touched more than a couple of files: consult once before writing the final summary, and include what you verified and how. Skip for trivial edits (typos, comments, a one-line config change) and say so in one line.
4. **On request.** A direct ask, or the user asks what the advisor thinks.

Do not consult for routine steps, for things you can verify yourself (run the test, read the code), or more than once per checkpoint. If you would consult more than about four times in one task, the task should probably be split, or you should ask the user.

## How to consult

1. Build the briefing from `references/briefing-template.md`. Give the advisor everything it needs to disagree with you:
   - The user's request verbatim, plus constraints or corrections they added later.
   - What has happened so far, in order: what you investigated, decided, changed, tried, and ruled out.
   - Relevant tool results verbatim: error messages, stack traces, test output, diffs. Trim unrelated noise and mark trims with `[...]`, but never paraphrase evidence.
   - Current state: `git status --short`, `git diff --stat`, files you touched, anything half-done.
   - Your specific questions, the options you see, and your current leaning with reasons.
   - The transcript when the mode is on in this conversation, so the advisor can read the full conversation itself.
   - No secrets. Redact tokens, keys, and `.env` values.
2. Spawn the advisor as a read-only subagent on the state's model and wait for it. On a second consult in the same session, brief only the delta: what changed since last time plus the new questions. Increment `consults` in the state file.
3. Act on the verdict:
   - `proceed`: go.
   - `proceed with changes`: make the recommended changes unless they conflict with the user's instructions or facts you have verified. Say which you skipped and why.
   - `stop`: do not continue with the plan. Rethink, or bring the disagreement to the user if it is a product or scope question.
   - If the advisor asks for something it needs, provide it once via a follow-up. Do not ping-pong.
   - You are accountable for the result. The advisor is a strong second opinion, not an authority. If it is wrong about the codebase, show it the evidence once, or overrule it and tell the user why.
4. Report each consult to the user in one or two lines: `Advisor (<model>): <verdict>. <One-line summary>. <What you did about it.>` Keep the advisor's full response out of the chat unless the user asks.

## Disabling

On disable: delete the state file and confirm in one line. Do not consult again in this session unless the user re-enables the mode or explicitly asks for a one-off consult.

## Guardrails

- Never enable advisor mode unasked. "Get a second opinion on this" is a one-off consult, not a mode change.
- The advisor is read-only. Never ask it to edit files or do the task.
- Never loop on the advisor: at most one follow-up per checkpoint.
