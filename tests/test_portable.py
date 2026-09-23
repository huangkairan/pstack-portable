import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import build, digest_tree
from check_plan import validate
from install import install, fingerprint
from worktree_audit import audit


class PlanTests(unittest.TestCase):
    def test_valid_dependency_graph_does_not_claim_execution(self):
        plan = {'goal': '迁移', 'units': [
            {'id': 'a', 'deliverable': '类型', 'verify': '类型检查'},
            {'id': 'b', 'dependsOn': ['a'], 'deliverable': '调用者', 'verify': '行为检查'}]}
        self.assertEqual(validate(plan), {'valid': True, 'units': 2, 'executionVerified': False})

    def test_rejects_invalid_dependencies_and_empty_verification(self):
        cases = [
            [{'id': 'a', 'dependsOn': ['a'], 'deliverable': 'x', 'verify': 'x'}],
            [{'id': 'a', 'dependsOn': ['missing'], 'deliverable': 'x', 'verify': 'x'}],
            [{'id': 'a', 'deliverable': 'x'}],
            [{'id': 'a', 'deliverable': 'x', 'verify': ' '}],
            [{'id': 'a', 'deliverable': 'x', 'verify': 'x'}]*2]
        for units in cases:
            with self.subTest(units=units), self.assertRaises(ValueError):
                validate({'goal': 'x', 'units': units})


class InstallTests(unittest.TestCase):
    def test_claude_global_install_uses_home_skills_and_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            with patch('install.Path.home', return_value=home):
                install('claude-code', global_install=True)
                skill = home / '.claude/skills/pstack-how/SKILL.md'
                agent = home / '.claude/agents/pstack-reviewer.md'
                self.assertTrue(skill.is_file())
                self.assertTrue(agent.is_file())
                install('claude-code', global_install=True)
                self.assertTrue(skill.is_file())
            self.assertFalse((home / '.agents').exists())

    def test_both_hosts_install_and_update_preserving_foreign_skills(self):
        for host, directory in [('codex', '.agents'), ('claude-code', '.claude')]:
            with self.subTest(host=host), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp)
                user = project / directory / 'skills/custom/SKILL.md'
                user.parent.mkdir(parents=True); user.write_text('用户技能')
                install(host, project)
                self.assertEqual(user.read_text(), '用户技能')
                root = project / directory / 'skills/pstack-tdd'
                self.assertTrue((root / 'references/contracts.md').is_file())
                self.assertTrue((root / 'references/host.md').is_file())
                self.assertEqual(len(list((project / directory / 'skills').glob('pstack-*/SKILL.md'))), 24)
                install(host, project)
                self.assertEqual(user.read_text(), '用户技能')

    def test_modified_owned_files_and_added_node_modules_block_update(self):
        for relative in ['SKILL.md', 'node_modules/custom/data.txt', '__pycache__/user.txt']:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp)
                install('codex', project)
                path = project / '.agents/skills/pstack-tdd' / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('用户本地修改')
                before = fingerprint(project)
                with self.assertRaises(ValueError): install('codex', project)
                self.assertEqual(fingerprint(project), before)

    def test_foreign_collision_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            path = project / '.agents/skills/pstack-how/SKILL.md'
            path.parent.mkdir(parents=True); path.write_text('外来技能')
            with self.assertRaises(ValueError): install('codex', project)
            self.assertEqual(path.read_text(), '外来技能')
            self.assertFalse((project / '.agents/skills/pstack-tdd').exists())

    def test_symlink_parent_and_marker_do_not_write_outside_project(self):
        for kind in ['parent', 'marker']:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp)/'project'; project.mkdir()
                outside = Path(tmp)/'outside'; outside.mkdir()
                secret = outside/'record.json'; secret.write_text('{}')
                if kind == 'parent': (project/'.agents').symlink_to(outside, target_is_directory=True)
                else:
                    (project/'.agents').mkdir()
                    (project/'.agents/pstack-portable-installed.json').symlink_to(secret)
                before = fingerprint(outside)
                with self.assertRaises(ValueError): install('codex', project)
                self.assertEqual(fingerprint(outside), before)

    def test_failed_write_rolls_back_existing_install(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            install('codex', project)
            before = fingerprint(project)
            real_copy = shutil.copytree
            def fail_once(src, dst, *args, **kwargs):
                if Path(dst).resolve() == (project/'.agents/skills/pstack-tdd').resolve() and not kwargs.get('symlinks'):
                    raise OSError('模拟写入失败')
                return real_copy(src, dst, *args, **kwargs)
            with patch('install.shutil.copytree', side_effect=fail_once), self.assertRaises(OSError):
                install('codex', project)
            self.assertEqual(fingerprint(project), before)

    def test_marker_commit_failure_cleans_own_temp_and_allows_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            install('codex', project)
            before = fingerprint(project)
            with patch('install.os.replace', side_effect=OSError('模拟记录提交失败')), self.assertRaises(OSError):
                install('codex', project)
            self.assertEqual(fingerprint(project), before)
            install('codex', project)
            self.assertEqual(fingerprint(project), before)

    def test_preexisting_temp_marker_is_preserved_on_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            install('codex', project)
            pending = project/'.agents/pstack-portable-installed.json.tmp'
            pending.write_text('用户文件')
            before = fingerprint(project)
            with self.assertRaises(ValueError): install('codex', project)
            self.assertEqual(fingerprint(project), before)

    def test_install_does_not_rebuild_source_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = digest_tree(ROOT/'skills')
            with patch('build.build', side_effect=AssertionError('不允许重建源码')):
                install('codex', Path(tmp))
            self.assertEqual(digest_tree(ROOT/'skills'), before)


class AuditTests(unittest.TestCase):
    def test_paths_with_spaces_and_dirty_worktree_are_preserved(self):
        with tempfile.TemporaryDirectory(prefix='pstack space ') as tmp:
            repo = Path(tmp)/'repo with spaces'
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (repo/'tracked.txt').write_text('x')
            subprocess.run(['git','-C',str(repo),'add','.'],check=True)
            subprocess.run(['git','-C',str(repo),'-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],check=True)
            self.assertFalse(audit(repo)[0]['dirty'])
            (repo/'tracked.txt').write_text('user edits')
            entry = audit(repo)[0]
            self.assertTrue(entry['dirty'])
            self.assertFalse(entry['deletionAuthorized'])
            self.assertEqual((repo/'tracked.txt').read_text(), 'user edits')


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): build()

    def test_links_resolve_inside_packages(self):
        for host in ['codex','claude-code']:
            package = ROOT/'dist'/host/'pstack-portable'
            for path in package.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                    if '://' in link or link.startswith('#'): continue
                    target = (path.parent/link.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to(package.resolve()), (path,link))
                    self.assertTrue(target.exists(), (path,link))
            self.assertTrue((package/'docs/coverage.json').is_file())

    def test_active_entries_have_no_cursor_fields_or_model_slugs(self):
        for path in (ROOT/'skills').rglob('*.md'):
            self.assertIsNone(re.search(r'\.cursor/|grok-4\.6|claude-fable|subagent_type|^mode:|^reminder:',path.read_text(),re.M),path)

    def test_inventory_covers_every_upstream_skill(self):
        coverage=json.loads((ROOT/'docs/coverage.json').read_text())
        expected={str(p.relative_to(ROOT/'vendor/pstack')) for p in (ROOT/'vendor/pstack').rglob('SKILL.md')}
        self.assertEqual({x['source'] for x in coverage['skills']},expected)
        for entry in coverage['skills']: self.assertTrue((ROOT/entry['target']).exists(),entry)


if __name__ == '__main__': unittest.main()
