# Claude Code adapter

Use native Skill discovery. From a plugin, an entry is `/pstack-portable:pstack-<capability>`; from a project or global skills directory, it is `/pstack-<capability>`. Read references in the current skill directory directly. Do not require a separate installed skill. Current task authorization still governs external actions.

For independent work, use the actual Agent tool schema exposed in the session and native model choices. Do not copy Cursor Task fields such as `readonly`, `environment`, or `run_in_background`. Inherit the session model by default. Multiple agents on the same model provide separate contexts, not cross-model verification. Enforce tool permissions through host-supported configuration; a prompt saying “read-only” is not a sandbox.

The plugin's agents/pstack-reviewer.md provides a read-only tool set, and agents/poteto-agent.md provides an execution role. `permissionMode`, `hooks`, and `mcpServers` in plugin-agent frontmatter are not effective isolation settings. Collect a background agent's terminal state and artifact before reporting completion. When nesting is unnecessary, coordinate workers from the main session.

Generate project verification skills in `.claude/skills/verify-<project>/`. Receive a transcript path from the user or locate only the current task's accessible record; do not scan other projects' sessions. Use durable scheduling only when that host facility has been verified. Cross-session wake-up and recovery require separate acceptance. This package installs no hooks or schedules and does not silently enable automation.
