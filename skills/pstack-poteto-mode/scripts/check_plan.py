#!/usr/bin/env python3
"""校验计划的依赖与验收结构，不证明执行成功。"""
import argparse
import json
from pathlib import Path


def validate(plan):
    if not isinstance(plan, dict) or not isinstance(plan.get('goal'), str) or not plan['goal'].strip():
        raise ValueError('goal 必须是非空字符串')
    units = plan.get('units')
    if not isinstance(units, list) or not units:
        raise ValueError('units 必须是非空列表')
    ids = set()
    for unit in units:
        if not isinstance(unit, dict):
            raise ValueError('unit 必须是对象')
        name = unit.get('id')
        if not isinstance(name, str) or not name.strip() or name in ids:
            raise ValueError('unit id 必须非空且唯一')
        ids.add(name)
        for field in ['deliverable', 'verify']:
            if not isinstance(unit.get(field), str) or not unit[field].strip():
                raise ValueError(f'{name}: {field} 必须非空')
        deps = unit.get('dependsOn', [])
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
            raise ValueError(f'{name}: dependsOn 必须为字符串列表')
        if len(deps) != len(set(deps)):
            raise ValueError(f'{name}: 重复依赖')
    graph = {u['id']: u.get('dependsOn', []) for u in units}
    visiting, done = set(), set()

    def visit(name):
        if name not in ids:
            raise ValueError(f'未知依赖: {name}')
        if name in visiting:
            raise ValueError(f'循环依赖: {name}')
        if name in done:
            return
        visiting.add(name)
        for dep in graph[name]:
            visit(dep)
        visiting.remove(name)
        done.add(name)

    for name in graph:
        visit(name)
    return {'valid': True, 'units': len(units), 'executionVerified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(json.loads(args.plan.read_text())), ensure_ascii=False))
    except (ValueError, OSError, RecursionError) as e:
        parser.exit(1, f'计划无效: {e}\n')
