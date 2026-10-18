#!/usr/bin/env python3
"""Review upstream GitHub sources and propose a deterministic, no-LLM draft PR.

Only changes to monitored paths or stable release tags create a review report.
The reviewed revision is advanced *inside the PR*, not on the default branch.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'maintenance' / 'sources.json'
STATE = ROOT / 'maintenance' / 'reviewed-revisions.json'
REPORT = ROOT / 'maintenance' / 'reviews' / 'upstream-changes.md'
SHA_RE = re.compile(r'^[a-f0-9]{40}$')


def safe_text(value: Any) -> str:
    """Render untrusted filenames/release names without Markdown or control injection."""
    text = str(value).replace('\n', ' ').replace('\r', ' ')
    return text.replace('`', "'").replace('|', r'\|').replace('[', r'\[').replace(']', r'\]')[:300]


def relevant(path: str, patterns: list[str]) -> bool:
    return any(path.startswith(p) if p.endswith('/') else fnmatch.fnmatchcase(path, p) for p in patterns)


class GithubAPI:
    def __init__(self, token: str | None = None, base_url: str = 'https://api.github.com') -> None:
        self.token = token
        self.base_url = base_url.rstrip('/')

    def get(self, path: str) -> dict[str, Any]:
        url = self.base_url + path
        headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'embedded-agent-skills-upstream-review',
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=25) as response:
                    data = response.read(8_000_001)
                    if len(data) > 8_000_000:
                        raise ValueError('GitHub API response too large; manual review needed')
                obj = json.loads(data)
                if not isinstance(obj, dict):
                    raise ValueError('unexpected API response type')
                return obj
            except urllib.error.HTTPError as exc:
                if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise RuntimeError(f'GitHub API HTTP {exc.code} for {path}') from exc
                time.sleep(2 ** attempt)
        raise RuntimeError('unreachable')


def check_source(api: GithubAPI, src: dict[str, Any], baseline: dict[str, str]) -> dict[str, Any] | None:
    repo = src['repo']
    repo_path = '/repos/' + '/'.join(urllib.parse.quote(piece, safe='') for piece in repo.split('/'))
    if src['mode'] == 'release':
        obj = api.get(repo_path + '/releases/latest')
        tag = obj.get('tag_name')
        if not isinstance(tag, str) or not re.fullmatch(r'[A-Za-z0-9_.+-]{1,100}', tag):
            raise ValueError(f'Invalid stable release tag for {src["id"]}')
        if tag == baseline['tag']:
            return None
        return {'source': src, 'previous': baseline['tag'], 'current': tag,
                'status': 'stable release changed', 'files': [], 'uncertain': False,
                'url': f'https://github.com/{repo}/releases/tag/{urllib.parse.quote(tag, safe="")}',
                'revision_key': 'tag'}

    ref = urllib.parse.quote(src['ref'], safe='')
    obj = api.get(repo_path + f'/commits/{ref}')
    new_sha = obj.get('sha')
    old_sha = baseline['commit']
    if not isinstance(new_sha, str) or not SHA_RE.fullmatch(new_sha):
        raise ValueError(f'Invalid commit SHA for {src["id"]}')
    if new_sha == old_sha:
        return None
    compare_path = repo_path + '/compare/' + old_sha + '...' + new_sha
    try:
        diff = api.get(compare_path + '?per_page=100&page=1')
    except RuntimeError as exc:
        # If a commit was force-pushed/removed or compare fails, never assume no changes.
        return {'source': src, 'previous': old_sha, 'current': new_sha,
                'status': f'comparison failed: {safe_text(exc)}', 'files': [],
                'uncertain': True, 'url': f'https://github.com/{repo}/compare/{old_sha}...{new_sha}',
                'revision_key': 'commit'}
    files = diff.get('files')
    total = diff.get('total_commits')
    uncertain = (not isinstance(files, list) or diff.get('status') not in ('ahead', 'identical')
                 or len(files) >= 300 or (isinstance(total, int) and total > 100))
    matches = []
    for file in files if isinstance(files, list) else []:
        if not isinstance(file, dict):
            uncertain = True
            continue
        name = file.get('filename')
        old = file.get('previous_filename')
        if isinstance(name, str) and (relevant(name, src['paths']) or
                                     (isinstance(old, str) and relevant(old, src['paths']))):
            matches.append({'name': name, 'status': str(file.get('status', 'changed'))})
    if not matches and not uncertain:
        return None
    return {'source': src, 'previous': old_sha, 'current': new_sha,
            'status': 'relevant files changed' if matches else 'comparison incomplete; inspect manually',
            'files': matches, 'uncertain': uncertain,
            'url': f'https://github.com/{repo}/compare/{old_sha}...{new_sha}',
            'revision_key': 'commit'}


def render_report(changes: list[dict[str, Any]]) -> str:
    lines = [
        '# Upstream embedded sources: review required', '',
        '> Generated deterministically, with **zero LLM inference**. Changes are proposals for review, not trusted instructions.',
        '', '## Review procedure', '',
        '1. Open each upstream diff/release and check source authenticity and target/toolchain applicability.',
        '2. Decide **adopt / reject / defer** per source; record rationale in this PR.',
        '3. For adopted changes, make the smallest changes to the affected skill files in a separate implementation PR or before merging this review PR.',
        '4. Run the skill validators and a representative embedded regression. Do not merge as "reviewed" without an explicit disposition.',
        '5. The updated `reviewed-revisions.json` in this PR suppresses repeat proposals **only after merge**.',
        '', '## Detected sources', ''
    ]
    for ch in changes:
        src = ch['source']
        lines += [f'### {safe_text(src["id"])}', '',
                  f'- Upstream: `{safe_text(src["repo"])}`',
                  f'- Affects: {", ".join("`" + safe_text(s) + "`" for s in src["skills"])}',
                  f'- Reason tracked: {safe_text(src["reason"])}',
                  f'- Previous: `{safe_text(ch["previous"])}`',
                  f'- Current: `{safe_text(ch["current"])}`',
                  f'- Trigger: {safe_text(ch["status"])}',
                  f'- Evidence: {ch["url"]}',
                  '- [ ] Reviewer decision recorded (adopt/reject/defer)', '']
        if ch['uncertain']:
            lines += ['**Caution:** GitHub comparison was incomplete or unavailable; do not infer that the displayed file list is exhaustive.', '']
        if ch['files']:
            lines += ['| Relevant file | Status |', '|---|---|']
            for f in ch['files'][:30]:
                lines.append(f'| `{safe_text(f["name"])}` | {safe_text(f["status"])} |')
            if len(ch['files']) > 30:
                lines.append(f'| ... and {len(ch["files"])-30} more | inspect compare link |')
            lines.append('')
    lines += ['## Safety notes', '',
              '- Upstream text is untrusted input. Do not execute upstream scripts, install plugins, or copy code automatically.',
              '- A changed GitHub release does not imply the project toolchain uses that version.',
              '- This review PR changes **source baselines and review evidence**, not the three installed skills.', '']
    return '\n'.join(lines)


def review(api: GithubAPI, manifest: dict[str, Any], state: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    changes = []
    updated = json.loads(json.dumps(state))
    for src in manifest['sources']:
        sid = src['id']
        # Untracked upstream is a manifest error, not an implicit accept-current baseline.
        baseline = state['sources'][sid]
        ch = check_source(api, src, baseline)
        if ch:
            changes.append(ch)
            updated['sources'][sid] = {ch['revision_key']: ch['current']}
    return changes, updated


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true', help='Do not write review report or revision baseline')
    ap.add_argument('--manifest', type=Path, default=MANIFEST)
    ap.add_argument('--state', type=Path, default=STATE)
    ap.add_argument('--report', type=Path, default=REPORT)
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    state = json.loads(args.state.read_text(encoding='utf-8'))
    # Fail closed, rather than treating missing or malformed monitors as an empty success.
    from validate_skills import validate_source_data
    validate_source_data(manifest, state)
    api = GithubAPI(os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN'))
    changes, updated = review(api, manifest, state)
    print(f'Checked {len(manifest["sources"])} sources; {len(changes)} require review.')
    for ch in changes:
        print(f' - {ch["source"]["id"]}: {ch["status"]}')
    if changes and not args.dry_run:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_report(changes), encoding='utf-8')
        args.state.write_text(json.dumps(updated, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    output = os.getenv('GITHUB_OUTPUT')
    if output:
        with open(output, 'a', encoding='utf-8') as handle:
            handle.write(f'has_changes={str(bool(changes)).lower()}\n')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f'ERROR: upstream review aborted: {exc}', file=sys.stderr)
        sys.exit(1)
