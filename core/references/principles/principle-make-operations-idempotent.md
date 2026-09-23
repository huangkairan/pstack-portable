# Make Operations Idempotent

When to apply: When designing commands, lifecycles, or loops that may retry after a crash.

Check the result of running twice and of resuming after a partial execution. Reconcile state, take over existing work where appropriate, and detect stale locks.

Boundary: These are design requirements, not an already-provided idempotent runtime. Prove each external side effect separately.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-make-operations-idempotent/SKILL.md#L7-L24)
