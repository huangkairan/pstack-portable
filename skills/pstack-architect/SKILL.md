---
name: pstack-architect
description: "Design module boundaries, core types, and interfaces from caller usage for substantial architecture decisions."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# architect

1. Read the relevant implementation and callers. Summarize current boundaries and constraints; define external interfaces for greenfield work. No other skill is required first.
2. Write the caller's usage before core types, function signatures, ownership, and error boundaries. Compare at least two structurally different designs, including the complexity each removes or adds.
3. If the user requests parallel design exploration or the decision is costly, read the arena workflow and run isolated candidates. Compare ordinary designs in the current context.
4. Check for shallow modules, leaked internals, pass-through layers, and modules divided only by execution phase. Select a base and state what to adopt or reject.
5. Deliver the design, usage example, tradeoffs, alternatives, risks, and verification approach. Stop at the design when that is all the user requested; when implementation is authorized, make the smallest complete change and verify it. Revisit the premise if the same friction persists.

Read when this workflow requires it:
- [arena](references/workflows/arena.md)
