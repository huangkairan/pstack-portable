# pstack-portable

An unofficial Claude Code and Codex port of Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/main/pstack). It is based on upstream version 0.15.2 at commit `53e579f1481697931fc44f5445171397cfa2b24b` and preserves the MIT license.

**[Chinese README](readm-cn.md)**

The package has 24 workflows from one shared content source. Twenty-three principles are on-demand references, and 23 playbooks are selectable through `pstack-poteto-mode`. Small tasks can run directly; design competitions and parallel reviews are opt-in. No third-party skill installation is required.

This port deliberately changes some behavior; it is not a verbatim copy. The upstream snapshot is preserved in `vendor/pstack` for provenance and is not loaded as active instructions. See the [capability inventory](docs/coverage.json) and [validation record](docs/validation.md).

## Install globally for Claude Code

Python 3.9+ is required. Clone the repository and run the installer once. New Claude Code sessions can then use the skills in any project.

```bash
git clone git@github.com:huangkairan/pstack-portable.git
cd pstack-portable
python3 scripts/install.py --host claude-code --global
```

This writes `~/.claude/skills/pstack-*`, `~/.claude/agents/poteto-agent.md`, and `~/.claude/agents/pstack-reviewer.md`. The ownership record is `~/.claude/pstack-portable-installed.json`. A same-named foreign skill or agent blocks installation instead of being overwritten. After updating the repository, run the same command again. Locally modified installed files are preserved and block the update.

Start a new `claude` session and invoke `/pstack-poteto-mode`, `/pstack-how`, or `/pstack-tdd`. Avoid installing both global and project copies of the same skill for a project because duplicate commands can become ambiguous.

## Install in one project

Project installation scopes the skills to one repository. It also requires Python 3.9+. The installer checks for foreign names and local modifications before writing.

```bash
git clone git@github.com:huangkairan/pstack-portable.git
cd pstack-portable
python3 scripts/install.py --host codex --project /path/to/project
python3 scripts/install.py --host claude-code --project /path/to/project
```

Start a new session inside that project.

| Task | Codex | Claude Code project install |
|---|---|---|
| Understand a system | `$pstack-how` | `/pstack-how` |
| Fix a bug with before/after evidence | `$pstack-tdd` | `/pstack-tdd` |
| Select a full playbook | `$pstack-poteto-mode` | `/pstack-poteto-mode` |
| Create a project verification skill | `$pstack-create-verification-skill` | `/pstack-create-verification-skill` |
| Split an investigation across agents | `$pstack-swarm` | `/pstack-swarm` |
| Review change impact | `$pstack-blast-radius` | `/pstack-blast-radius` |

Start with `how`, `tdd`, or `poteto-mode` rather than memorizing every entry point. Every leaf skill bundles its own execution contract and host adapter; it does not require globally installed sibling skills.

## Native plugin packages

```bash
python3 scripts/build.py
claude --plugin-dir ./dist/claude-code/pstack-portable
```

The Claude plugin uses names such as `/pstack-portable:pstack-how`; project and global skill installs use `/pstack-how`. The Codex package is in `dist/codex/pstack-portable`. The root `.codex-plugin/plugin.json` and generated `skills` are also a plugin source. The tested project installer additionally provides `.codex/agents`; discovering a plugin does not prove that its custom role profiles were registered. When an exposed delegation tool cannot name a role, the adapter passes the role brief to a native subagent while preserving parent permissions.

## Deliberate behavior changes

- Investigation, design comparison, independent review, regression evidence, project verification, and decision logs remain available.
- Principles are references instead of default-loaded skills. Leaf workflows do not call the mode router again. Invocation settings are adapted for each host rather than copied from Cursor frontmatter.
- Model selection inherits the host session by default. Multiple agents on the same model have separate contexts; that is not cross-model verification.
- Installation changes no global rules, hooks, timers, or background services. A skill instruction cannot grant permission for an external action.
- Useful rationale, license text, tool directives, and API documentation are preserved rather than removed to pursue zero comments.
- In-process installation errors are rolled back. Power-loss recovery and concurrent installation are outside the installer's guarantee. Stop using a destination directory while updating it.

## Optional deterministic tools

```bash
python3 scripts/doctor.py --host codex
python3 scripts/worktree_audit.py /path/to/repository
python3 scripts/check_plan.py plan.json
```

The plan format is `{"goal":"Goal","units":[{"id":"a","dependsOn":[],"deliverable":"Artifact","verify":"Real check or user path"}]}`. The checker validates non-empty checks, known dependencies, and an acyclic graph. It does not implement upstream's fixed ten-lane Markdown template or prove the plan ran.

The preserved ledger and PR watcher require Bun and locked dependencies. Their first dependency installation is explicit; the tools do not silently download packages.

```bash
cd tools
bun install --frozen-lockfile
bun orch/orch.ts --help
bun watch-pr/cli.ts --help
```

`orch` maintains a ledger; it neither starts agents nor validates evidence. Its Graphite frontier operation still requires `gt`; basic ledger use does not. `watch-pr` reads GitHub through `gh` and does not fix or merge. In a project install, the optional tool copy lives under `pstack-poteto-mode/tools`. Installing dependencies in that copy is a local change that blocks a later overwrite. Preserve that directory's data before replacing it; the installer never deletes user-added files on an update.

## External integration boundaries

Cursor cloud workers, durable wake-up, GrokBot UI, and Benny's Slack, tracker, and control environment have no simulated equivalent here. Their workflows retain explicit inputs, outputs, and blocked states until the target host and project supply real capabilities. See [Benny's integration contract](docs/benny.md).

`make-bot-ui` reports a block without an actual platform interface. Long-running playbooks can advance within a session and save a checkpoint, but that does not imply automatic recovery after exit. PR, publishing, and deletion actions require current task authorization. The live tests executed none of those actions.

## Develop and verify

`core` is the content source; `adapters` hold host-specific instructions; `scripts/build.py` generates the packages. Do not hand-edit the root `skills` directory or `dist`.

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py --check
cd tools
bun install --frozen-lockfile
bun test orch watch-pr
bun run typecheck
```

Live model tests are optional and consume the current account's allowance. Each Claude run has a USD 2 cap and a default 180-second timeout. The output directory must not exist.

```bash
python3 tests/live_smoke.py --host codex --case tdd --output .test-runs/codex-tdd
python3 tests/live_smoke.py --host claude-code --case delegation --output .test-runs/claude-delegation
```

Each live test creates an isolated Git project and records events, exit state, and artifacts. A model exit code of zero is not treated as acceptance; inspect skill loading, before/after order, and child agent completion. Raw logs stay local and are not committed.
