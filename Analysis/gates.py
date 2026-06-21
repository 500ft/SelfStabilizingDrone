#!/usr/bin/env python3
"""Pre-registered Stage 1 verification gates.

These thresholds are locked BEFORE bench measurement so that results cannot be
rationalized after the fact. Decisions reference these functions; do not inline
new thresholds elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass

try:  # package import in tests / module execution
    from Analysis.hardware_resources import load_interfaces
except ModuleNotFoundError:  # direct `python3 Analysis/gates.py`
    from hardware_resources import load_interfaces

# --- Requirements anchors -------------------------------------------------
TW_MIN = 2.0  # REQ-PROP-001 static thrust-to-weight
ABORT_CEILING_G = 225.0  # REQ-MASS-002
PLANNING_CEILING_G = 200.0  # REQ-MASS-001
N_MOTORS = 4

# Propulsion bench is acceptance-gated at the worst-case usable cell voltage.
ACCEPTANCE_VOLTAGE_V = 7.0  # 3.5 V/cell under load; 8.4 V / 7.6 V are references only

# Margin policy: keep >= 1.25x against the rated continuous limit.
MARGIN_FACTOR = 1.25
ESC_CONT_A = 13.0
ESC_BURST_A = 20.0
BATTERY_CONT_A = 55.0

# Nicla end-to-end (sensor-event -> MAVLink) p95 latency budget, milliseconds.
NICLA_RECOVERY_MS = 50.0
NICLA_LOG_ONLY_MS = 100.0


def thrust_required_per_motor(vehicle_mass_g: float) -> float:
    """Minimum per-motor static thrust (gf) to meet T/W >= 2.0 at a given mass."""
    return TW_MIN * vehicle_mass_g / N_MOTORS


def allowable_mass(per_motor_thrust_gf: float) -> float:
    """Maximum frozen mass (g) supported at T/W >= 2.0 by a measured per-motor thrust."""
    return N_MOTORS * per_motor_thrust_gf / TW_MIN


def propulsion_decision(measured_per_motor_gf: float, frozen_mass_g: float) -> str:
    """Pre-registered propulsion gate (use the uncertainty-adjusted lower bound)."""
    if measured_per_motor_gf >= thrust_required_per_motor(ABORT_CEILING_G):
        return "PASS_FULL_RESERVE"
    if measured_per_motor_gf >= thrust_required_per_motor(PLANNING_CEILING_G):
        return "PASS_200G_CEILING"
    if frozen_mass_g <= allowable_mass(measured_per_motor_gf):
        return "CONDITIONAL_REDUCED_MASS"
    return "BLOCKER"


def esc_decision(peak_per_motor_a: float) -> str:
    """Pre-registered ESC gate (use measured peak plus uncertainty)."""
    if peak_per_motor_a <= ESC_CONT_A / MARGIN_FACTOR:
        return "PASS"
    if peak_per_motor_a <= ESC_CONT_A:
        return "CONDITIONAL_THERMAL"
    if peak_per_motor_a <= ESC_BURST_A:
        return "CONDITIONAL_TRANSIENT_ONLY"
    return "FAIL"


def battery_decision(pack_peak_a: float) -> str:
    """Pre-registered battery current gate (use measured pack peak plus uncertainty)."""
    if pack_peak_a <= BATTERY_CONT_A / MARGIN_FACTOR:
        return "PASS"
    if pack_peak_a <= BATTERY_CONT_A:
        return "CONDITIONAL_SAG_THERMAL"
    return "FAIL"


def nicla_decision(p95_latency_ms: float) -> str:
    """Pre-registered vision latency gate (p95 sensor-event -> MAVLink)."""
    if p95_latency_ms <= NICLA_RECOVERY_MS:
        return "RECOVERY_CANDIDATE"
    if p95_latency_ms <= NICLA_LOG_ONLY_MS:
        return "LOG_ONLY"
    return "INELIGIBLE"


# --- Provisional ArduPilot resource allocation (verify vs board revision) --
@dataclass(frozen=True)
class Allocation:
    function: str
    serial: str | None
    pad: str
    timer_group: str | None
    stage: str


RESOURCE_MAP: tuple[Allocation, ...] = tuple(
    Allocation(
        row["function"],
        row["serial"] or None,
        row["pad"],
        row["resource_group"] or None,
        row["stage"],
    )
    for row in load_interfaces()
)


if __name__ == "__main__":
    print(f"Propulsion full-reserve floor @225g: {thrust_required_per_motor(ABORT_CEILING_G)} gf/motor")
    print(f"Propulsion floor @129.8g nominal:   {thrust_required_per_motor(129.8):.1f} gf/motor")
    print(f"ESC pass ceiling:  {ESC_CONT_A / MARGIN_FACTOR:.1f} A/motor")
    print(f"Battery pass ceiling: {BATTERY_CONT_A / MARGIN_FACTOR:.1f} A pack")
