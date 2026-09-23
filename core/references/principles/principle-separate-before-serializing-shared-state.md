# Separate Before Serializing Shared State

When to apply: When concurrent actors write a file, branch, key, or object.

Give each actor separate output and aggregate at read time. If sharing one object is unavoidable, use a real lock, single writer, or compare-and-swap.

Boundary: A prose agreement is not concurrency control. This principle does not automatically isolate other skills.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md#L7-L16)
