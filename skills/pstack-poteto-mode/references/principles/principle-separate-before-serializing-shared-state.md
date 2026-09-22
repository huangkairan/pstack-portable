# 先消除共享写，再考虑锁

适用：并发参与者写文件、分支或键时，先各自持有输出并在读取时聚合；必须共享单一对象时再用锁、单写者或 CAS。

并发参与者写文件、分支或键时，先各自持有输出并在读取时聚合；必须共享单一对象时再用锁、单写者或 CAS。

边界：文字约定不是并发控制。原则本身没有替所有 skill 自动建立隔离。

[上游原文](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md#L7-L16)
