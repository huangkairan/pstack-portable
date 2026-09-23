# Validation record

Date: 2026-09-22. Environment: macOS, Codex CLI 0.155.1, Claude Code 2.1.278, Bun 1.3.14. Real model tests ran in isolated Git projects. A later global-skill discovery check ran on Claude Code 2.1.280. These tests did not modify an ordinary business project.

## Verified

| Surface | Result | What it establishes |
|---|---|---|
| Port tests | 16 passed | Both project installers, Claude Code global install and update, foreign-file collisions, local changes, symlink protection, write and marker-commit rollback, plan dependencies, worktree paths with spaces, reference links, upstream inventory coverage, and English active content. |
| Preserved tools | 52 passed, 206 assertions | `orch` ledger and CLI plus `watch-pr` policy, parsing, and CLI. External GitHub and Graphite calls use test doubles. |
| TypeScript | Type check passed | The scope defined by the upstream `watch-pr` tsconfig. |
| Packaging | 24 skills passed `quick_validate`; Codex manifest and Claude plugin validation passed | Format and manifests, not complete behavioral acceptance for every skill. |
| Codex TDD | Passed | Loaded `pstack-tdd`, added and ran a failing regression before changing implementation, then passed 3 tests. |
| Claude TDD | Passed | Native Skill invocation loaded `pstack-tdd`, read its contract and adapter, observed failure before the fix, then passed 4 tests. |
| Claude plugin delegation | Passed | Native plugin discovery; two `pstack-portable:pstack-reviewer` agents started, each read a different file, and both completed. |
| Claude global skill discovery | Passed | A fresh session invoked `/pstack-how`, read the contract and adapter under `~/.claude/skills/pstack-how`, and read an isolated project's `calc.py`. |
| Codex delegation | Passed | Two native spawns. Two separate child sessions each read its assigned file and produced `final_answer` and `task_complete`; the parent waited and synthesized results. |

An independent check after both TDD runs also covered an empty cart, excessive discount, normal discount, and normal subtotal. All passed. Only `cart.py` and `test_cart.py` had tracked changes.

The first ephemeral Codex delegation run did not expose enough spawn detail in its JSONL output, so the model's final answer was not accepted alone. A second run retained the parent and child transcripts. Two spawn events, their separate reads, and two child completion events supported the result. The exposed tool did not allow a named role parameter; the parent passed read-only role instructions to native subagents while the run used a read-only sandbox. This proves native delegation, not named instantiation of the custom TOML role.

Claude's first test under `--bare` did not load the existing authentication setup and reported a login failure. A retry with normal user settings succeeded; authentication was not changed. The two successful Claude task tests cost about USD 1.114 in the CLI. Codex used the existing account allowance; no dollar estimate is provided.

## Independent review and fixes

An independent review reproduced three installer issues in an isolated snapshot: a symlinked installation marker could overwrite a file outside the project, fingerprints omitted newly added user dependency/cache files, and the standalone package lacked the coverage file referenced by its notice. All three were fixed with regression tests. A later review found a temporary marker left behind after marker-commit failure; cleanup and retry tests now cover it. The installer no longer rebuilds the source tree before checking for destination conflicts.

The rollback tests cover errors within a running process. They do not establish recovery after a power loss, concurrent installation, or malicious races.

On 2026-09-23, the shared content source, generated skills, package descriptions, README, and supporting documentation were converted to English. `readm-cn.md` remains the linked Chinese translation. The regenerated packages passed 16 Python tests, 52 Bun tests, TypeScript typecheck, 24 skill format checks, both plugin validators, and a clean rebuild check. The global Claude Code installation was updated. Live model behavior tests were not rerun for this documentation change; the behavior results above refer to the earlier version.

## Not yet verified or provided

- Not all 24 workflows have been exercised on a real project. TDD and delegation have behavior tests on both hosts.
- Cross-provider model competitions, cloud isolation, long-lived recovery, cancellation races, real PR merging, production UI control, and deployment were not tested.
- Cursor's durable wake-up and cloud worker are not represented as equivalent local implementations.
- Benny and GrokBot UI require project-specific external interfaces. Their contracts and blocked states are documented; no live service integration is claimed.
- GitHub PR watching has deterministic tests but has not run as a sustained watcher against a live PR.

See [live-results.json](live-results.json) for structured results. Raw model logs remain in the local work directory; conversation history, credentials, and full environment details were not committed.

## Rerunning

The repository README lists static checks, deterministic tests, and optional live model checks. The live-test script initially returns `needs-evidence-review`: a model exit code of zero is not acceptance. Inspect invocation order and real artifacts before promoting the result.
