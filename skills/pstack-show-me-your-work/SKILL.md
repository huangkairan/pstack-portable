---
name: pstack-show-me-your-work
description: "Keep a reviewable decision log and actual evidence for multi-round work."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# show-me-your-work

1. Create decisions.tsv in the task directory with time, revision, question, action, evidence, result, and next columns. Record one decision per row; replace embedded tabs and newlines with spaces.
2. Record observations rather than intentions: what ran, what happened, and why the change was kept or reverted. Point evidence to durable files or rerunnable commands.
3. At each phase boundary, check claims against the current artifact and the revision behind the evidence. Preserve failures and unknown states; separate inference from observation.
4. Return a short decision summary, reviewable evidence, and unfinished work. Commit the log only when the user requests an auditable commit. Do not publish it automatically.
