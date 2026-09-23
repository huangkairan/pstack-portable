---
name: pstack-why
description: "Trace the historical reasons for a code or design decision using commits and records."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# why

1. Locate the current behavior and its callers. List the decisions that require explanation.
2. Use git blame, git log -S/-G, related commits, and accessible PRs or design records to trace when behavior appeared and changed. State the versions and scope investigated.
3. Separate an author's stated reason, a historical constraint, and a reason inferred from source. Preserve unknowns when the original motivation is unavailable.
4. Compare historical and current constraints. If the user asks whether to change course, give current evidence, alternatives, and costs. A read-only investigation does not implement the change.
5. Report the decision timeline, source references, constraints that still apply, and assumptions requiring verification.
