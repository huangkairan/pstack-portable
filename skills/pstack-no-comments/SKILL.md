---
name: pstack-no-comments
description: "Replace redundant code narration with clearer code while preserving valuable rationale and directives."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# no-comments

1. Review comments in the changed scope. Classify code narration, non-obvious rationale, protocol or compatibility constraints, documentation, license text, and tool directives.
2. Improve naming or structure before removing comments that merely repeat the code. Keep rationale the code cannot express clearly.
3. Preserve licenses, generator markers, compiler and linter directives, public API documentation, and evidenced constraints. Do not break behavior or widen the refactor to pursue zero comments.
4. Inspect the diff and run affected checks. Report what changed and why important comments remain. Do not make this workflow a mandatory step before every review.
