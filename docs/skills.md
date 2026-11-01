# Skill catalog

Reference for every skill, agent, playbook, and script in this repo. Counts hold at this commit. Regenerate with:

```sh
ls skills/ | wc -l
ls agents/ skills/poteto-mode/playbooks/ scripts/
```

## Routers

| Name | Purpose |
|---|---|
| `gtan-mode` | Product router. Frames the request, runs plan reviews, files specs, hands to `poteto-mode`. |
| `poteto-mode` | Engineering router. Matches tasks to skills or playbooks, owns todos, enforces verify and no-push. |

## Product skills

| Name | Purpose |
|---|---|
| `office-hours` | Reframes vague ideas with forcing questions. Writes the design doc. |
| `plan-ceo-review` | Rethinks scope in four modes from Expansion to Reduction. |
| `plan-eng-review` | Locks architecture, data flow, edge cases, and the test plan. |
| `plan-devex-review` | Reviews developer experience against personas and TTHW benchmarks. |
| `plan-design-review` | Rates design dimensions 0-10 with AI-slop detection. |
| `design-consultation` | Builds a design system from scratch. Writes `DESIGN.md`. |
| `spec` | Turns intent into a filed executable spec in five phases. |
| `security-review` | Security audit with evidence. Report and repair proposals. |

## Engineering playbooks

These live under `skills/poteto-mode/playbooks/`.

| Name | Purpose |
|---|---|
| `bug-fix` | Reproduces, binary-searches the cause, fixes, verifies on the same surface. |
| `feature` | Designs, delegates behind a throughput checkpoint, verifies, stacks commits. |
| `refactoring` | Pins the behavior contract first, reshapes, proves equivalence. |
| `investigation` | Read-only cited answer. No code change. |
| `prototype` | Throwaway build to settle a decision cheaply. |
| `opening-a-pr` | Commit shape, PR body sections, readiness. Runs at the end of every playbook. |

## Workflow skills

| Name | Purpose |
|---|---|
| `advisor` | Second opinion from another model at checkpoints. |
| `architect` | Types and module shape before code. |
| `benchmark-checklist` | Vets a perf number before you report it. |
| `blast-radius` | Finds what a change could break beyond the diff. |
| `cli-for-agents` | Designs CLIs that agents can run headlessly. |
| `correct` | Makes a repeated mistake impossible through structure. |
| `figure-it-out` | Designs a bespoke playbook when none fits. |
| `how` | How a subsystem works and where code should live. |
| `interrogate` | Adversarial review. Only findings proven by a run survive. |
| `no-comments` | Strips comments before review. Keeps survive only with proof. |
| `reflect` | Mines the session for durable learnings. Routes them into skill edits. |
| `sharpen` | Deepens the prompt before spending tokens. |
| `statechart` | Checks a TLA+ model of states and draws a Mermaid statechart with shortest bug paths. |
| `tdd` | Failing test first, only where the test path is cheap. |
| `teach` | Explains a subsystem so a person understands it. |
| `technical-writing` | Layered standard for docs, readmes, and PR bodies. |
| `unslop` | Removes AI tells from writing. |
| `verify-this` | Verifies a claim with fresh evidence. Returns a verdict. |
| `why` | Design rationale from parallel evidence queries. |

## Review bundle

| Name | Purpose |
|---|---|
| `thermos` | Runs both thermo-nuclear reviews in parallel. Synthesizes. |
| `thermo-nuclear-review` | Security and correctness audit of branch changes. |
| `thermo-nuclear-code-quality-review` | Strict maintainability audit. |

## Principles

24 skills named `principle-*`. Each states when it applies. Read the leaf skill in full before citing it. Names: `attack-the-premise`, `boundary-discipline`, `build-the-lever`, `encode-lessons-in-structure`, `exhaust-the-design-space`, `experience-first`, `explain-the-number`, `fix-root-causes`, `foundational-thinking`, `guard-the-context-window`, `laziness-protocol`, `make-operations-idempotent`, `migrate-callers-then-delete-legacy-apis`, `minimize-reader-load`, `model-the-domain`, `never-block-on-the-human`, `outcome-oriented-execution`, `prove-it-works`, `redesign-from-first-principles`, `separate-before-serializing-shared-state`, `sequence-verifiable-units`, `subtract-before-you-add`, `test-behavior-not-implementation`, `type-system-discipline`.

## Agents

| Name | Purpose |
|---|---|
| `poteto-agent` | Delegate for `poteto-mode` playbook steps. Reads the mode skill first. |
| `thermo-nuclear-review-subagent` | Delegate for bug and security review findings. |
| `thermo-nuclear-code-quality-review-subagent` | Delegate for maintainability review findings. |

## Scripts

| Name | Purpose |
|---|---|
| `scripts/pre-push` | Refuses pushes that carry `wip:` handoff commits. |
