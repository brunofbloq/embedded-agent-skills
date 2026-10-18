#!/usr/bin/env python3
"""Create individually installable skill.zip files with deterministic ZIP metadata."""
from __future__ import annotations
import argparse
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from validate_skills import ROOT, SKILL_NAMES, validate_skill


def package(folder: Path, destination: Path) -> None:
    validate_skill(folder)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, 'w', compression=ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix == '.pyc':
                continue
            arcname = '/'.join((folder.name, *path.relative_to(folder).parts))
            info = ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o644 << 16)
            archive.writestr(info, path.read_bytes())
    with ZipFile(destination) as z:
        assert z.testzip() is None
        assert f'{folder.name}/SKILL.md' in z.namelist()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    for name in sorted(SKILL_NAMES):
        path = args.output / name / 'skill.zip'
        package(ROOT / 'skills' / name, path)
        print(f'Created {path}')


if __name__ == '__main__':
    main()
