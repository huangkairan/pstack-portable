# Guard the Context Window

When to apply: When large outputs and repeated reads crowd the main context.

Give bulk raw material to a subagent and keep summaries in the main thread. Expand frequently needed templates locally and limit phase size.

Boundary: Isolation can reduce main-context load without reducing total tokens. Inspect decisive original evidence yourself.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-guard-the-context-window/SKILL.md#L7-L17)
