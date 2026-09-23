# orchestrate

Run one end-to-end pilot to prove briefs, artifacts, real verification, and integration. Track goal, base revision, owner, state, evidence, and questions per unit. tools/orch is an optional ledger; its CLI neither starts agents nor verifies evidence. The host schedules bounded parallelism and one coordinator integrates results. After two retries for the same reason, record the block. Graphite frontier is a separate dependency; without it, maintain the queue using verified git or gh data. Cross-session operation needs an actual scheduler and tested recovery.
