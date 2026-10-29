### Feature

**You own the design. Plan, review, verify.** Delegate implementation. Stay in the lead.

1. `how` over the affected subsystem.
2. `architect` for parallel design exploration when the shape is unclear.
3. Write the throughput checkpoint as todos: blocking first steps, independent workstreams, shared mutable state, smallest safe decomposition. A dimension that genuinely does not apply keeps its item with `n/a: <reason>`.
4. Delegate code-writing to a fresh `poteto-agent` with a specific scope (file paths, named data shape per `principle-model-the-domain`, success criteria). Commit liberally.
5. Verify on the real surface. "Inconclusive" or wrong-surface is not a pass.
6. Rebase into small, ordered commits per `principle-sequence-verifiable-units`.
7. If the design is contested, run `interrogate` before shipping.
8. Run **Opening a PR**.

**Reply:** what you built, what you chose and why, open decisions.
