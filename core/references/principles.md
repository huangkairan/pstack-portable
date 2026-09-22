# 按需读取的工程原则

只读取会改变当前决策的条目，不要求每次任务逐条加载。

- [少写代码，减少协调](principles/principle-laziness-protocol.md)：重构、评估改动规模、准备增加抽象时。
- [先确定数据结构与基础设施](principles/principle-foundational-thinking.md)：写逻辑前梳理类型、访问路径和并发共享；先删除废代码，再安排所有后续阶段受益的脚手架。
- [把新需求放回设计起点](principles/principle-redesign-from-first-principles.md)：整合需求前阅读受影响文件，思考如果需求从第一天就存在会怎样设计，再同步类型、引用、文档并增量交付。
- [重复失败后审视共同前提](principles/principle-attack-the-premise.md)：两个以上基于同一前提的修复都失败时，写出前提，用可重跑脚本统计各参与者的不平衡，再找角色分配机制。
- [先减后加](principles/principle-subtract-before-you-add.md)：演进系统时先清除死代码、冗余验证、空引用，再在简化后的结构上建设。
- [同时减少层次和隐藏状态](principles/principle-minimize-reader-load.md)：审查代码时统计追踪层数与读者需记住的可变状态，合并无压缩价值的转发层，缩小状态作用域。
- [以最终可验证状态组织迁移](principles/principle-outcome-oriented-execution.md)：明确阶段边界的重写和迁移可接受计划内、可逆的中间破坏；持续验证活跃区域，结束时做完整静态和运行验证。
- [从使用者体验取舍](principles/principle-experience-first.md)：产品和接口权衡时先看使用者收益，少做但打磨完整；把调用库的同事和未来维护者也视为用户。
- [有真实选择时比较多种方案](principles/principle-exhaust-the-design-space.md)：新交互或无既有范式的架构决策，构建 2–3 个结构不同的原型后再选。
- [把操作或验证变成可重跑工具](principles/principle-build-the-lever.md)：非琐碎工作先手做一单元学出方法，再写最小脚本并对照验证；有确定性批处理就不让大量 Agent 手工重复。
- [用结构表达领域](principles/principle-model-the-domain.md)：有状态逻辑或反复分支时，选择状态机、联合类型、表、reducer 或领域模块，减少非法状态和规则散落。
- [在边界验证，内部保持纯逻辑](principles/principle-boundary-discipline.md)：在 CLI、配置、网络和外部 API 解析输入；内部使用已验证类型，隔离框架外壳与纯业务函数。
- [让非法状态无法构造](principles/principle-type-system-discipline.md)：用联合类型、语义品牌类型、穷尽匹配和权威 schema 派生类型；只在部分函数真的可能失败处强化类型。
- [重复执行仍能收敛](principles/principle-make-operations-idempotent.md)：设计命令、生命周期和循环时逐项检查执行两次、半途崩溃再执行的结果；采用状态协调、存量接管或陈旧锁检测。
- [迁移调用方后删除旧 API](principles/principle-migrate-callers-then-delete-legacy-apis.md)：盘点所有调用方，在同一改造波次迁移并删除旧接口，更新契约测试。
- [先消除共享写，再考虑锁](principles/principle-separate-before-serializing-shared-state.md)：并发参与者写文件、分支或键时，先各自持有输出并在读取时聚合；必须共享单一对象时再用锁、单写者或 CAS。
- [直接验证真实产物](principles/principle-prove-it-works.md)：宣布完成前运行真实功能路径，检查输入到输出全链路；审阅委派者的实际 diff 或运行结果，能脚本化就保留重跑工具。
- [先复现，再修根因](principles/principle-fix-root-causes.md)：复现、连续追问原因、加仪表而非猜测；同类模式一并搜索。
- [每个单元都能被验证](principles/principle-sequence-verifiable-units.md)：把工作拆成可检查的小单元，验证后再推进；用失败测试→修复、基线→处理等提交顺序展示证据。
- [测试用户可观察行为](principles/principle-test-behavior-not-implementation.md)：用具体输入执行真实主体，对照独立的字面量预期；避免只检查 mock 调用次数、常量复述、自我计算预期。
- [把大体量阅读隔离出去](principles/principle-guard-the-context-window.md)：大输出与重复阅读挤占窗口时，把原始数据交给子代理，主线程保留摘要；常用模板就地展开，限制阶段规模。
- [可逆工作尽量先做后审](principles/principle-never-block-on-the-human.md)：对可逆编辑做合理判断，让人异步纠偏；只有无法推断意图的问题再问。
- [把重复教训变成机制](principles/principle-encode-lessons-in-structure.md)：同一纠正出现第二次时，优先变成不可表示状态、lint、规范 helper 或运行检查；能结构化就删去重复文字提醒。
