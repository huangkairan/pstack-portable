---
name: pstack-setup-pstack
description: "检查 pstack 的宿主、工具和项目能力，配置有限并发与模型角色。"
---

先读取 [执行契约](references/contracts.md) 与 [宿主适配](references/host.md)，再按下列流程执行。

# setup-pstack

1. 读取当前宿主适配说明，检查 CLI、git、可用验证工具和项目结构。可运行 python3 scripts/doctor.py --host <codex|claude-code>；安装包路径按实际位置定位。
2. CLI 存在不证明登录、委派或权限有效。只在用户要求测试且成本受控时执行真实模型任务；缺能力明确标记 unknown 或 unavailable。
3. 默认继承宿主模型，两名 worker、两轮复核。若需项目配置，写入用户项目 .pstack.json，字段 maxWorkers、maxRounds；模型仅作为经核实的宿主配置，不猜测 Cursor 型号映射。
4. 区分可读取、可运行命令、可写项目、可委派、可调用控制工具、可跨会话唤醒。配置不能授予权限，也不能伪造能力。
5. 返回可用能力、未验证项和最小后续动作；不改用户全局规则或已有模型配置。
