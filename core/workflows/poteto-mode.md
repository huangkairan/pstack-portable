# poteto-mode

1. 读取 references/playbooks/index.md，选择与本次目标匹配的一条流程。小任务直接完成，不为所有函数改动启动架构竞赛。
2. 读取所选 playbook，列出任务特有的完成条件。只有遇到对应设计或验证问题时才读取 references/principles.md 中的相关原则。
3. 工作流位于 references/workflows/，可直接读取所需流程，不要求调用其他已安装技能。叶流程不回调此入口。
4. 按任务复杂度选择本地执行或原生委派；默认模型继承、最多两名并行 worker。需要更多时先结合现有授权与预算决定。
5. 完成后报告产物、真实验证和未完成项。该入口仅作用于当前任务；不修改全局指令，不自动发送消息、开 PR、合并或部署。

常用路径：理解系统→how；修 bug→bug-fix playbook；新行为→feature；复杂结构→architect；变更审查→blast-radius；项目验证→create-verification-skill。
