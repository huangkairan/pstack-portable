#!/usr/bin/env python3
"""Validate plan dependencies and checks without claiming execution succeeded."""
import argparse
import json
from pathlib import Path


def validate(plan):
    if not isinstance(plan, dict) or not isinstance(plan.get('goal'), str) or not plan['goal'].strip():
        raise ValueError('goal must be a non-empty string')
    units = plan.get('units')
    if not isinstance(units, list) or not units:
        raise ValueError('units must be a non-empty list')
    ids = set()
    for unit in units:
        if not isinstance(unit, dict):
            raise ValueError('unit must be an object')
        name = unit.get('id')
        if not isinstance(name, str) or not name.strip() or name in ids:
            raise ValueError('unit id must be non-empty and unique')
        ids.add(name)
        for field in ['deliverable', 'verify']:
            if not isinstance(unit.get(field), str) or not unit[field].strip():
                raise ValueError(f'{name}: {field} must be non-empty')
        deps = unit.get('dependsOn', [])
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
            raise ValueError(f'{name}: dependsOn must be a list of strings')
        if len(deps) != len(set(deps)):
            raise ValueError(f'{name}: duplicate dependency')
    graph = {u['id']: u.get('dependsOn', []) for u in units}
    visiting, done = set(), set()

    def visit(name):
        if name not in ids:
            raise ValueError(f'Unknown dependency: {name}')
        if name in visiting:
            raise ValueError(f'Cyclic dependency: {name}')
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
        parser.exit(1, f'Invalid plan: {e}\n')
