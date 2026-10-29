### Opening a PR

Invoked at the end of every other playbook.

**Commits.** Commit liberally during work. Rebase into small, ordered commits before opening PRs. Each commit tells one story step.

**PRs.** Run `no-comments` before review. Write title, description, and commit bodies per `technical-writing`, then apply `unslop`.

**Titles.** Conventional Commits `type(scope): subject`, no trailing period. Type such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`.

**Descriptions.** One-minute briefing for a reviewer who has the diff, in this order, dropping empty sections:

- `## Why`: problem and approach, 1–3 sentences.
- `## What changed`: 1–3 bullets.
- `## Scope`: what it covers and deliberately leaves out.
- `## Tradeoffs`: only rejected alternatives a reviewer would ask about.
- `## Blast Radius`: who or what it touches and why that is safe or risky.
- `## Verification`: each real run path and its outcome.

**Size.** Prefer five narrow PRs to one large PR. Branch from trunk for independent work.

**Readiness.** Open every PR ready, never as a draft, unless the harness defaults otherwise and you explicitly override it.
