import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis import rigid_body
from Analysis.monte_carlo_recovery import clopper_pearson_lower, draw_case
from Analysis.sim_release_recovery import (DroneParams, Imperfections, _control,
                                           axis_angle_quat, best_params,
                                           max_recoverable_rate, nominal_params,
                                           quat_mul, quat_to_rotmat, simulate,
                                           worst_params)


class TestPrimitives(unittest.TestCase):
    def test_identity_rotmat(self):
        np.testing.assert_allclose(quat_to_rotmat(np.array([1.0, 0, 0, 0])), np.eye(3), atol=1e-12)

    def test_quat_mul_matches_kernel(self):
        a = (0.5, 0.5, 0.5, 0.5)
        b = (0.7071, 0.0, 0.7071, 0.0)
        mine = quat_mul(np.array(a), np.array(b))
        kernel = rigid_body.quaternion_multiply(a, b)
        np.testing.assert_allclose(mine, kernel, atol=1e-9)

    def test_axis_angle_90deg_about_z(self):
        q = axis_angle_quat(np.array([0.0, 0.0, 1.0]), math.pi / 2)
        R = quat_to_rotmat(q)
        np.testing.assert_allclose(R @ np.array([1.0, 0, 0]), [0, 1, 0], atol=1e-9)


class TestRecovery(unittest.TestCase):
    def test_nominal_recovers_within_envelope(self):
        r = simulate(nominal_params(), 2.0, math.radians(60))
        self.assertTrue(r["success"])
        self.assertIsNotNone(r["recovery_time_s"])
        self.assertLess(r["final_tilt_deg"], 5.0)
        self.assertLess(r["max_descent_m"], r["available_height_m"])

    def test_envelope_has_a_limit(self):
        # not trivially always-success: a high tumble rate beats the worst-tier authority
        self.assertFalse(simulate(worst_params(), 5.0, math.radians(60))["success"])
        # ...but the same rate is fine for the high-authority best tier
        self.assertTrue(simulate(best_params(), 2.0, math.radians(60))["success"])

    def test_envelope_orders_by_control_authority(self):
        b = max_recoverable_rate(best_params(), math.radians(60))
        n = max_recoverable_rate(nominal_params(), math.radians(60))
        w = max_recoverable_rate(worst_params(), math.radians(60))
        self.assertGreater(b, n)
        self.assertGreater(n, w)

    def test_no_nans_and_bounded_tilt(self):
        log = simulate(nominal_params(), 2.0, math.radians(60))["log"]
        for key, arr in log.items():
            self.assertFalse(np.any(np.isnan(arr)), f"NaN in {key}")
        self.assertTrue(np.all(log["tilt"] >= -1e-9) and np.all(log["tilt"] <= math.pi + 1e-9))


class TestEnvelopeEdge(unittest.TestCase):
    def test_scan_capped_at_gyro_limit(self):
        # the envelope can never exceed what the gyro can measure
        p = best_params()
        rate, edge = max_recoverable_rate(p, math.radians(60), with_edge=True)
        self.assertLessEqual(rate, p.gyro_limit_rad_s + 1e-9)
        self.assertIn(edge, ("failure", "gyro_limit"))

    def test_nominal_edge_is_a_real_failure(self):
        rate, edge = max_recoverable_rate(nominal_params(), math.radians(60), with_edge=True)
        self.assertEqual(edge, "failure")
        self.assertGreater(rate, 0.0)


class TestImperfections(unittest.TestCase):
    def test_default_imperfections_change_nothing(self):
        r0 = simulate(nominal_params(), 2.0, math.radians(60))
        r1 = simulate(nominal_params(), 2.0, math.radians(60), imperfections=Imperfections())
        np.testing.assert_allclose(r0["log"]["tilt"], r1["log"]["tilt"], atol=0.0)

    def test_seeded_runs_are_repeatable(self):
        imp = Imperfections(gyro_noise_rad_s=0.02, tilt_noise_rad=math.radians(2), seed=7)
        a = simulate(nominal_params(), 2.0, math.radians(60), imperfections=imp)
        b = simulate(nominal_params(), 2.0, math.radians(60), imperfections=imp)
        np.testing.assert_allclose(a["log"]["tilt"], b["log"]["tilt"], atol=0.0)

    def test_cg_offset_disturbance_defeats_placeholder_authority(self):
        # documented finding: >=2 mm thrust-line offset exceeds the placeholder
        # 0.004 N*m budget at recovery thrust and recovery fails
        imp = Imperfections(cg_offset_m=(0.002, 0.0))
        r = simulate(nominal_params(), 2.0, math.radians(60), imperfections=imp)
        self.assertFalse(r["success"])

    def test_battery_sag_caps_thrust(self):
        imp = Imperfections(thrust_scale=0.9)
        p = nominal_params()
        r = simulate(p, 2.0, math.radians(60), imperfections=imp)
        self.assertLessEqual(r["peak_thrust_n"], 0.9 * p.max_thrust_n + 1e-9)

    def test_clopper_pearson_bounds(self):
        self.assertEqual(clopper_pearson_lower(0, 100), 0.0)
        self.assertAlmostEqual(clopper_pearson_lower(100, 100), 0.05 ** 0.01, places=6)
        lb = clopper_pearson_lower(90, 100)
        self.assertGreater(lb, 0.80)
        self.assertLess(lb, 0.90)

    def test_draw_case_respects_cg_cap(self):
        rng = np.random.default_rng(0)
        for _ in range(50):
            _, imp = draw_case(rng, cg_offset_max_m=0.001)
            self.assertLessEqual(math.hypot(*imp.cg_offset_m), 0.001 + 1e-12)


class TestSaturation(unittest.TestCase):
    def test_controller_respects_actuator_limits(self):
        p = nominal_params()
        q = axis_angle_quat(np.array([0.0, 1.0, 0.0]), math.radians(60))
        omega = np.array([10.0, -8.0, 3.0])           # aggressive tumble
        pos = np.array([0.0, 0.0, -1.5]); vel = np.array([0.0, 0.0, -6.0])
        torque, thrust, _ = _control(q, omega, pos, vel, p)
        self.assertTrue(np.all(np.abs(torque) <= p.max_torque_n_m + 1e-12))
        self.assertGreaterEqual(thrust, 0.0)
        self.assertLessEqual(thrust, p.max_thrust_n + 1e-12)

    def test_peak_thrust_never_exceeds_max(self):
        p = nominal_params()
        log = simulate(p, 2.0, math.radians(60))["log"]
        self.assertLessEqual(float(np.max(log["thrust"])), p.max_thrust_n + 1e-9)


if __name__ == "__main__":
    unittest.main()
