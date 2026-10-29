# About the two modes

## Why product and engineering route separately

A wrong premise built well is still wrong. Reviews that judge direction need different questions than reviews that judge code. One router asking both sets asks neither well. `gtan-mode` asks whether to build. `poteto-mode` asks how to build well.

## How a task flows

Vague work enters `gtan-mode` at `office-hours`, which reframes the request and writes a design doc. The reviews that apply run next: `plan-ceo-review` for scope, `plan-design-review` and `plan-devex-review` for surface, `plan-eng-review` last so the shipping gate sees the final plan. `spec` files the result. The spec hands to `poteto-mode`, which matches a playbook, fans out to `poteto-agent` delegates, verifies on the real artifact, and opens a PR.

Sharp tasks skip the product side and start in `poteto-mode`. If the premise cracks mid-build, the task goes back to `gtan-mode` instead of pushing through.

## What stays manual

No auto-merge and no auto-deploy anywhere in the stack. `wip:` session commits never push; the `pre-push` hook blocks them. PRs open ready for a human who reads the diff. `security-review` findings arrive as repair proposals, never silent fixes.
