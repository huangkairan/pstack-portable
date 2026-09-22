# 把大体量阅读隔离出去

适用：大输出与重复阅读挤占窗口时，把原始数据交给子代理，主线程保留摘要；常用模板就地展开，限制阶段规模。

大输出与重复阅读挤占窗口时，把原始数据交给子代理，主线程保留摘要；常用模板就地展开，限制阶段规模。

边界：隔离减少主窗口负担，未必减少总 token；仍要检查关键原始证据。

[上游原文](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-guard-the-context-window/SKILL.md#L7-L17)
