# Codex adapter

Use native skills. Explicit invocation is `$pstack-<capability>`. References in the current skill directory are ordinary files and require no other installed skill. A skill does not expand the user's authorization.

For investigation, candidate comparison, or independent review, explicitly request subagent work. Use the delegation, wait, message, and cancel tools actually exposed in the current session. Do not paste Cursor Task parameters into tool calls. If delegation is unavailable, disclose the limitation. Serial investigation is possible, but do not present it as independent review. Inherit the parent model and current permissions. Choose another model only when the host and current instructions allow it.

The project installer places `poteto-agent.toml` and `pstack-reviewer.toml` in `.codex/agents/`; the latter requests a read-only sandbox. Plugin discovery alone does not prove these profiles are registered. If a named profile is unavailable, use the host's native subagent with the role instructions and existing permissions. Do not disable the sandbox to compensate.

Generate project verification skills in `.agents/skills/verify-<project>/`. Read only records or handoff summaries explicitly in this task's scope. Durable tasks depend on actual host scheduling; otherwise save a checkpoint and state that background continuation is unavailable. This package does not change global rules, enable hooks, or schedule tasks.
