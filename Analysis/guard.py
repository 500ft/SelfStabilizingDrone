#!/usr/bin/env python3
"""Low-energy linear-elastic guard functional check."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class GuardCase:
    name: str
    impact_energy_j: float
    stiffness_n_m: float
    stress_per_force_pa_n: float
    clearance_m: float
    elastic_allowable_pa: float


def evaluate_guard(case: GuardCase) -> dict[str, float | bool | str]:
    if case.stiffness_n_m <= 0:
        raise ValueError("stiffness must be positive")
    delta = sqrt(2.0 * case.impact_energy_j / case.stiffness_n_m)
    equivalent_force = sqrt(2.0 * case.impact_energy_j * case.stiffness_n_m)
    stress = case.stress_per_force_pa_n * equivalent_force
    clearance_sf = case.clearance_m / delta
    stress_sf = case.elastic_allowable_pa / stress
    return {
        "name": case.name,
        "deflection_m": delta,
        "equivalent_force_n": equivalent_force,
        "stress_pa": stress,
        "clearance_safety_factor": clearance_sf,
        "elastic_stress_safety_factor": stress_sf,
        "functional_pass": clearance_sf >= 2.0 and stress_sf >= 3.0,
    }


def default_cases() -> list[GuardCase]:
    return [
        GuardCase("best", 0.02, 1400.0, 150000.0, 0.003, 20e6),
        GuardCase("nominal", 0.05, 900.0, 225000.0, 0.0025, 16e6),
        GuardCase("worst", 0.10, 500.0, 300000.0, 0.002, 12e6),
    ]


def main() -> None:
    print("Functional elastic guard check; this is not a fracture model")
    for case in default_cases():
        print(evaluate_guard(case))


if __name__ == "__main__":
    main()
