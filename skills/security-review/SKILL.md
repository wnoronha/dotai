---
name: security-review
description: "Security audit with evidence before assurance. Application model, attack-surface census, scope-dependent phases, independent challenge, report with repair candidates. Use for any auth, payments, PII, or pre-ship review."
---

# Gtan CSO

## Flow (always run)

- **Phase 0:** application model and readiness.
- **Phase 1:** attack-surface census.
- **Phases 2–11:** scope-dependent audit (OWASP + STRIDE), selected by resolved mode.
- **Phase 12:** evidence rubric and independent challenge.
- **Phase 13:** report and repair candidates.
- **Phase 14:** rechecks against current source.

## Rules

- Evidence before assurance. No finding without a supported trace.
- Static assessment always available. Runtime/scanner execution only with qualified, contained tooling.
- Repair candidates are reviewable proposals, never auto-applied.

Source: `~/code/gstack/cso/SKILL.md` + `sections/audit-phases.md`. Upstream ships a Bun launcher; this wrapper uses the phase protocol only.
