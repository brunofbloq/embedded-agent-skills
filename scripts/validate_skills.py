#!/usr/bin/env python3
"""Portable validation: no PyYAML, LLM or framework dependency required."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = {'embedded-architect', 'embedded-developer', 'embedded-qa'}
SHA_RE = re.compile(r'[a-f0-9]{40}\Z')


def validate_source_data(manifest: dict, revisions: dict) -> None:
    if manifest.get('schema_version') != 1 or revisions.get('schema_version') != 1:
        raise ValueError('Unsupported source manifest/revision schema')
    entries = manifest.get('sources')
    if not isinstance(entries, list) or not entries:
        raise ValueError('Empty/missing source definitions')
    states = revisions.get('sources')
    if not isinstance(states, dict):
        raise ValueError('Missing source baselines')
    seen = set()
    for src in entries:
        ident = src['id']
        if not re.fullmatch(r'[a-z0-9-]+', ident) or ident in seen:
            raise ValueError(f'Invalid/duplicate monitor ID: {ident}')
        seen.add(ident)
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', src['repo']):
            raise ValueError(f'Invalid repository: {ident}')
        if not set(src['skills']) <= SKILL_NAMES or not src['skills']:
            raise ValueError(f'Invalid target skill list: {ident}')
        mode = src['mode']
        old = states.get(ident)
        if not isinstance(old, dict):
            raise ValueError(f'Missing baseline: {ident}')
        if mode == 'files':
            if not re.fullmatch(r'[a-zA-Z0-9._/-]+', src.get('ref', '')):
                raise ValueError(f'Invalid branch ref: {ident}')
            if not isinstance(src.get('paths'), list) or not src['paths']:
                raise ValueError(f'Missing watched paths: {ident}')
            if any(not isinstance(p, str) or '..' in p or p.startswith('/') or not p for p in src['paths']):
                raise ValueError(f'Invalid watched path: {ident}')
            if not SHA_RE.fullmatch(old.get('commit', '')):
                raise ValueError(f'Invalid commit baseline: {ident}')
        elif mode == 'release':
            if not re.fullmatch(r'[A-Za-z0-9_.+-]{1,100}', old.get('tag', '')):
                raise ValueError(f'Invalid tag baseline: {ident}')
        else:
            raise ValueError(f'Unsupported source mode for {ident}: {mode}')
    if set(states) != seen:
        raise ValueError('Source baselines differ from defined monitors')


def validate_skill(path: Path) -> None:
    entry = path / 'SKILL.md'
    if not entry.exists():
        raise ValueError(f'Missing SKILL.md in {path}')
    text = entry.read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.DOTALL)
    if not match:
        raise ValueError(f'Invalid skill YAML boundary: {entry}')
    meta = match.group(1)
    keys = re.findall(r'^([\w-]+):', meta, re.MULTILINE)
    if sorted(keys) != ['description', 'name']:
        raise ValueError(f'Skill must contain only name/description frontmatter: {entry}')
    actual = re.search(r'^name:\s*(\S+)\s*$', meta, re.MULTILINE)
    if not actual or actual.group(1) != path.name:
        raise ValueError(f'Wrong skill name: {path.name}')
    if len(text.splitlines()) > 500:
        raise ValueError(f'Skill entrypoint too large: {path.name}')
    if len(re.search(r'^description:\s*(.*)$', meta, re.MULTILINE).group(1)) < 60:
        raise ValueError(f'Skill description too vague: {path.name}')
    if not (path / 'agents' / 'openai.yaml').exists():
        raise ValueError(f'Missing UI metadata: {path.name}')
    for target in re.findall(r'\]\((references/[^)]+|assets/[^)]+)\)', text):
        dest = path / target
        if not dest.is_file() or not dest.resolve().is_relative_to(path.resolve()):
            raise ValueError(f'Broken reference {target} in {path.name}')
    for candidate in path.rglob('*'):
        if candidate.is_symlink():
            raise ValueError(f'Unexpected symlink in skill: {candidate}')


def main() -> None:
    manifest = json.loads((ROOT / 'maintenance' / 'sources.json').read_text(encoding='utf-8'))
    revisions = json.loads((ROOT / 'maintenance' / 'reviewed-revisions.json').read_text(encoding='utf-8'))
    validate_source_data(manifest, revisions)
    dirs = {p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()}
    if dirs != SKILL_NAMES:
        raise ValueError(f'Unexpected skills: {dirs}')
    for name in sorted(SKILL_NAMES):
        validate_skill(ROOT / 'skills' / name)
    print(f'PASS: {len(SKILL_NAMES)} skills and {len(manifest["sources"])} upstream monitors')


if __name__ == '__main__':
    try:
        main()
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
