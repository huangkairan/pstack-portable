---
name: pstack-setup-pstack
description: "Inspect host and project capabilities and configure bounded pstack roles and concurrency."
---

Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.

# setup-pstack

1. Read the host adapter and inspect the CLI, git, available verification tools, and project layout. You may run python3 scripts/doctor.py --host <codex|claude-code>; locate that script relative to the installed package.
2. CLI availability does not prove authentication, delegation, or permissions. Run real model tasks only when the user has requested testing and cost is bounded. Mark missing capabilities unknown or unavailable.
3. Inherit the host model by default, with two workers and two review rounds. If project configuration is useful, write .pstack.json in that project with maxWorkers and maxRounds. Use only verified host model names; do not guess a translation of Cursor model IDs.
4. Distinguish reading files, running commands, writing the project, delegating, using control tools, and waking across sessions. Configuration cannot grant permissions or invent a capability.
5. Return available capabilities, unverified items, and the smallest next action. Do not rewrite global rules or existing model settings.
