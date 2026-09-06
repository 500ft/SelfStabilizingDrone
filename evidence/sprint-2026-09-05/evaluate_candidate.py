#!/usr/bin/env python3
"""Bounded synthetic consumer checks; not independent or physical validation."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from Analysis.tests.test_measured_authority_gate import evidence_bundle, rows

CASES = (
    ("nominal synthetic", "DEVELOPMENT_ONLY", 3, "PASS"),
    ("below-threshold synthetic", "DEVELOPMENT_ONLY", 3, "FAIL"),
    ("missing calibration file", "INCONCLUSIVE", 2, None),
    ("reused raw observation", "INCONCLUSIVE", 2, None),
    ("missing uncertainty", "INCONCLUSIVE", 2, None),
    ("raw operating-point mismatch with updated hash", "INCONCLUSIVE", 2, None),
    ("malformed manifest array", "INCONCLUSIVE", 2, None),
    ("measured-label branch on synthetic records", "PASS", 0, "PASS"),
    ("empty derived file with matching hash", "INCONCLUSIVE", 2, None),
    ("8.4 V reference rows only", "INCONCLUSIVE", 2, None),
)


def reject_nonfinite(value):
    raise ValueError("non-standard JSON number: " + value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = []
    for name, classification, code, numerical in CASES:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = rows(0.019 if name == "below-threshold synthetic" else 0.025)
            if name == "reused raw observation":
                data[0]["raw_record_id"] = data[1]["raw_record_id"] = "duplicate"
            if name == "missing uncertainty":
                data[0]["expanded_uncertainty_n_m"] = None
            if name == "8.4 V reference rows only":
                for row in data:
                    row["voltage_v"] = 8.4
            kind = "measured" if name == "measured-label branch on synthetic records" else "synthetic"
            path = evidence_bundle(root, data, kind)
            manifest = json.loads(path.read_text())
            if name == "missing calibration file":
                (root / "calibration.txt").unlink()
            if name == "raw operating-point mismatch with updated hash":
                with (root / "raw.csv").open(newline="") as handle:
                    records = list(csv.DictReader(handle))
                records[0]["voltage_v"] = "7.1"
                with (root / "raw.csv").open("w", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(records[0]))
                    writer.writeheader()
                    writer.writerows(records)
                manifest["artifacts"]["raw"]["sha256"] = hashlib.sha256((root / "raw.csv").read_bytes()).hexdigest()
            if name == "malformed manifest array":
                manifest = []
            if name == "empty derived file with matching hash":
                (root / "authority.csv").write_text("")
                manifest["artifacts"]["derived"]["sha256"] = hashlib.sha256(b"").hexdigest()
            path.write_text(json.dumps(manifest))
            command = [sys.executable, "-m", "Analysis.measured_authority_gate",
                       str(root / "authority.csv"), "--manifest", str(path)]
            process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            payload = json.loads(process.stdout, parse_constant=reject_nonfinite)
            observed = (payload["classification"], process.returncode, payload["numerical_result"])
            expected = (classification, code, numerical)
            results.append({"case": name, "all_inputs_synthetic": True, "expected": expected,
                            "observed": observed, "matches": observed == expected,
                            "stdout": payload, "stderr": process.stderr,
                            "command": "python -m Analysis.measured_authority_gate TEMP/authority.csv --manifest TEMP/manifest.json"})
    report = {"scope": "developer synthetic consistency checks; not hardware or independent evaluation",
              "python": sys.version, "candidate_sha256": hashlib.sha256((ROOT / "Analysis/measured_authority_gate.py").read_bytes()).hexdigest(),
              "case_count": len(results), "matched": sum(result["matches"] for result in results),
              "results": results}
    text = json.dumps(report, indent=2, allow_nan=False)
    print(text)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    return 0 if all(result["matches"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

