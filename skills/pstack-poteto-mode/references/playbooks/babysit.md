# babysit

先声明 check（一次只读快照）、threads-only（评论处理）、drive（推进就绪）或 background（需真实调度）。普通查询选 check。读取最低未合并 PR 的冲突、评论和 CI，逐项判断真实问题，批量修复后重新核对当前 SHA。只在已授权时推送或回复，不合并、不变栈拓扑；flake 最多一次有依据重跑。监听可选 tools/watch-pr，监听不等于修复。
