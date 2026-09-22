#!/usr/bin/env python3
"""只读列出 worktree 状态；不判断可安全删除，不调用删除命令。"""
import argparse
import json
import subprocess
from pathlib import Path


def audit(repo):
    raw = subprocess.check_output(['git', '-C', str(repo), 'worktree', 'list', '--porcelain', '-z'])
    result, record = [], {}
    for field in raw.decode('utf-8', errors='surrogateescape').split('\0'):
        if not field:
            if record:
                result.append(record)
                record = {}
            continue
        key, _, value = field.partition(' ')
        record[key] = value if value else True
    if record:
        result.append(record)
    for item in result:
        path = item.get('worktree')
        if path and not item.get('bare'):
            proc = subprocess.run(['git', '-C', path, 'status', '--porcelain', '-z'], capture_output=True)
            item['dirty'] = bool(proc.stdout) if proc.returncode == 0 else None
        else:
            item['dirty'] = None
        item['deletionAuthorized'] = False
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.repo), ensure_ascii=False, indent=2))
