# Test Behavior, Not Implementation

When to apply: When writing or reviewing a test.

Execute a real subject with concrete input and compare it with an independent literal expectation. Avoid assertions that only count mock calls, restate constants, or compute their own expected value using the same logic.

Boundary: The “would it pass if every function returned undefined?” question is a heuristic, not a theorem. A matcher is not automatically wrong in isolation.

[Upstream source](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-test-behavior-not-implementation/SKILL.md#L7-L25)
