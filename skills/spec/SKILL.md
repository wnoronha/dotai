---
name: spec
description: "Vague intent to executable spec in five phases (why, scope, technical with code-reading, draft, file). Quality gate before filing, secret redaction, dedupe. Use to file backlog-ready issues."
---

# Gtan spec

## Process (do not skip phases)

1. **Why:** intent, problem, non-goals.
2. **Scope:** in/out, acceptance criteria.
3. **Technical:** mandatory code-reading; name files, symbols, integration points.
4. **Draft:** precise spec; confirm with user.
5. **File:** quality gate, secret redaction (always runs), dedupe against existing issues, then file.

## Flags

- `--dedupe` (default ON): check for near-duplicates first.
- `--no-gate`: skip quality gate (redaction still runs; no flag disables it).
- `--execute`: file then build via `poteto-mode` in a fresh scope.

## Output

Filed issue + spec path. `poteto-mode` picks it up for build. `ship` auto-close behavior intentionally omitted — manual PR gate stands.

Source: `~/code/gstack/spec/SKILL.md` (646 lines).
