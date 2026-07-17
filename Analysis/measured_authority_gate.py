#!/usr/bin/env python3
"""Evaluate the preregistered EST-REC-007 differential-authority gate."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


ACCEPTANCE_VOLTAGE_V = 7.0
COLLECTIVE_GRID = (0.25, 0.375, 0.50, 0.625, 0.75)
MIN_REPEATS_PER_POINT = 6
LOWER_QUANTILE = 0.05
MIN_AUTHORITY_N_M = 0.020


@dataclass(frozen=True)
class CollectiveResult:
    collective_fraction: float
    samples: int
    fifth_percentile_tau_n_m: float


@dataclass(frozen=True)
class AuthorityVerdict:
    classification: str
    threshold_n_m: float
    conservative_minimum_n_m: Optional[float]
    voltage_v: float
    points: List[CollectiveResult]
    reasons: List[str]


def mixer_torque_authority(
    total_max_thrust_n: float,
    arm_m: float,
    collective_fraction: float,
) -> float:
    """Four-motor X-frame roll/pitch authority at a collective fraction."""

    if total_max_thrust_n <= 0 or arm_m <= 0:
        raise ValueError("thrust and arm must be positive")
    if not 0.0 <= collective_fraction <= 1.0:
        raise ValueError("collective_fraction must lie in [0, 1]")
    per_motor_max = total_max_thrust_n / 4.0
    per_motor_collective = collective_fraction * per_motor_max
    differential_headroom = min(
        per_motor_collective,
        per_motor_max - per_motor_collective,
    )
    return 2.0 * math.sqrt(2.0) * arm_m * differential_headroom


def minimum_authority_over_band(total_max_thrust_n: float, arm_m: float) -> float:
    """Minimum authority on the closed 25–75% collective interval."""

    return min(
        mixer_torque_authority(total_max_thrust_n, arm_m, fraction)
        for fraction in (COLLECTIVE_GRID[0], COLLECTIVE_GRID[-1])
    )


def _empirical_lower_quantile(values: List[float], quantile: float) -> float:
    if not values:
        raise ValueError("at least one sample is required")
    ordered = sorted(values)
    index = max(0, int(math.ceil(quantile * len(ordered))) - 1)
    return ordered[index]


def evaluate_rows(rows: Iterable[Dict[str, object]]) -> AuthorityVerdict:
    """Evaluate direct tau_rp measurements at 7.0 V and the frozen grid."""

    by_collective: Dict[float, List[float]] = {point: [] for point in COLLECTIVE_GRID}
    reasons = []
    for row in rows:
        try:
            voltage = float(row["voltage_v"])
            collective = float(row["collective_fraction"])
            torque = float(row["tau_rp_n_m"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("rows require voltage_v, collective_fraction, tau_rp_n_m") from exc
        if abs(voltage - ACCEPTANCE_VOLTAGE_V) > 0.05:
            continue
        match = min(COLLECTIVE_GRID, key=lambda point: abs(point - collective))
        if abs(match - collective) <= 0.002:
            by_collective[match].append(torque)

    point_results = []
    for point in COLLECTIVE_GRID:
        values = by_collective[point]
        if len(values) < MIN_REPEATS_PER_POINT:
            reasons.append(
                "collective {:.3f} has {} samples; {} required".format(
                    point, len(values), MIN_REPEATS_PER_POINT
                )
            )
            continue
        point_results.append(
            CollectiveResult(
                collective_fraction=point,
                samples=len(values),
                fifth_percentile_tau_n_m=_empirical_lower_quantile(values, LOWER_QUANTILE),
            )
        )

    if reasons:
        return AuthorityVerdict(
            classification="INCONCLUSIVE",
            threshold_n_m=MIN_AUTHORITY_N_M,
            conservative_minimum_n_m=None,
            voltage_v=ACCEPTANCE_VOLTAGE_V,
            points=point_results,
            reasons=reasons,
        )

    conservative = min(point.fifth_percentile_tau_n_m for point in point_results)
    if conservative >= MIN_AUTHORITY_N_M:
        classification = "PASS"
        reasons.append("fifth-percentile authority clears 0.020 N m at every grid point")
    else:
        classification = "FAIL"
        reasons.append("fifth-percentile authority falls below 0.020 N m in the band")
    return AuthorityVerdict(
        classification=classification,
        threshold_n_m=MIN_AUTHORITY_N_M,
        conservative_minimum_n_m=conservative,
        voltage_v=ACCEPTANCE_VOLTAGE_V,
        points=point_results,
        reasons=reasons,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="CSV with voltage_v, collective_fraction, tau_rp_n_m")
    parser.add_argument("--output", type=Path, help="optional verdict JSON")
    args = parser.parse_args()
    with args.csv.open(newline="", encoding="utf-8") as handle:
        verdict = evaluate_rows(csv.DictReader(handle))
    payload = json.dumps(asdict(verdict), indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
