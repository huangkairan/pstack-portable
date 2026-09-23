#!/usr/bin/env python3
"""Run live model tests explicitly; they consume host allowance and keep logs in the selected directory."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from install import install
from build import build


def prepare(path, case):
    path.mkdir(parents=True)
    if case == 'tdd':
        (path/'cart.py').write_text('def total_cents(items, discount_cents=0):\n    subtotal = sum(price * quantity for price, quantity in items)\n    return subtotal - discount_cents\n')
        (path/'test_cart.py').write_text('import unittest\nfrom cart import total_cents\nclass CartTests(unittest.TestCase):\n    def test_subtotal(self): self.assertEqual(total_cents([(120, 2), (55, 1)]), 295)\n    def test_discount(self): self.assertEqual(total_cents([(100, 2)], 50), 150)\n')
    else:
        (path/'stock.py').write_text('def can_reserve(stock, quantity):\n    return quantity > 0 and quantity <= stock\n')
        (path/'price.py').write_text('def discounted(price, discount):\n    return max(0, price - discount)\n')
    subprocess.run(['git','init','-q',str(path)],check=True)
    subprocess.run(['git','-C',str(path),'add','.'],check=True)
    subprocess.run(['git','-C',str(path),'-c','user.name=Portable Test','-c','user.email=test@example.invalid','commit','-qm','test baseline'],check=True)


def run(host, case, output, timeout=180, persist=False):
    output = Path(output).resolve()
    if output.exists(): raise ValueError('Output directory must not exist, to avoid overwriting evidence')
    project = output/'project'
    prepare(project, case)
    if host == 'codex':
        install(host, project)
        skill = '$pstack-'+('tdd' if case == 'tdd' else 'swarm')
    else:
        build()
        skill = '/pstack-portable:pstack-'+('tdd' if case == 'tdd' else 'swarm')
    if case == 'tdd':
        prompt = f'Use {skill} to fix cart.py: return 0 when the discount exceeds the subtotal, while preserving normal discounts. First write and run a failing regression test, then change the implementation and run all unittest tests. Edit only cart.py and test_cart.py. Do not commit, access the network, or use external connectors. Report the actual evidence in English.'
    else:
        role = 'pstack-reviewer' if host == 'codex' else 'pstack-portable:pstack-reviewer'
        prompt = f'Use {skill} to investigate the boundary behavior of stock.py and price.py separately. Actually delegate to two independent {role} subagents, one read-only file per agent. Each must return concrete conditions and examples. Wait for both before summarizing. Do not modify files, access the network, or use external connectors. Acceptance requires two real independent delegations; do not substitute two perspectives from yourself. State clearly if delegation is unavailable.'
    if host == 'codex':
        cmd=['codex','exec','--ignore-user-config','--ephemeral','--sandbox','workspace-write' if case=='tdd' else 'read-only','--json','-c','model_reasoning_effort="low"','-C',str(project),prompt]
        if persist: cmd.remove('--ephemeral')
    else:
        cmd=['claude','-p',prompt,'--plugin-dir',str(ROOT/'dist/claude-code/pstack-portable'),'--output-format','stream-json','--verbose','--max-budget-usd','2','--tools','Read,Edit,Write,Glob,Grep,Skill,Bash,Agent','--allowedTools','Read,Edit,Write,Glob,Grep,Skill,Agent,Bash(python3 *)','--setting-sources','user,project']
    start=time.monotonic()
    with (output/'events.jsonl').open('w') as out,(output/'stderr.log').open('w') as err:
        proc=subprocess.Popen(cmd,cwd=project,stdout=out,stderr=err,start_new_session=True)
        try: code=proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=8)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            code=124
    events=[]
    for line in (output/'events.jsonl').read_text().splitlines():
        try:events.append(json.loads(line))
        except ValueError:pass
    errors=[e for e in events if e.get('is_error') or e.get('type') in ['error','turn.failed']]
    changed=subprocess.check_output(['git','-C',str(project),'diff','--name-only'],text=True).splitlines()
    result={'host':host,'case':case,'exitCode':code,'seconds':round(time.monotonic()-start,1),'modelErrors':len(errors),'changedTrackedFiles':changed,'state':'needs-evidence-review'}
    if code != 0 or errors: result['state']='failed'
    if case=='tdd' and result['state']!='failed':
        check=subprocess.run([sys.executable,'-c','from cart import total_cents; assert total_cents([(100,2)],500)==0; assert total_cents([(100,2)],50)==150; assert total_cents([],5)==0; assert total_cents([(120,2),(55,1)])==295'],cwd=project,capture_output=True,text=True)
        tests=subprocess.run([sys.executable,'-m','unittest','discover','-v'],cwd=project,capture_output=True,text=True)
        (output/'independent-check.txt').write_text(check.stderr+tests.stdout+tests.stderr)
        result['independentAssertionsPassed']=check.returncode==0 and tests.returncode==0
        if not result['independentAssertionsPassed'] or set(changed)-{'cart.py','test_cart.py'}: result['state']='failed'
    if case=='delegation' and changed:result['state']='failed'
    (output/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
    return 1 if result['state']=='failed' else 0


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--host',choices=['codex','claude-code'],required=True)
    p.add_argument('--case',choices=['tdd','delegation'],required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--timeout',type=int,default=180)
    p.add_argument('--persist',action='store_true',help='Keep this Codex test session for reviewing delegation events')
    a=p.parse_args()
    sys.exit(run(a.host,a.case,a.output,a.timeout,a.persist))
