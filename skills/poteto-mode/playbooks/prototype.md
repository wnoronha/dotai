### Prototype

**You own the design decision, not the code. The prototype is throwaway. The real build follows Feature.**

1. Scope the decision the prototype exists to make. No decision means no prototype. Route to Feature.
2. Build throwaway in an isolated scratch dir, separate from production source. Smallest script or sketch that exercises the question. No tests, no abstractions.
3. When comparing alternatives, build them behind one switcher per `principle-exhaust-the-design-space`.
4. Verify by observing the thing being decided (output, timing, render). The observation is the test here.
5. Present alternatives, tradeoffs, and a recommendation. Hand the chosen direction to **Feature** for the real build.

**Reply:** variants explored, evidence, tradeoffs, recommendation, scratch path. Say plainly the prototype is throwaway.
