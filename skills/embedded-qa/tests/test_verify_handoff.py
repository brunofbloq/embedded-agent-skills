import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_handoff import verify


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_handoff.py"


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / "manifest.json"
        self.data = {"schema_version": 1, "required_paths": ["src/main.c"],
                     "artifacts": []}
        for role, name in (("source", "src/main.c"), ("config", "config.h"),
                           ("license", "LICENSE"), ("evidence", "log.txt"),
                           ("firmware", "image.bin")):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            content = (b"source\n" * 180000 if role == "source" else b"fixture\n")
            target.write_bytes(content)
            self.data["artifacts"].append({"path": name, "role": role,
                                          "sha256": hashlib.sha256(content).hexdigest()})

    def write(self, data=None):
        self.manifest.write_text(json.dumps(self.data if data is None else data),
                                 encoding="utf-8")

    def rejected(self, data=None):
        self.write(data)
        with self.assertRaises((ValueError, OSError)):
            verify(self.root, self.manifest)

    def test_valid_bundle(self):
        self.write()
        self.assertEqual(verify(self.root, self.manifest), 5)

    def test_changed_and_missing_files(self):
        target = self.root / "src/main.c"
        target.write_bytes(b"changed")
        self.rejected()
        target.unlink()
        self.rejected()

    def test_duplicate_paths(self):
        for case_variant in (False, True):
            data = copy.deepcopy(self.data)
            duplicate = copy.deepcopy(data["artifacts"][0])
            if case_variant:
                duplicate["path"] = duplicate["path"].upper()
            data["artifacts"].append(duplicate)
            with self.subTest(case_variant=case_variant):
                self.rejected(data)
        self.data["required_paths"] *= 2
        self.rejected()

    def test_required_omission_and_missing_source(self):
        self.data["required_paths"].append("omitted.h")
        self.rejected()
        self.data["required_paths"].pop()
        self.data["artifacts"][0]["role"] = "firmware"
        self.rejected()

    def test_invalid_schema_and_types(self):
        cases = [None, [], True, 1, "manifest", {},
                 {**self.data, "extra": 1}]
        for key, values in {
            "schema_version": [True, False, "1", 1.0, 2, None, []],
            "required_paths": [None, {}, "src/main.c", [], [None], [1], [True], [[]]],
            "artifacts": [None, {}, "artifact", [], [None], [True], [[]], [{}]],
        }.items():
            cases.extend({**self.data, key: value} for value in values)
        for key in self.data:
            cases.append({k: v for k, v in self.data.items() if k != key})
        for data in cases:
            with self.subTest(data=data):
                # None is a deliberate invalid JSON root here.
                self.manifest.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(ValueError):
                    verify(self.root, self.manifest)

    def test_invalid_artifact_fields(self):
        for key, values in {
            "sha256": [None, 1, True, [], {}, "a" * 63, "a" * 65,
                       "A" * 64, "g" * 64, "a" * 64 + "\n"],
            "role": [None, 1, True, [], {}, "unknown", "SOURCE"],
            "path": [None, 1, True, [], {}, ""],
        }.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    data = copy.deepcopy(self.data)
                    data["artifacts"][0][key] = value
                    self.rejected(data)
        for key in ("path", "sha256", "role"):
            data = copy.deepcopy(self.data)
            del data["artifacts"][0][key]
            self.rejected(data)
        self.data["artifacts"][0]["extra"] = 1
        self.rejected()

    def test_unsafe_paths_in_both_lists(self):
        paths = ["../outside", "src/../../outside", "/absolute", "//server/share",
                 "C:/outside", "C:outside", "C:\\outside", "\\\\server\\share",
                 "src\\main.c", "src/./main.c", "src//main.c", "src/",
                 "src/../src/main.c", "src/main.c\x00", "src/main.c."]
        for name in paths:
            for field in ("required_paths", "artifacts"):
                with self.subTest(name=name, field=field):
                    data = copy.deepcopy(self.data)
                    if field == "required_paths":
                        data[field] = [name]
                    else:
                        data[field][0]["path"] = name
                    self.rejected(data)

    def test_malformed_json_and_duplicate_keys(self):
        for content in ("{", '{"schema_version":1,"schema_version":1}',
                        json.dumps(self.data).replace('"role": "source"',
                                                     '"role":"source","role":"source"')):
            self.manifest.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                verify(self.root, self.manifest)

    def test_directory_and_missing_manifest_or_root(self):
        (self.root / "config.h").unlink()
        (self.root / "config.h").mkdir()
        self.rejected()
        self.manifest.unlink()
        with self.assertRaises(OSError):
            verify(self.root, self.manifest)
        with self.assertRaises(ValueError):
            verify(self.root / "absent", self.manifest)

    def test_symlink_file_directory_root_and_manifest(self):
        target = self.root / "config.h"
        alias = self.root / "alias"
        try:
            alias.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        self.addCleanup(lambda: alias.unlink(missing_ok=True))
        self.data["artifacts"][1]["path"] = "alias"
        self.rejected()
        alias.unlink()
        alias.symlink_to(self.root / "src", target_is_directory=True)
        self.data["artifacts"][0]["path"] = "alias/main.c"
        self.data["required_paths"] = ["alias/main.c"]
        self.rejected()
        self.write()
        with self.assertRaises(ValueError):
            verify(alias, self.manifest)
        alias.unlink()
        alias.symlink_to(self.manifest)
        with self.assertRaises(ValueError):
            verify(self.root, alias)

    def test_cli_status_and_wording(self):
        self.write()
        command = [sys.executable, "-B", str(SCRIPT), "--root", str(self.root),
                   "--manifest", str(self.manifest)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("declared artifacts verified", result.stdout.lower())
        self.assertNotIn("test", result.stdout.lower())
        (self.root / "config.h").unlink()
        for args in (command, command[:3]):
            result = subprocess.run(args, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("verification failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
