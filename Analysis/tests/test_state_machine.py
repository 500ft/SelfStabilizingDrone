import json
import unittest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Controls" / "state_machine.json"
DOC = ROOT / "Controls" / "README.md"


class StateMachineTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_all_states_are_documented(self):
        documentation = DOC.read_text(encoding="utf-8")
        for state in self.data["states"]:
            self.assertIn(state, documentation)

    def test_recovery_active_has_failsafe_edge(self):
        matching = [
            transition
            for transition in self.data["transitions"]
            if transition["from"] == "RECOVERY_ACTIVE"
            and transition["to"] == "FAILSAFE"
        ]
        self.assertEqual(len(matching), 1)
        guards = matching[0]["guards"]
        for required in ("arrest timeout", "gyro saturation", "estimator invalid", "manual abort"):
            self.assertIn(required, guards)

    def test_transitions_reference_known_states(self):
        states = set(self.data["states"])
        for transition in self.data["transitions"]:
            self.assertIn(transition["from"], states)
            self.assertIn(transition["to"], states)


if __name__ == "__main__":
    unittest.main()
