---
name: pstack-how
description: "Explain a system mechanism, call chain, data ownership, or module boundary from source."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# how

1. Define the question, entry point, expected output, and scope. For a single-module question, read its callers, implementation, and tests yourself. When scope is unclear, start with the smallest useful interpretation. Keep this workflow read-only.
2. For a cross-module question, divide the system into two to four distinct angles and delegate read-only exploration through the host adapter. Each explorer reports the entry point, call chain, data changes, boundaries, files read, and unknowns. If delegation is unavailable, cover the angles serially and say so.
3. Check conflicting findings against actual source. Separate static inference from observed runtime behavior. Design motivation requires historical evidence; do not infer author intent from the current implementation alone.
4. Explain the mechanism, key concepts, execution path, file and symbol locations, boundaries, and unresolved points. Cite paths and lines you actually read without dumping annotated source.
