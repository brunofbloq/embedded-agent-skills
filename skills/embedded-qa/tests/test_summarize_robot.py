import tempfile
import unittest
from pathlib import Path
from sys import path

path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from summarize_robot import summarize


class ReportTests(unittest.TestCase):
    def run_report(self, fragment):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "output.xml"
            p.write_text(f'<robot><suite name="example">{fragment}</suite></robot>')
            return summarize(p)

    def test_pass(self):
        r = self.run_report('<test name="A"><status status="PASS"/></test>')
        self.assertEqual((r["state"], r["executed"]), ("PASS", 1))

    def test_fail(self):
        r = self.run_report('<test name="A"><status status="FAIL">bad</status></test>')
        self.assertEqual(r["state"], "FAIL")
        self.assertEqual(r["failed_tests"][0]["name"], "A")

    def test_skipped(self):
        r = self.run_report('<test name="A"><status status="SKIP"/></test>')
        self.assertEqual(r["state"], "INCOMPLETE")
        self.assertEqual(r["executed"], 0)

    def test_zero(self):
        self.assertEqual(self.run_report("")["state"], "INCOMPLETE")

    def test_invalid_xml(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "output.xml"
            p.write_text("<broken>")
            self.assertEqual(summarize(p)["state"], "FAIL")

    def test_unknown_status(self):
        self.assertEqual(self.run_report('<test name="A"><status status="UNKNOWN"/></test>')["state"], "FAIL")

    def test_missing_status(self):
        self.assertEqual(self.run_report('<test name="A"/>')["state"], "FAIL")

    def test_root_must_be_robot(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "output.xml"
            p.write_text('<suite name="fake"><test name="A"><status status="PASS"/></test></suite>')
            self.assertEqual(summarize(p)["state"], "FAIL")


if __name__ == "__main__":
    unittest.main()
