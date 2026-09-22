# 在边界验证，内部保持纯逻辑

适用：在 CLI、配置、网络和外部 API 解析输入；内部使用已验证类型，隔离框架外壳与纯业务函数。

在 CLI、配置、网络和外部 API 解析输入；内部使用已验证类型，隔离框架外壳与纯业务函数。

边界：“信任内部类型”以边界完整为前提，不能据此删除外部数据校验。

[上游原文](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-boundary-discipline/SKILL.md#L7-L34)
