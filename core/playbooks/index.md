# 流程索引

只读取匹配当前任务的一个流程；需要相关叶流程时读取 ../workflows/ 对应文件。

- [investigation](investigation.md)：读取 workflows/how.md 调查机制；只有问题涉及历史动机才读取 workflows/why.md。
- [bug-fix](bug-fix.md)：在用户报告的同一界面或 CLI 路径复现并保留失败证据。
- [perf-issue](perf-issue.md)：固定负载、版本、机器与测量方法，采集基线。
- [hillclimb](hillclimb.md)：明确指标、目标、预算与停止条件。
- [runtime-forensics](runtime-forensics.md)：明确诊断范围、目标进程和允许的采集方式。
- [trace-forensics](trace-forensics.md)：识别用户提供的采集格式与版本，选现有解析器查询热点、保留链或等待链，映射到已核实源码。
- [feature](feature.md)：写用户可观察的完成条件，读取现有实现并确定数据结构。
- [refactoring](refactoring.md)：先用现有行为检查锁定契约，定义结构性收益。
- [prototype](prototype.md)：明确需要观察才能决定的问题与最低成本实验。
- [visual-parity](visual-parity.md)：先固定基线、浏览器/字体/视口/设备缩放和数据。
- [authoring-a-skill](authoring-a-skill.md)：从实际请求确定触发、输入、产物和边界，按宿主 SKILL.md 格式编写。
- [eval](eval.md)：固定原始任务、输入、预算与评分标准，候选只收到自然任务，不泄露期望答案。
- [babysit](babysit.md)：先声明 check（一次只读快照）、threads-only（评论处理）、drive（推进就绪）或 background（需真实调度）。
- [shipping](shipping.md)：必须有本任务合并授权。
- [autonomous-run](autonomous-run.md)：明确完成谓词、预算、停止条件与持久任务目录。
- [orchestrate](orchestrate.md)：先执行一个端到端 pilot，确认 brief、产物、真实验证和集成路径。
- [autopilot-full](autopilot-full.md)：先确认当前范围含每个目标 PR 的创建、推送和合并。
- [autopilot-stack](autopilot-stack.md)：按固定基线拆任务，每个 owner 独立实现并提交证据。
- [session-pickup](session-pickup.md)：读取明确范围的交接记录，再核查实际分支、HEAD、未提交文件、进程、PR 与证据。
- [pause-safely](pause-safely.md)：仅在用户明确暂停或实际会话交接时使用。
- [multi-phase-plan](multi-phase-plan.md)：仅产出计划时不实施。
- [worktree-cleanup](worktree-cleanup.md)：先运行只读 scripts/worktree_audit.py <仓库> 列出路径、分支、dirty 状态。
- [opening-a-pr](opening-a-pr.md)：检查当前分支与变更范围，核对证据对应最终版本。
