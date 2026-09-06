import unittest
import csv
import hashlib
import json
import subprocess
import tempfile

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.measured_authority_gate import (
    COLLECTIVE_GRID,
    evaluate_rows,
    minimum_authority_over_band,
    mixer_torque_authority,
)


def rows(torque_n_m=0.025, repeats=6):
    return [
        {
            "voltage_v": 7.0,
            "collective_fraction": collective,
            "tau_rp_n_m": torque_n_m,
        }
        for collective in COLLECTIVE_GRID
        for _ in range(repeats)
    ]


def evidence_bundle(root, data, kind="measured"):
    """Generated software fixture only; 'measured' exercises a label, not hardware."""
    raw = []
    for index, row in enumerate(data):
        row.setdefault("sample_id", "derived-{}".format(index))
        row.setdefault("raw_record_id", "raw-{}".format(index))
        row.setdefault("motor_id", "motor-{}".format(index % 6))
        row.setdefault("expanded_uncertainty_n_m", 0.001)
        raw.append({"record_id": row["raw_record_id"], "motor_id": row["motor_id"],
                    "voltage_v": row["voltage_v"], "collective_fraction": row["collective_fraction"],
                    "thrust_n": 1.05, "current_a": 3.0, "temperature_c": 25.0,
                    "rpm": 10000, "time_s": index, "arm_m": 0.06, "calibration_id": "fixture-cal"})
    for name, records in (("authority.csv", data), ("raw.csv", raw)):
        with (root / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    for name in ("calibration.txt", "uncertainty.txt", "derivation.txt"):
        (root / name).write_text("SYNTHETIC SOFTWARE TEST ONLY: " + name, encoding="utf-8")
    def artifact(name):
        return {"path": name, "sha256": hashlib.sha256((root / name).read_bytes()).hexdigest()}
    manifest = {"schema_version": 1, "evidence_kind": kind,
                "motor_ids": ["motor-{}".format(i) for i in range(6)],
                "calibration_id": "fixture-cal",
                "calibration_quantities": ["thrust_n", "voltage_v", "current_a", "temperature_c", "rpm", "time_s", "arm_m"],
                "review": {"status": "accepted", "reviewer": "SYNTHETIC TEST", "reviewed_on": "2026-09-05"},
                "artifacts": {"derived": artifact("authority.csv"), "raw": artifact("raw.csv"),
                              "calibration": artifact("calibration.txt"), "uncertainty": artifact("uncertainty.txt"),
                              "derivation": artifact("derivation.txt")}}
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


class EvidenceContractTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def evaluate(self, data, kind="measured"):
        manifest = evidence_bundle(self.root, data, kind)
        return evaluate_rows(data, evidence_path=manifest)

    def test_three_columns_alone_cannot_pass(self):
        self.assertEqual(evaluate_rows(rows()).classification, "INCONCLUSIVE")

    def test_valid_reviewed_fixture_preserves_threshold(self):
        verdict = self.evaluate(rows())
        self.assertEqual(verdict.classification, "PASS")
        self.assertAlmostEqual(verdict.conservative_minimum_n_m, 0.024)

    def test_uncertainty_can_cross_frozen_threshold(self):
        data = rows(0.0205)
        self.assertEqual(self.evaluate(data).classification, "FAIL")

    def test_exact_registered_threshold_and_tolerance_endpoints(self):
        data = rows(0.021)
        for row in data:
            row["voltage_v"] = 7.05
            row["collective_fraction"] += 0.002
        self.assertEqual(self.evaluate(data).classification, "PASS")

    def test_outside_voltage_or_grid_tolerance_is_inconclusive(self):
        for field, value in (("voltage_v", 7.051), ("collective_fraction", 0.253)):
            with self.subTest(field=field):
                data = rows()
                data[0][field] = value
                self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_bool_is_not_a_numeric_measurement(self):
        data = rows()
        data[0]["expanded_uncertainty_n_m"] = False
        self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_raw_telemetry_and_derived_motor_must_agree(self):
        for field, value in (("motor_id", "motor-1"), ("rpm", "nan"), ("arm_m", "0")):
            with self.subTest(field=field):
                data = rows()
                path = evidence_bundle(self.root, data)
                with (self.root / "raw.csv").open(newline="") as handle:
                    raw = list(csv.DictReader(handle))
                raw[0][field] = value
                with (self.root / "raw.csv").open("w", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(raw[0]))
                    writer.writeheader()
                    writer.writerows(raw)
                manifest = json.loads(path.read_text())
                manifest["artifacts"]["raw"]["sha256"] = hashlib.sha256((self.root / "raw.csv").read_bytes()).hexdigest()
                path.write_text(json.dumps(manifest))
                self.assertEqual(evaluate_rows(data, evidence_path=path).classification, "INCONCLUSIVE")

    def test_synthetic_label_cannot_authorize_physical_gate(self):
        verdict = self.evaluate(rows(), kind="synthetic")
        self.assertEqual(verdict.classification, "DEVELOPMENT_ONLY")
        self.assertEqual(verdict.numerical_result, "PASS")

    def test_six_distinct_motors_required_at_every_point(self):
        data = rows()
        for row in data:
            row["motor_id"] = "motor-0"
        self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_unique_derived_and_raw_observations_required(self):
        for field in ("sample_id", "raw_record_id"):
            with self.subTest(field=field):
                data = rows()
                data[0][field] = "duplicate"
                data[1][field] = "duplicate"
                self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_negative_nonfinite_or_missing_uncertainty_is_inconclusive(self):
        for value in (-0.001, float("nan"), float("inf"), None):
            with self.subTest(value=value):
                data = rows()
                data[0]["expanded_uncertainty_n_m"] = value
                self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_tampered_source_and_missing_calibration_cannot_pass(self):
        for filename in ("raw.csv", "calibration.txt", "uncertainty.txt", "derivation.txt"):
            with self.subTest(filename=filename):
                data = rows()
                manifest = evidence_bundle(self.root, data)
                (self.root / filename).write_text("altered", encoding="utf-8")
                self.assertEqual(evaluate_rows(data, evidence_path=manifest).classification, "INCONCLUSIVE")

    def test_unreviewed_or_incomplete_manifest_cannot_pass(self):
        for field in ("review", "motor_ids", "calibration_quantities", "artifacts"):
            with self.subTest(field=field):
                data = rows()
                path = evidence_bundle(self.root, data)
                manifest = json.loads(path.read_text())
                del manifest[field]
                path.write_text(json.dumps(manifest))
                self.assertEqual(evaluate_rows(data, evidence_path=path).classification, "INCONCLUSIVE")

    def test_rows_must_match_hashed_derived_artifact(self):
        data = rows()
        manifest = evidence_bundle(self.root, data)
        data[0]["tau_rp_n_m"] = 0.5
        self.assertEqual(evaluate_rows(data, evidence_path=manifest).classification, "INCONCLUSIVE")

    def test_cli_is_strict_json_and_nonzero_for_missing_or_synthetic_evidence(self):
        data = rows()
        manifest = evidence_bundle(self.root, data, "synthetic")
        command = [sys.executable, "-m", "Analysis.measured_authority_gate", str(self.root / "authority.csv")]
        for options, code, classification in (([], 2, "INCONCLUSIVE"),
                                               (["--manifest", str(manifest)], 3, "DEVELOPMENT_ONLY")):
            result = subprocess.run(command + options, capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stderr)
            self.assertEqual(json.loads(result.stdout)["classification"], classification)


class MeasuredAuthorityGateTests(unittest.TestCase):
    def evaluate(self, data):
        with tempfile.TemporaryDirectory() as directory:
            manifest = evidence_bundle(Path(directory), data)
            return evaluate_rows(data, evidence_path=manifest)

    def test_nonfinite_measurements_are_inconclusive(self):
        for field in ("voltage_v", "collective_fraction", "tau_rp_n_m"):
            for invalid in (float("inf"), float("-inf"), float("nan")):
                with self.subTest(field=field, invalid=invalid):
                    data = rows()
                    data[0][field] = invalid
                    self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_unphysical_measurements_are_inconclusive(self):
        for field, invalid in (("voltage_v", -7.0), ("collective_fraction", -0.1),
                               ("collective_fraction", 1.1), ("tau_rp_n_m", -0.01)):
            with self.subTest(field=field, invalid=invalid):
                data = rows()
                data[0][field] = invalid
                self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_nominal_prediction_clears_registered_threshold(self):
        self.assertAlmostEqual(
            minimum_authority_over_band(total_max_thrust_n=4.2, arm_m=0.060),
            0.0445477272147525,
            places=12,
        )

    def test_authority_is_zero_at_zero_and_full_collective(self):
        self.assertEqual(mixer_torque_authority(4.2, 0.060, 0.0), 0.0)
        self.assertEqual(mixer_torque_authority(4.2, 0.060, 1.0), 0.0)

    def test_pass_requires_every_collective_point(self):
        self.assertEqual(self.evaluate(rows()).classification, "PASS")
        data = rows()
        data = [row for row in data if row["collective_fraction"] != 0.75]
        self.assertEqual(self.evaluate(data).classification, "INCONCLUSIVE")

    def test_fifth_percentile_below_threshold_fails(self):
        data = rows()
        for row in data:
            if row["collective_fraction"] == 0.625:
                row["tau_rp_n_m"] = 0.019
        self.assertEqual(self.evaluate(data).classification, "FAIL")


if __name__ == "__main__":
    unittest.main()
