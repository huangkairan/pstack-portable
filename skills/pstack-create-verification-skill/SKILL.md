---
name: pstack-create-verification-skill
description: "为当前项目创建可真实启动、操作、取证和清理的验证技能。"
---

先读取 [执行契约](references/contracts.md) 与 [宿主适配](references/host.md)，再按下列流程执行。

# create-verification-skill

1. 从源码发现用户界面、启动命令、已有测试与控制工具、可观察结果、隔离方式。只询问源码不能回答的必要环境信息。
2. 按宿主适配说明选择项目技能目录，生成 verify-<项目>/SKILL.md。包含 Launch、Doctor、Drive、Evidence、Cleanup、Helpers，命令来自实际项目，不用猜测的占位符。
3. 建立 3–5 个用户功能的地图，每项列前置条件、实际操作、预期、证据与清理。可用功能不足时按实际数量。
4. 完整运行至少一个功能：启动、检查环境、操作真实界面/CLI、断言、保留证据、清理本任务资源。清理后再次确认报告/截图仍存在。
5. 输出生成位置、已跑功能、未跑功能和缺少的工具。一个功能通过不能称整个地图通过；环境启动失败时保留失败证据。
