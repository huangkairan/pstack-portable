---
name: pstack-figure-it-out
description: "为跨阶段迁移或没有现成流程的复杂任务制定并执行可验证计划。"
---

先读取 [执行契约](references/contracts.md) 与 [宿主适配](references/host.md)，再按下列流程执行。

# figure-it-out

1. 写可证伪的完成条件、范围、基线、规模和关键未知项。先找现有检查，再决定需要的最小验证工具。
2. 拆成每个都能结束于实测的交付单元，明确依赖和回退点；仅在结构性决策需要时读取 architect 流程。
3. 每轮记录假设、改动、实际结果、保留或回退的理由。持续失败时重审共同前提，不继续堆补丁。
4. 多轮工作保存 checkpoint 和决策日志，包含当前 revision、证据位置、未完成项和下一步。持久唤醒不由此流程提供。
5. 逐单元复验后在真实目标上验证整体。输出 VERIFIED/NOT_VERIFIED/INCONCLUSIVE/BLOCKED 状态及依据，不以计划执行完毕代替完成条件。

按流程需要读取：
- [architect](references/workflows/architect.md)
- [arena](references/workflows/arena.md)
