import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.guard import GuardCase, evaluate_guard


class GuardTests(unittest.TestCase):
    def test_energy_relations(self):
        case = GuardCase("test", 0.05, 1000.0, 200000.0, 0.02, 100e6)
        result = evaluate_guard(case)
        recovered_energy = 0.5 * case.stiffness_n_m * result["deflection_m"] ** 2
        self.assertAlmostEqual(recovered_energy, case.impact_energy_j)
        self.assertAlmostEqual(
            result["equivalent_force_n"],
            case.stiffness_n_m * result["deflection_m"],
        )

    def test_nonpositive_stiffness_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_guard(GuardCase("bad", 0.05, 0.0, 1.0, 0.002, 1.0))


if __name__ == "__main__":
    unittest.main()
