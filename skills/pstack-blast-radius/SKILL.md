---
name: pstack-blast-radius
description: "Trace a change beyond its diff and test the assumptions on which its safety depends."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# blast-radius

1. Fix the diff base and target revision. Identify one or two facts on which the change's safety depends.
2. Trace callers, data fields, protocols, databases, async ordering, cross-language consumers, and locked dependency versions. Use commit history for constraints that a text search misses.
3. For each credible risk, state its trigger, impact, and cheapest useful check. Run a focused check against real code without expanding implementation for hypothetical risks.
4. Distinguish an assertion, source inference, runnable example, actual code execution, and observation on the user path. Do not call safety proven without executing the real code.
5. Report real risks, ruled-out cases, evidence level, and the minimum remaining checks before merge.
