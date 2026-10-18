#!/usr/bin/env python3
"""Summarize Robot Framework output.xml as compact, CI-friendly JSON.

Exit: 0 PASS, 1 FAIL (including malformed/unreadable XML), 2 INCOMPLETE.
This script does not run Renode or assert hardware correctness.
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def summarize(path: Path) -> dict:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return {"state": "FAIL", "error": f"Unreadable Robot XML: {exc}"}
    if root.tag != "robot":
        return {"state": "FAIL", "error": "Expected Robot Framework <robot> root"}
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    failures = []
    for test in root.iter("test"):
        status = test.find("status")
        outcome = (status.get("status", "") if status is not None else "").upper()
        if outcome not in counts:
            return {"state": "FAIL", "error": f"Missing/unknown status for {test.get('name', '?')}"}
        counts[outcome] += 1
        if outcome == "FAIL":
            failures.append({"name": test.get("name", "?"), "message": (status.text or "").strip()[:300]})
    total = sum(counts.values())
    if counts["FAIL"]:
        state = "FAIL"
    elif total == 0 or counts["SKIP"]:
        state = "INCOMPLETE"
    else:
        state = "PASS"
    return {"state": state, "executed": total - counts["SKIP"], "counts": counts, "failed_tests": failures[:10]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path, help="Robot Framework output.xml")
    args = parser.parse_args()
    result = summarize(args.xml)
    print(json.dumps(result, sort_keys=True))
    return {"PASS": 0, "FAIL": 1, "INCOMPLETE": 2}[result["state"]]


if __name__ == "__main__":
    sys.exit(main())
