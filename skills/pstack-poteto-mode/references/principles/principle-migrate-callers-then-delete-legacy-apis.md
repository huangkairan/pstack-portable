# Migrate Callers, Then Delete Legacy APIs

When to apply: When changing an internal API.

Inventory callers, migrate them in the same change, delete the old interface, and update contract tests.

Boundary: Apply only when there are no external compatibility consumers and the coordination cost is acceptable. Do not silently apply this to public APIs.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md#L7-L22)
