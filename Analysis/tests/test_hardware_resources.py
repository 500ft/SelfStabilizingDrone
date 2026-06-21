import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.hardware_resources import (
    load_interfaces,
    load_power_budget,
    power_margin_fraction,
    validate_interfaces,
    validate_power_budget,
)


class HardwareResourceTests(unittest.TestCase):
    def test_locked_interface_map_has_no_conflicts(self):
        errors = validate_interfaces(load_interfaces())
        self.assertEqual(errors, [])

    def test_stage_2_uart_reservations_exist(self):
        rows = load_interfaces()
        assignments = {row["function"]: row for row in rows}
        self.assertEqual(assignments["GPS"]["stage"], "STAGE_2_RESERVED")
        self.assertEqual(assignments["FPV/VTX control"]["stage"], "STAGE_2_RESERVED")

    def test_motor_timer_groups_use_one_protocol(self):
        rows = load_interfaces()
        motors = [row for row in rows if row["resource_type"] == "motor_output"]
        by_group = {}
        for motor in motors:
            by_group.setdefault(motor["resource_group"], set()).add(motor["protocol"])
        self.assertEqual(by_group, {"PWM_GROUP_1": {"DSHOT"}, "PWM_GROUP_2": {"DSHOT"}})

    def test_conservative_5v_power_budget_has_25_percent_margin(self):
        rows = load_power_budget()
        self.assertEqual(validate_power_budget(rows), [])
        self.assertGreaterEqual(power_margin_fraction(rows), 0.25)


if __name__ == "__main__":
    unittest.main()
