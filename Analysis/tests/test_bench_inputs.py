"""Consistency checks for planning inputs, not geometry or hardware validation."""
import csv
import math
from pathlib import Path
import unittest

from Analysis.measured_authority_gate import COLLECTIVE_GRID, MIN_AUTHORITY_N_M

ROOT = Path(__file__).resolve().parents[2]


class BenchInputTests(unittest.TestCase):
    def test_register_states_units_and_sources(self):
        with (ROOT / 'cad/bench/parameters.csv').open(newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        self.assertEqual(len(rows), len({row['parameter'] for row in rows}))
        for row in rows:
            with self.subTest(parameter=row['parameter']):
                self.assertNotIn(None, row)
                self.assertTrue(row['release_requirement'])
                self.assertIn(row['unit'], {'mm', 'm', 'N', 'V', '1', 'N*m'})
                self.assertIn(row['evidence_state'], {'pending', 'vendor_nominal', 'model_assumption', 'protocol'})
                if row['evidence_state'] == 'pending':
                    self.assertEqual(row['value'], '')
                else:
                    self.assertTrue(math.isfinite(float(row['value'])))
                    self.assertGreater(float(row['value']), 0)
                if not row['source'].startswith('https://'):
                    self.assertTrue((ROOT / row['source']).is_file(), row['source'])
        values = {row['parameter']: row for row in rows}
        self.assertEqual(tuple(float(values[f'collective_{i}']['value']) for i in range(1, 6)), COLLECTIVE_GRID)
        self.assertEqual(float(values['authority_threshold']['value']), MIN_AUTHORITY_N_M)
        self.assertEqual(values['authority_arm_model']['evidence_state'], 'model_assumption')
        self.assertEqual(values['authority_arm_measured']['evidence_state'], 'pending')
        self.assertEqual(values['stand_calibration_lever']['evidence_state'], 'pending')


if __name__ == '__main__':
    unittest.main()
