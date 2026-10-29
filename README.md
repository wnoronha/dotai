# dotai

A curated personal agent stack. Two routers split the work: `gtan-mode` owns product thinking, `poteto-mode` owns engineering. Everything else is a skill they call.

## How it is organized

Product thinking lives in `skills/gtan-mode/` and eight leaf skills (`office-hours`, four `plan-*` reviews, `design-consultation`, `spec`, `security-review`). Engineering lives in `skills/poteto-mode/` with six playbooks and the `poteto-agent` delegate in `agents/`. Shared workflow skills (`how`, `why`, `architect`, `interrogate`) and 24 `principle-*` skills serve both routers. The full catalog is in `docs/skills.md`.

Session handoffs are `wip:` commits, never files. The `pre-push` hook in `scripts/` refuses to push them. `poteto-mode` defines the protocol.

## Start here

New initiative or contested direction: start in `gtan-mode`. Straightforward build or fix: start in `poteto-mode`. Unsure: start in `poteto-mode` and it routes you.

Install steps are in `docs/install.md`. The mode split is explained in `docs/modes.md`.

## Contents

55 skills, 3 agents, 6 playbooks, 1 script. Counts hold at this commit. Regenerate with:

```sh
ls skills/ | wc -l
ls agents/
ls skills/poteto-mode/playbooks/
```
