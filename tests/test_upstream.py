"""Offline deterministic tests for source tracking and PR-report generation."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_upstream import check_source, relevant, render_report, review, safe_text  # noqa: E402
from validate_skills import validate_source_data, validate_skill  # noqa: E402

A = 'a' * 40
B = 'b' * 40
FILES = {'id': 'test-files', 'repo': 'owner/repo', 'mode': 'files', 'ref': 'main',
         'paths': ['skills/embedded/'], 'skills': ['embedded-developer'], 'reason': 'test'}
RELEASE = {'id': 'test-release', 'repo': 'owner/tool', 'mode': 'release',
           'skills': ['embedded-qa'], 'reason': 'test'}


class FakeAPI:
    def __init__(self, changes=None, head=B, tag='v2.0', fail=False):
        self.files = changes if changes is not None else []
        self.head = head
        self.tag = tag
        self.fail = fail
        self.calls = []

    def get(self, path):
        self.calls.append(path)
        if path.endswith('/releases/latest'):
            return {'tag_name': self.tag}
        if '/commits/main' in path:
            return {'sha': self.head}
        if '/compare/' in path:
            if self.fail:
                raise RuntimeError('not found')
            return {'status': 'ahead', 'total_commits': 1, 'files': self.files}
        raise AssertionError(path)


class UpstreamTest(unittest.TestCase):
    def test_no_change_no_compare(self):
        api = FakeAPI(head=A)
        self.assertIsNone(check_source(api, FILES, {'commit': A}))
        self.assertEqual(len(api.calls), 1)

    def test_irrelevant_path_no_pr(self):
        api = FakeAPI([{'filename': 'README.md', 'status': 'modified'}])
        self.assertIsNone(check_source(api, FILES, {'commit': A}))

    def test_relevant_path_detected(self):
        api = FakeAPI([{'filename': 'skills/embedded/SKILL.md', 'status': 'modified'}])
        found = check_source(api, FILES, {'commit': A})
        self.assertEqual(found['status'], 'relevant files changed')
        self.assertEqual(found['current'], B)
        self.assertEqual(len(found['files']), 1)

    def test_rename_from_relevant_path(self):
        api = FakeAPI([{'filename': 'new/SKILL.md', 'previous_filename': 'skills/embedded/SKILL.md',
                        'status': 'renamed'}])
        self.assertEqual(len(check_source(api, FILES, {'commit': A})['files']), 1)

    def test_release_and_no_change(self):
        self.assertIsNone(check_source(FakeAPI(tag='v1.0'), RELEASE, {'tag': 'v1.0'}))
        self.assertEqual(check_source(FakeAPI(), RELEASE, {'tag': 'v1.0'})['current'], 'v2.0')

    def test_incomplete_compare_proposes_review(self):
        many = [{'filename': f'unrelated/{i}.txt', 'status': 'modified'} for i in range(300)]
        result = check_source(FakeAPI(many), FILES, {'commit': A})
        self.assertTrue(result['uncertain'])

    def test_missing_compare_proposes_review(self):
        result = check_source(FakeAPI(fail=True), FILES, {'commit': A})
        self.assertTrue(result['uncertain'])

    def test_review_updates_only_changed_baselines(self):
        manifest = {'sources': [FILES, RELEASE]}
        old = {'schema_version': 1, 'sources': {'test-files': {'commit': A}, 'test-release': {'tag': 'v1.0'}}}
        changes, current = review(FakeAPI([{'filename': 'README.md'}], tag='v2.0'), manifest, old)
        self.assertEqual(len(changes), 1)
        self.assertEqual(current['sources']['test-files']['commit'], A)
        self.assertEqual(current['sources']['test-release']['tag'], 'v2.0')
        self.assertEqual(old['sources']['test-release']['tag'], 'v1.0')

    def test_report_deterministic_and_sanitized(self):
        ch = check_source(FakeAPI([{'filename': 'skills/embedded/`oops`.md', 'status': 'modified'}]),
                          FILES, {'commit': A})
        report = render_report([ch])
        self.assertIn("'oops'", report)
        self.assertEqual(report, render_report([ch]))
        self.assertIn('zero LLM', report)

    def test_unknown_source_rejected(self):
        manifest = {'schema_version': 1, 'sources': [FILES]}
        state = {'schema_version': 1, 'sources': {}}
        with self.assertRaises(ValueError):
            validate_source_data(manifest, state)

    def test_monitored_paths(self):
        self.assertTrue(relevant('folder/file.md', ['folder/']))
        self.assertTrue(relevant('folder/a/SKILL.md', ['folder/*/SKILL.md']))
        self.assertFalse(relevant('folderish/x', ['folder/']))
        self.assertEqual(safe_text('bad\nthing'), 'bad thing')

    def test_skills_valid(self):
        for name in ('embedded-architect', 'embedded-developer', 'embedded-qa'):
            validate_skill(ROOT / 'skills' / name)

    def test_manifest_consistent(self):
        manifest = json.loads((ROOT / 'maintenance/sources.json').read_text())
        state = json.loads((ROOT / 'maintenance/reviewed-revisions.json').read_text())
        validate_source_data(manifest, state)


if __name__ == '__main__':
    unittest.main()
