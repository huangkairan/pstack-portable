---
name: pstack-create-verification-skill
description: "Create a project skill that can launch, operate, capture evidence, and clean up a real feature."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# create-verification-skill

1. Inspect the source for the user interface, launch command, existing tests and control tools, observable outcomes, and isolation method. Ask only for essential environment facts that the source cannot supply.
2. Choose the project skill location from the host adapter. Create verify-<project>/SKILL.md with Launch, Doctor, Drive, Evidence, Cleanup, and Helpers. Use commands found in the real project, not guessed placeholders.
3. Map three to five user-facing features. For each, record prerequisites, real actions, expectations, evidence, and cleanup. Use fewer entries when fewer features exist.
4. Run at least one feature end to end: launch, check the environment, operate the real UI or CLI, assert the result, save evidence, and clean up resources created by this task. Confirm that the report and captures still exist after cleanup.
5. Report the generated path, features run, features not run, and missing tools. Passing one feature does not validate the whole map. Preserve startup failure evidence when the environment will not launch.
