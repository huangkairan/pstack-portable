# Laziness Protocol

When to apply: When refactoring, sizing a diff, or adding abstractions.

Prefer deletion and centralize decisions that would otherwise repeat. Check whether a new signal truly needs to pass through multiple layers.

Boundary: Less code means less complexity, not missing required behavior. File and layer counts are heuristics.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-laziness-protocol/SKILL.md#L7-L18)
