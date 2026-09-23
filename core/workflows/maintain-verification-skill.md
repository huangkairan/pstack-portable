# maintain-verification-skill

1. Read the existing verification skill and feature map. Find stale commands, selectors, prerequisites, or evidence checks. Run the smallest affected path to reproduce the issue.
2. Determine whether the product contract actually changed. A failed check can expose a product regression; do not automatically weaken the assertion.
3. Update steps or helpers supported by evidence, remove superseded content, and update callers and references.
4. Rerun affected features, verify that evidence survives cleanup, and report the changed and tested scope. Periodic maintenance requires a separately configured real scheduler; this skill is not a resident process.
