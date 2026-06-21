import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Analysis.gates import (
    RESOURCE_MAP,
    allowable_mass,
    battery_decision,
    esc_decision,
    nicla_decision,
    propulsion_decision,
    thrust_required_per_motor,
)


class PropulsionGateTests(unittest.TestCase):
    def test_full_reserve_boundary_is_112_5(self):
        self.assertAlmostEqual(thrust_required_per_motor(225.0), 112.5)

    def test_nominal_mass_floor_is_65_1(self):
        self.assertAlmostEqual(thrust_required_per_motor(130.2), 65.1)

    def test_mass_lever_two_grams_per_gram(self):
        self.assertAlmostEqual(allowable_mass(105.0), 210.0)

    def test_decision_tiers(self):
        self.assertEqual(propulsion_decision(120.0, 130.2), "PASS_FULL_RESERVE")
        self.assertEqual(propulsion_decision(105.0, 130.2), "PASS_200G_CEILING")
        self.assertEqual(propulsion_decision(80.0, 150.0), "CONDITIONAL_REDUCED_MASS")
        self.assertEqual(propulsion_decision(60.0, 130.2), "BLOCKER")


class CurrentGateTests(unittest.TestCase):
    def test_esc_tiers(self):
        self.assertEqual(esc_decision(9.2), "PASS")
        self.assertEqual(esc_decision(10.4), "PASS")
        self.assertEqual(esc_decision(12.0), "CONDITIONAL_THERMAL")
        self.assertEqual(esc_decision(15.0), "CONDITIONAL_TRANSIENT_ONLY")
        self.assertEqual(esc_decision(21.0), "FAIL")

    def test_battery_tiers(self):
        self.assertEqual(battery_decision(36.8), "PASS")
        self.assertEqual(battery_decision(44.0), "PASS")
        self.assertEqual(battery_decision(50.0), "CONDITIONAL_SAG_THERMAL")
        self.assertEqual(battery_decision(60.0), "FAIL")


class NiclaGateTests(unittest.TestCase):
    def test_latency_tiers(self):
        self.assertEqual(nicla_decision(40.0), "RECOVERY_CANDIDATE")
        self.assertEqual(nicla_decision(80.0), "LOG_ONLY")
        self.assertEqual(nicla_decision(120.0), "INELIGIBLE")


class ResourceMapTests(unittest.TestCase):
    def test_serial_assignments_unique(self):
        serials = [a.serial for a in RESOURCE_MAP if a.serial]
        self.assertEqual(len(serials), len(set(serials)), "duplicate SERIAL assignment")

    def test_pads_unique(self):
        pads = [a.pad for a in RESOURCE_MAP]
        self.assertEqual(len(pads), len(set(pads)), "duplicate physical pad assignment")

    def test_motors_present_on_four_outputs(self):
        motors = [a for a in RESOURCE_MAP if a.function.startswith("Motor")]
        self.assertEqual(len(motors), 4)


if __name__ == "__main__":
    unittest.main()
