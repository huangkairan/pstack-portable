#!/usr/bin/env python3
"""只读检查工具存在性，不把命令存在等同于能力验收。"""
import argparse
import json
import shutil
import subprocess


def inspect(host):
    cli = 'claude' if host == 'claude-code' else 'codex'
    result = {'host': host, 'tools': {}, 'authentication': 'unknown',
              'delegation': 'unknown', 'durableWake': 'unknown', 'controlSurface': 'unknown'}
    for tool in [cli, 'git', 'python3', 'bun', 'gh', 'gt']:
        path = shutil.which(tool)
        result['tools'][tool] = {'available': path is not None}
        if tool == cli and path:
            try:
                proc = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=10)
                result['tools'][tool]['version'] = proc.stdout.strip() if proc.returncode == 0 else 'unknown'
            except (OSError, subprocess.TimeoutExpired):
                result['tools'][tool]['version'] = 'unknown'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['codex', 'claude-code'], required=True)
    args = parser.parse_args()
    print(json.dumps(inspect(args.host), ensure_ascii=False, indent=2))
