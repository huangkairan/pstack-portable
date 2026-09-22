# Claude Code 适配

使用原生 Skill 发现入口；插件调用为 /pstack-portable:pstack-<能力>。可直接读取当前技能目录中的 references，无需调用同名其他技能。所有迁移入口可以自动选择；执行外部动作仍须来自本次任务授权。

需要独立子代理时按实际暴露的 Agent 工具 schema 调用，使用当前会话允许的角色与模型。不要照搬 Cursor Task 的 readonly、environment、run_in_background 参数。模型默认继承；多个相同模型角色只算独立上下文，不算跨模型复核。对子代理的工具权限使用宿主真正支持的配置；prompt 中的“只读”不能充当沙箱。

原生插件 agents/pstack-reviewer.md 提供只读工具集合，agents/poteto-agent.md 提供执行角色。插件 agent 的 permissionMode/hooks/mcpServers 不作为有效隔离配置。后台委派必须收集终态与产物后再汇报。无需嵌套时主会话扁平调度。

生成项目技能使用 .claude/skills/verify-<项目>/。历史输入由用户提供路径或当前任务可访问的 transcript 定位，不扫描其他项目会话。持续任务只使用已验证的宿主调度；会话结束后的唤醒与恢复必须另行验收。此插件不安装 hooks 或定时任务，不暗中启用自动化。
