# 测试用户可观察行为

适用：用具体输入执行真实主体，对照独立的字面量预期；避免只检查 mock 调用次数、常量复述、自我计算预期。

用具体输入执行真实主体，对照独立的字面量预期；避免只检查 mock 调用次数、常量复述、自我计算预期。

边界：“函数全返回 undefined 是否仍通过”是启发式，不是严格定理。原文将部分断言列为弱测试，不意味着单个匹配器一律有错。

[上游原文](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-test-behavior-not-implementation/SKILL.md#L7-L25)
