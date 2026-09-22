---
name: pstack-typescript-best-practices
description: "在 TypeScript 实现或审查中改进边界、类型与可维护性。"
---

先读取 [执行契约](references/contracts.md) 与 [宿主适配](references/host.md)，再按下列流程执行。

# typescript-best-practices

1. 读取项目 tsconfig、现有约定与目标代码，沿用已有类型和库。
2. 外部输入先验证并缩窄；内部使用可信类型。用判别联合表示互斥状态，避免不受约束的 any、掩盖错误的断言和无必要的可空字段。
3. 让公开签名表达实际契约，保持模块内部实现可替换；不为少量相似语句引入复杂泛型。
4. 运行项目已有类型检查及相关行为检查，区分编译正确与运行正确。类型改动同时更新调用者。

检查具体类型设计时读取 [类型规则](references/typescript.md)。
