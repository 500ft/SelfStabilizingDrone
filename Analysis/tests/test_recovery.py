import math
import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.recovery import (
    RecoveryCase,
    arrest_time,
    evaluate_case,
    integrate_vertical,
)


class RecoveryTests(unittest.TestCase):
    def test_free_fall(self):
        elapsed, distance, velocity = integrate_vertical(0.5, 0.17, dt=0.0001)
        self.assertAlmostEqual(elapsed, 0.5, places=6)
        self.assertAlmostEqual(distance, 0.5 * 9.81 * 0.5**2, places=3)
        self.assertAlmostEqual(velocity, 9.81 * 0.5, places=3)

    def test_single_axis_spin_down(self):
        inertia = 0.0004
        rate = 6.0
        torque = 0.004
        self.assertAlmostEqual(arrest_time(inertia, rate, torque), inertia * rate / torque)

    def test_gyro_saturation_is_rejected(self):
        case = RecoveryCase(
            "saturation",
            0.17,
            0.0004,
            30.0,
            math.pi / 4,
            0.05,
            0.05,
            0.004,
            4.0,
            8.4,
            8.4,
            0.8,
            0.008,
            20.0,
        )
        self.assertFalse(evaluate_case(case)["gyro_ok"])

    def test_more_torque_reduces_minimum_height(self):
        common = dict(
            name="case",
            mass_kg=0.17,
            inertia_kg_m2=0.0004,
            initial_rate_rad_s=5.0,
            initial_tilt_rad=math.pi / 2,
            detection_latency_s=0.05,
            motor_start_latency_s=0.05,
            total_thrust_n=4.0,
            battery_voltage_v=8.4,
            reference_voltage_v=8.4,
            drag_coefficient=0.0,
            projected_area_m2=0.0,
            gyro_limit_rad_s=35.0,
        )
        low = RecoveryCase(control_torque_n_m=0.002, **common)
        high = RecoveryCase(control_torque_n_m=0.006, **common)
        self.assertGreater(
            evaluate_case(low)["minimum_height_m"],
            evaluate_case(high)["minimum_height_m"],
        )


if __name__ == "__main__":
    unittest.main()
