# Minimize Reader Load

When to apply: When code is hard to trace.

Count the layers a reader must follow and the mutable state they must remember. Collapse pass-through layers that add no compression and shrink state scope.

Boundary: A flat file can still hide global state. The aim is not to ban deep modules; Guard the Context Window is related.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-minimize-reader-load/SKILL.md#L7-L23)
