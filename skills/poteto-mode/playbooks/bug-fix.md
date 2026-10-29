### Bug fix

**You own this task. Plan, review, verify.** Delegate investigation and the fix, stay in the lead.

1. Reproduce it yourself on the real surface first. If it won't reproduce directly, tighten conditions or instrument until it fires.
2. Binary-search the cause. Seed hypotheses with `how` over the affected subsystem and `why` for regression history. Rule out with runtime evidence until one mechanism survives. Don't guess.
3. Plan the fix. If it crosses a function boundary, run `architect` first. Delegate implementation to a fresh `poteto-agent` with a specific scope (files, behavior to change, success criteria).
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass.
5. Stage commits so a failing test lands before the fix when the bug has a cheap local test path. See `tdd`. Skip it when the test would be expensive or integration-heavy.
6. Run **Opening a PR**.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing output verbatim.
