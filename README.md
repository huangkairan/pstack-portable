# pstack-portable

Lauren Tan 的 [pstack](https://github.com/cursor/plugins/tree/main/pstack) 的非官方 Claude Code / Codex 移植。固定上游 0.15.2、提交 `53e579f1481697931fc44f5445171397cfa2b24b`，保留 MIT 许可证。

24 个工作流使用一份共用正文，分别生成原生技能包。23 条原则作为按需参考，23 个 playbook 从 `pstack-poteto-mode` 选择。简单任务直接完成，设计竞赛与并行审查按需启用；不要求安装其他第三方技能。

这是有明确行为调整的移植，不是原版逐字复制。原始资料在 `vendor/pstack`，不作为运行指令加载。完整来源与状态见 [coverage.json](docs/coverage.json)，实测范围见 [验证记录](docs/validation.md)。

## 安装到项目

需要 Python 3.9+ 和已登录的目标宿主。安装器只写指定项目，不改用户全局设置；发现同名外来技能或本地修改时拒绝覆盖。

```bash
git clone git@github.com:huangkairan/pstack-portable.git
cd pstack-portable
python3 scripts/install.py --host codex --project /你的项目路径
python3 scripts/install.py --host claude-code --project /你的项目路径
```

在项目中启动新会话：

| 任务 | Codex | Claude Code 项目安装 |
|---|---|---|
| 理解系统 | `$pstack-how` | `/pstack-how` |
| 修 bug 并保留失败/通过证据 | `$pstack-tdd` | `/pstack-tdd` |
| 选择整套流程 | `$pstack-poteto-mode` | `/pstack-poteto-mode` |
| 创建项目验证能力 | `$pstack-create-verification-skill` | `/pstack-create-verification-skill` |
| 独立多代理调查 | `$pstack-swarm` | `/pstack-swarm` |
| 分析变更影响 | `$pstack-blast-radius` | `/pstack-blast-radius` |

先用 how、tdd 或 poteto-mode，无需记住全部入口。每个叶技能包包含自己的契约与适配说明，不依赖全局安装的其他技能。

## 原生插件包

```bash
python3 scripts/build.py
claude --plugin-dir ./dist/claude-code/pstack-portable
```

Claude 插件命名空间为 `/pstack-portable:pstack-how` 等；项目安装是 `/pstack-how`。避免同时装项目副本和插件副本，以免出现重复入口。

Codex 包在 `dist/codex/pstack-portable`，根目录 `.codex-plugin/plugin.json` 与生成的 `skills` 也可作为插件源。推荐先使用经过实测的项目安装路径；项目安装还提供 `.codex/agents`，插件发现本身不证明角色配置已注册。具体委派工具不支持命名角色时，适配层在原生子代理中传递角色职责，并保留父会话权限。

## 保留与调整

- 保留调查、动机追溯、设计比较、独立审查、回归证据、真实项目验证和决策记录。
- 原则改为参考材料；叶工作流不回调总模式。调用限制按宿主重写，不复制 Cursor frontmatter。
- 默认继承宿主模型。多个同模型代理是不同上下文，不声称跨模型复核。
- 不自动修改全局规则，不注册 hooks、定时器或后台服务，不把技能指令当作外部写入授权。
- 有价值的原因说明、许可证、工具指令和 API 文档保留，不机械追求零注释。
- 安装操作有进程内异常回滚；不宣称断电恢复或跨进程事务保证。更新前停止使用同一目标目录，安装不是并发更新服务。

## 可选确定性工具

```bash
python3 scripts/doctor.py --host codex
python3 scripts/worktree_audit.py /你的仓库路径
python3 scripts/check_plan.py plan.json
```

计划格式为 `{"goal":"目标","units":[{"id":"a","dependsOn":[],"deliverable":"产物","verify":"真实验证命令或路径"}]}`。检查器验证非空验收、依赖存在性与无环；不兼容上游固定十 lane 的 Markdown 模板，不证明计划已执行。

账本与 PR 监听复用上游实现，需要 Bun 与锁定依赖。首次使用显式安装；工具不自动联网下载：

```bash
cd tools
bun install --frozen-lockfile
bun orch/orch.ts --help
bun watch-pr/cli.ts --help
```

`orch` 管账本，不启动代理或核验结果；Graphite frontier 仍依赖 `gt`，普通账本不需要。`watch-pr` 通过 `gh` 读取 GitHub，不自动修复或合并。安装到项目后，工具副本位于 `pstack-poteto-mode/tools`；在该副本安装依赖会使安装器检测到本地变化并拒绝覆盖，保留旧副本后重新安装即可，不会自动清理用户文件。

## 外部集成边界

Cursor cloud worker、持久唤醒、GrokBot UI、Benny 的 Slack/tracker/控制环境没有伪造替代实现。相应流程保留输入、输出和阻塞条件，依赖目标宿主的真实能力与项目配置。[Benny 接口边界](docs/benny.md)。

`make-bot-ui` 缺少实际平台接口时返回阻塞。长期 playbook 能在当前会话推进并记录 checkpoint，不因此承诺退出后自动恢复。PR/发布/删除流程需要当前任务授权；本次测试没有执行这些外部动作。

## 开发与验证

`core` 是内容唯一来源，`adapters` 处理宿主差异，`scripts/build.py` 生成包。不要手改根目录 `skills` 或 `dist`。

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py --check
cd tools
bun install --frozen-lockfile
bun test orch watch-pr
bun run typecheck
```

真实模型测试为显式可选，会消耗当前账号额度；每个 Claude 测试预算上限 2 美元，每个测试默认 180 秒。输出目录必须不存在：

```bash
python3 tests/live_smoke.py --host codex --case tdd --output .test-runs/codex-tdd
python3 tests/live_smoke.py --host claude-code --case delegation --output .test-runs/claude-delegation
```

真实测试生成隔离 Git 项目，记录事件、退出状态与实际产物。脚本不会仅因模型退出码为零就宣称行为通过；仍需检查 Skill 加载、先失败再修改的顺序或独立委派的调用与终态。原始日志留在本机，不提交到仓库。
