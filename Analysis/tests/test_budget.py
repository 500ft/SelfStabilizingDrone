import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.budget import rollup, roundup_to_5g


class BudgetTests(unittest.TestCase):
    def test_roundup_to_5g(self):
        self.assertEqual(roundup_to_5g(176.0), 180.0)
        self.assertEqual(roundup_to_5g(180.0), 180.0)

    def test_rollup_does_not_add_margin_component(self):
        rows = [
            {"best_g": "10", "nominal_g": "12", "worst_g": "14"},
            {"best_g": "20", "nominal_g": "22", "worst_g": "24"},
        ]
        result = rollup(rows)
        self.assertEqual(result["worst_g"], 38.0)
        self.assertEqual(result["proposed_frozen_max_g"], 45.0)
        self.assertEqual(result["nominal_margin_g"], 11.0)


if __name__ == "__main__":
    unittest.main()
