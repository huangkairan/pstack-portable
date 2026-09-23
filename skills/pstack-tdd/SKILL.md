---
name: pstack-tdd
description: "Fix a bug through an observed failing check followed by a passing regression."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# tdd

1. Read the intended behavior, existing implementation, and test conventions. Choose the smallest reproduction through a real entry point.
2. Add a behavioral test or rerunnable check first. Run it before production changes, preserve the failing output, and confirm that it fails for the target bug.
3. Make the smallest fix. Keep correct assertions; do not change expected behavior to accommodate a broken implementation.
4. Rerun the focused check until it passes, then run nearby checks relevant to the change.
5. Report the before and after commands and observations. If a test would require disproportionate scaffolding, explain why and choose a real user action or targeted script. Without before-failure evidence, say the regression was not demonstrated rather than inventing it.
