#!/usr/bin/env python3
"""Generate native packages from shared content; do not edit generated files."""
import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRA = {'architect': ['arena'], 'figure-it-out': ['architect', 'arena'], 'teach': ['how', 'why']}


def copy(src, dst):
    if src.is_dir():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('node_modules', '__pycache__'))
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def build_package(root, host):
    root.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((ROOT / 'core/catalog.json').read_text())
    for name, info in catalog.items():
        folder = root / 'skills' / f'pstack-{name}'
        folder.mkdir(parents=True)
        refs = folder / 'references'
        refs.mkdir()
        copy(ROOT / 'core/references/contracts.md', refs / 'contracts.md')
        copy(ROOT / f'adapters/{host}.md', refs / 'host.md')
        body = (ROOT / f'core/workflows/{name}.md').read_text()
        entry = f'---\nname: pstack-{name}\ndescription: {json.dumps(info["description"], ensure_ascii=False)}\n---\n\n'
        entry += 'Read the [execution contract](references/contracts.md) and [host adapter](references/host.md) before following this workflow.\n\n' + body
        if name in EXTRA:
            entry += '\nRead when this workflow requires it:\n' + '\n'.join(f'- [{n}](references/workflows/{n}.md)' for n in EXTRA[name]) + '\n'
            for n in EXTRA[name]:
                copy(ROOT / f'core/workflows/{n}.md', refs / f'workflows/{n}.md')
        if name == 'poteto-mode':
            copy(ROOT / 'core/playbooks', refs / 'playbooks')
            copy(ROOT / 'core/workflows', refs / 'workflows')
            copy(ROOT / 'core/references/principles', refs / 'principles')
            copy(ROOT / 'core/references/principles.md', refs / 'principles.md')
            copy(ROOT / 'tools', folder / 'tools')
            for n in ['check_plan.py', 'worktree_audit.py', 'doctor.py']:
                copy(ROOT / 'scripts' / n, folder / 'scripts' / n)
            entry += '\n[Playbook index](references/playbooks/index.md); [principle index](references/principles.md). Tool paths are relative to this skill directory. Explicitly install tool dependencies before first use.\n'
        if name == 'setup-pstack':
            copy(ROOT / 'scripts/doctor.py', folder / 'scripts/doctor.py')
        if name == 'typescript-best-practices':
            copy(ROOT / 'core/references/typescript.md', refs / 'typescript.md')
            entry += '\nRead the [type rules](references/typescript.md) when assessing a concrete type design.\n'
        (folder / 'SKILL.md').write_text(entry)
    manifest = {'name': 'pstack-portable', 'version': '0.1.0', 'description': 'An unofficial pstack port for Claude Code and Codex with task-specific workflows and real verification.', 'author': {'name': 'huangkairan'}, 'license': 'MIT'}
    if host == 'codex':
        manifest['skills'] = './skills/'
        manifest_dir = root / '.codex-plugin'
    else:
        manifest_dir = root / '.claude-plugin'
        agents = root / 'agents'
        agents.mkdir()
        (agents / 'pstack-reviewer.md').write_text('''---
name: pstack-reviewer
description: Independently review implementation and evidence without modifying files.
tools: Read, Grep, Glob
---

Read the code and evidence specified by the task. Report paths, triggering conditions, impact, and recommendations. Without execution access, report only static findings. Do not claim runtime success, edit files, or send messages on behalf of the parent.
''')
        (agents / 'poteto-agent.md').write_text('''---
name: poteto-agent
description: Implement or investigate within a defined scope and report actual evidence.
---

Work from the parent task goal, allowed write paths, base revision, and completion criteria. Choose the smallest relevant workflow and complete simple tasks directly. Return artifacts, actual checks, unfinished work, and limitations. Keep outputs isolated. Follow current authorization for external actions and do not recursively delegate by default.
''')
    manifest_dir.mkdir()
    (manifest_dir / 'plugin.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    copy(ROOT / 'LICENSE', root / 'LICENSE')
    copy(ROOT / 'NOTICE.md', root / 'NOTICE.md')
    copy(ROOT / 'docs/coverage.json', root / 'docs/coverage.json')
    copy(ROOT / 'docs/benny.md', root / 'docs/benny.md')


def digest_tree(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts}


def build(check=False):
    with tempfile.TemporaryDirectory(prefix='pstack-build-') as tmp:
        tmp = Path(tmp)
        for host in ['codex', 'claude-code']:
            out = tmp / host / 'pstack-portable'
            build_package(out, host)
            dest = ROOT / 'dist' / host / 'pstack-portable'
            if check:
                if not dest.exists() or digest_tree(out) != digest_tree(dest):
                    raise ValueError(f'{host} package differs from source; run scripts/build.py first')
            else:
                if dest.exists():
                    shutil.rmtree(dest)
                copy(out, dest)
        source = tmp / 'codex/pstack-portable/skills'
        if check:
            if digest_tree(source) != digest_tree(ROOT / 'skills'):
                raise ValueError('Root skills differ from source')
        else:
            shutil.rmtree(ROOT / 'skills')
            copy(source, ROOT / 'skills')
    print('Both host packages match source' if check else 'Generated both host packages and root Codex skills')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    try:
        build(p.parse_args().check)
    except ValueError as e:
        p.exit(1, f'{e}\n')
