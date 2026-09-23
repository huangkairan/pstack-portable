# autonomous-run

Set a completion predicate, budget, stop condition, and durable task directory. Each round reads the checkpoint, inspects current state, advances one step, verifies it, and records evidence and the next step. Use host scheduling only when supported and authorized. Without cross-session wake-up, work in the current session and leave an explicit continuation point; do not claim a background service remains alive. A user stop ends this task’s delegation and external writes.
