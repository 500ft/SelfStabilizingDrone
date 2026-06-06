import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.classifier_stats import required_zero_event_trials, zero_event_upper_bound


class ClassifierStatsTests(unittest.TestCase):
    def test_three_hundred_trials_is_about_one_percent(self):
        self.assertLess(zero_event_upper_bound(300), 0.01)
        self.assertGreater(zero_event_upper_bound(300), 0.009)

    def test_one_thousand_trials_is_about_point_three_percent(self):
        self.assertLess(zero_event_upper_bound(1000), 0.003)
        self.assertGreater(zero_event_upper_bound(1000), 0.0029)

    def test_required_trials(self):
        self.assertEqual(required_zero_event_trials(0.01), 299)
        self.assertEqual(required_zero_event_trials(0.003), 998)


if __name__ == "__main__":
    unittest.main()
