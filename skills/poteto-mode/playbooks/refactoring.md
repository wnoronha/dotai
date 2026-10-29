### Refactoring

**You own the contract. The structure changes. The behavior does not.**

If the cleanup reveals a missing feature or a real bug, split it out and ship the structural change first against the pinned contract.

1. Pin the behavior contract first. Run `how` over the subsystem, then write a characterization test or equivalence check capturing current behavior before any structure moves.
2. Name the structure the code is missing per `principle-model-the-domain`.
3. Name the target shape per `principle-foundational-thinking`. If it crosses a function boundary, run `architect` first.
4. Subtract before you add per `principle-subtract-before-you-add`. Smallest change that reaches the target ships.
5. Move in small behavior-preserving steps, each keeping the pin green. Migrate every caller and delete the old API in the same wave per `principle-migrate-callers-then-delete-legacy-apis`. No compatibility shims.
6. Prove behavior is unchanged on the real artifact per `principle-prove-it-works`.
7. Confirm reduced reader load per `principle-minimize-reader-load`. If the diff does not lower it somewhere, revert it.
8. Rebase into small ordered commits. Run **Opening a PR**.

**Reply:** structure changed, pin held, equivalence proof, what shipped and what got reverted. No new behavior.
