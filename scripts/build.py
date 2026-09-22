#!/usr/bin/env python3
"""从共用内容生成两个原生包；生成目录不手改。"""
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
        entry += '先读取 [执行契约](references/contracts.md) 与 [宿主适配](references/host.md)，再按下列流程执行。\n\n' + body
        if name in EXTRA:
            entry += '\n按流程需要读取：\n' + '\n'.join(f'- [{n}](references/workflows/{n}.md)' for n in EXTRA[name]) + '\n'
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
            entry += '\n[流程索引](references/playbooks/index.md)；[原则索引](references/principles.md)。本入口中的工具路径相对本技能目录，首次用 tools 显式安装其依赖。\n'
        if name == 'setup-pstack':
            copy(ROOT / 'scripts/doctor.py', folder / 'scripts/doctor.py')
        if name == 'typescript-best-practices':
            copy(ROOT / 'core/references/typescript.md', refs / 'typescript.md')
            entry += '\n检查具体类型设计时读取 [类型规则](references/typescript.md)。\n'
        (folder / 'SKILL.md').write_text(entry)
    manifest = {'name': 'pstack-portable', 'version': '0.1.0', 'description': 'pstack 的 Claude Code 与 Codex 非官方移植；按需工作流与真实验证。', 'author': {'name': 'huangkairan'}, 'license': 'MIT'}
    if host == 'codex':
        manifest['skills'] = './skills/'
        manifest_dir = root / '.codex-plugin'
    else:
        manifest_dir = root / '.claude-plugin'
        agents = root / 'agents'
        agents.mkdir()
        (agents / 'pstack-reviewer.md').write_text('''---
name: pstack-reviewer
description: 独立只读检查实现与证据，返回具体问题和未知项。
tools: Read, Grep, Glob
---

独立读取任务指定的代码与证据。报告路径、问题触发条件、影响与建议；没有执行权限时只报告静态审查，不声称运行通过。不修改文件，不代表主代理发送消息。
''')
        (agents / 'poteto-agent.md').write_text('''---
name: poteto-agent
description: 在明确范围内完成实现或调查并返回实际证据。
---

按主任务目标、允许写入范围、基线与完成条件工作。选择最小相关流程，任务简单时直接完成。返回产物、实际验证、未完成项和限制。隔离输出，外部动作遵循当前任务授权；不自动递归派生。
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
                    raise ValueError(f'{host} 产物与源码不一致，先运行 scripts/build.py')
            else:
                if dest.exists():
                    shutil.rmtree(dest)
                copy(out, dest)
        source = tmp / 'codex/pstack-portable/skills'
        if check:
            if digest_tree(source) != digest_tree(ROOT / 'skills'):
                raise ValueError('根目录 skills 与源码不一致')
        else:
            shutil.rmtree(ROOT / 'skills')
            copy(source, ROOT / 'skills')
    print('两个宿主产物已核对' if check else '已生成两个宿主包和根目录 Codex skills')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    try:
        build(p.parse_args().check)
    except ValueError as e:
        p.exit(1, f'{e}\n')
