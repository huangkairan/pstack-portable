#!/usr/bin/env python3
"""安装到指定项目或 Claude Code 全局目录；冲突不覆盖，失败回滚。"""
import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

from build import ROOT, build_package


def fingerprint(path):
    if path.is_symlink():
        return {'symlink': os.readlink(path)}
    if path.is_dir():
        return {str(p.relative_to(path)): fingerprint(p) for p in sorted(path.iterdir())}
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_symlinks(path, project):
    current = path
    while current != project:
        if current.is_symlink():
            raise ValueError(f'拒绝通过符号链接安装: {current}')
        current = current.parent


def install(host, project=None, global_install=False):
    if global_install:
        if host != 'claude-code':
            raise ValueError('目前仅支持 Claude Code 全局安装')
        project = Path.home().resolve()
    elif project is None:
        raise ValueError('项目安装需要 --project')
    else:
        project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError('项目目录必须已存在')
    native = '.claude' if host == 'claude-code' else '.agents'
    marker = project / native / 'pstack-portable-installed.json'
    reject_symlinks(marker, project)
    old = json.loads(marker.read_text()) if marker.exists() else {}
    if not isinstance(old, dict):
        raise ValueError('安装记录格式错误')
    with tempfile.TemporaryDirectory(prefix='pstack-install-') as tmp:
        tmp = Path(tmp)
        source = tmp / 'pstack-portable'
        build_package(source, host)
        targets = [(p, project / native / 'skills' / p.name) for p in (source / 'skills').iterdir()]
        agent_root = project / ('.claude' if host == 'claude-code' else '.codex') / 'agents'
        agents = source / 'agents' if host == 'claude-code' else ROOT / 'adapters/codex-agents'
        targets += [(p, agent_root / p.name) for p in agents.iterdir()]
        for _, dest in targets:
            reject_symlinks(dest, project)
            key = str(dest.relative_to(project))
            if dest.exists() and (key not in old or fingerprint(dest) != old[key]):
                raise ValueError(f'目标存在且不属于未修改的本包: {dest}')
        backup = tmp / 'backup'
        backup.mkdir()
        changed = []
        created_dirs = []
        def ensure_parent(path):
            missing = []
            while not path.exists():
                missing.append(path)
                path = path.parent
            for directory in reversed(missing):
                directory.mkdir()
                created_dirs.append(directory)
        temp_marker = marker.with_name(marker.name+'.tmp')
        marker_created = False
        try:
            installed = {}
            for index, (src, dest) in enumerate(targets):
                ensure_parent(dest.parent)
                saved = backup / str(index)
                if dest.exists():
                    if dest.is_dir(): shutil.copytree(dest, saved, symlinks=True)
                    else: shutil.copy2(dest, saved)
                changed.append((dest, saved))
                if dest.is_dir(): shutil.rmtree(dest)
                elif dest.exists(): dest.unlink()
                if src.is_dir(): shutil.copytree(src, dest)
                else: shutil.copy2(src, dest)
                installed[str(dest.relative_to(project))] = fingerprint(dest)
            ensure_parent(marker.parent)
            if temp_marker.exists() or temp_marker.is_symlink():
                raise ValueError(f'临时记录已存在: {temp_marker}')
            with temp_marker.open('x') as stream:
                marker_created = True
                json.dump(installed, stream, ensure_ascii=False, indent=2)
                stream.write('\n')
            os.replace(temp_marker, marker)
        except BaseException:
            if marker_created and temp_marker.exists():
                temp_marker.unlink()
            for dest, saved in reversed(changed):
                if dest.is_dir(): shutil.rmtree(dest)
                elif dest.exists(): dest.unlink()
                if saved.exists():
                    if saved.is_dir(): shutil.copytree(saved, dest, symlinks=True)
                    else: shutil.copy2(saved, dest)
            for directory in reversed(created_dirs):
                if directory.exists() and not any(directory.iterdir()): directory.rmdir()
            raise
    scope = '全局' if global_install else '项目'
    print(f'已将 {len(targets)} 项安装到 {scope}目录 {project / native}，请启动新的 Claude Code 会话' if host == 'claude-code' else f'已将 {len(targets)} 项安装到 {scope}目录 {project / native}，请在该项目启动新会话')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--host', required=True, choices=['codex', 'claude-code'])
    destination = p.add_mutually_exclusive_group(required=True)
    destination.add_argument('--project', type=Path)
    destination.add_argument('--global', dest='global_install', action='store_true')
    args = p.parse_args()
    try:
        install(args.host, args.project, args.global_install)
    except (ValueError, OSError) as e:
        p.exit(1, f'安装未完成: {e}\n')
