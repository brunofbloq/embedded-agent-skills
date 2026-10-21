"""Verify declared handoff artifacts, without interpreting test evidence."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import sys


ROLES = {"source", "config", "license", "evidence", "firmware"}


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _path(value):
    if (not isinstance(value, str) or not value or "\\" in value
            or ":" in value or "\x00" in value or value.startswith("/")
            or PureWindowsPath(value).drive
            or any(part in {"", ".", ".."} or part.endswith((" ", "."))
                   or re.match(r"(?i)^(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(?:\.|$)", part)
                   for part in value.split("/"))):
        raise ValueError(f"invalid relative path: {value!r}")
    return value


def _no_symlinks(path):
    for component in (path, *path.parents):
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        if (stat.S_ISLNK(info.st_mode)
                or getattr(info, "st_file_attributes", 0) & 0x400):
            raise ValueError(f"symlink/junction path rejected: {component}")


def _identity(info):
    # Windows stat/fstat can expose creation/change time differently as ctime.
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns if os.name != "nt" else None)


def verify(root, manifest):
    """Return the artifact count; raise ValueError/OSError on rejection."""
    root, manifest = Path(root).absolute(), Path(manifest).absolute()
    _no_symlinks(root)
    _no_symlinks(manifest)
    if not root.is_dir():
        raise ValueError("root must be an existing directory")
    with manifest.open(encoding="utf-8") as stream:
        data = json.load(stream, object_pairs_hook=_object)
    if (type(data) is not dict
            or set(data) != {"schema_version", "required_paths", "artifacts"}
            or type(data["schema_version"]) is not int
            or data["schema_version"] != 1):
        raise ValueError("invalid manifest schema; expected schema_version 1")
    required, artifacts = data["required_paths"], data["artifacts"]
    if type(required) is not list or not required:
        raise ValueError("required_paths must be a nonempty list")
    if type(artifacts) is not list or not artifacts:
        raise ValueError("artifacts must be a nonempty list")
    required = [_path(value) for value in required]
    if len({value.casefold() for value in required}) != len(required):
        raise ValueError("duplicate required path")
    declared, seen, sources = {}, set(), False
    for artifact in artifacts:
        if type(artifact) is not dict or set(artifact) != {"path", "sha256", "role"}:
            raise ValueError("invalid artifact schema")
        name = _path(artifact["path"])
        digest, role = artifact["sha256"], artifact["role"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"invalid lowercase SHA256: {name}")
        if not isinstance(role, str) or role not in ROLES:
            raise ValueError(f"invalid artifact role: {name}")
        if name.casefold() in seen:
            raise ValueError(f"duplicate artifact path: {name}")
        seen.add(name.casefold())
        declared[name] = digest
        sources |= role == "source"
    if not sources:
        raise ValueError("at least one source-role artifact is required")
    if not set(required) <= declared.keys():
        raise ValueError("required paths missing from artifacts")
    for name, expected in declared.items():
        target = root.joinpath(*name.split("/"))
        _no_symlinks(target)
        before = target.stat()
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"artifact is not a regular file: {name}")
        digest = hashlib.sha256()
        with target.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            if _identity(opened) != _identity(before):
                raise ValueError(f"artifact changed while opening: {name}")
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
            after = os.fstat(stream.fileno())
        _no_symlinks(target)
        if (_identity(after) != _identity(opened)
                or _identity(target.stat()) != _identity(after)):
            raise ValueError(f"artifact changed during verification: {name}")
        if digest.hexdigest() != expected:
            raise ValueError(f"SHA256 mismatch: {name}")
    return len(declared)


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv=None):
    parser = _Parser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--manifest", required=True)
    try:
        args = parser.parse_args(argv)
        count = verify(args.root, args.manifest)
    except (ValueError, OSError, RecursionError) as exc:
        print(f"Declared artifacts verification failed: {exc}", file=sys.stderr)
        return 1
    print(f"Declared artifacts verified: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
