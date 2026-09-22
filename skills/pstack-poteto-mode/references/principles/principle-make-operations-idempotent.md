# 重复执行仍能收敛

适用：设计命令、生命周期和循环时逐项检查执行两次、半途崩溃再执行的结果；采用状态协调、存量接管或陈旧锁检测。

设计命令、生命周期和循环时逐项检查执行两次、半途崩溃再执行的结果；采用状态协调、存量接管或陈旧锁检测。

边界：这些是设计要求，不是已经提供幂等执行平台；具体副作用仍要逐项证明。

[上游原文](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-make-operations-idempotent/SKILL.md#L7-L24)
