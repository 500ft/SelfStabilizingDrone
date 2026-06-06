import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.rigid_body import quaternion_norm, step


class RigidBodyTests(unittest.TestCase):
    def test_zero_torque_spherical_inertia_preserves_rate(self):
        q, omega = step(
            (1.0, 0.0, 0.0, 0.0),
            (2.0, -1.0, 0.5),
            (0.0, 0.0, 0.0),
            (0.0004, 0.0004, 0.0004),
            0.001,
        )
        self.assertEqual(omega, (2.0, -1.0, 0.5))
        self.assertAlmostEqual(quaternion_norm(q), 1.0, places=12)

    def test_symmetric_torque_produces_symmetric_response(self):
        _, omega = step(
            (1.0, 0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (0.002, 0.002, 0.0),
            (0.0004, 0.0004, 0.0008),
            0.01,
        )
        self.assertAlmostEqual(omega[0], omega[1])
        self.assertEqual(omega[2], 0.0)

    def test_quaternion_stays_normalized_over_many_steps(self):
        q = (1.0, 0.0, 0.0, 0.0)
        omega = (5.0, 2.0, -1.0)
        for _ in range(10000):
            q, omega = step(
                q,
                omega,
                (0.0, 0.0, 0.0),
                (0.0004, 0.0004, 0.0004),
                0.0001,
            )
        self.assertAlmostEqual(quaternion_norm(q), 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
