import unittest

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


class MeasuredAuthorityGateTests(unittest.TestCase):
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
        self.assertEqual(evaluate_rows(rows()).classification, "PASS")
        data = rows()
        data = [row for row in data if row["collective_fraction"] != 0.75]
        self.assertEqual(evaluate_rows(data).classification, "INCONCLUSIVE")

    def test_fifth_percentile_below_threshold_fails(self):
        data = rows()
        for row in data:
            if row["collective_fraction"] == 0.625:
                row["tau_rp_n_m"] = 0.019
        self.assertEqual(evaluate_rows(data).classification, "FAIL")


if __name__ == "__main__":
    unittest.main()
