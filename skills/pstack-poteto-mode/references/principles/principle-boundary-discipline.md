# Boundary Discipline

When to apply: When parsing CLI, configuration, network, or API input.

Validate external data at the boundary, then use verified internal types. Keep framework integration separate from pure domain logic.

Boundary: Trusting internal types depends on complete boundary validation; do not remove checks on external input.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-boundary-discipline/SKILL.md#L7-L34)
