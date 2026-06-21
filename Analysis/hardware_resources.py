#!/usr/bin/env python3
"""Validate the locked Kakute H7 Mini Stage 1 hardware-resource allocation."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERFACES = ROOT / "Engineering Data" / "hardware_interfaces.csv"
POWER_BUDGET = ROOT / "Engineering Data" / "power_budget.csv"
CONSERVATIVE_5V_CAPACITY_MA = 1500.0


def load_interfaces(path: Path = INTERFACES) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_power_budget(path: Path = POWER_BUDGET) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def power_margin_fraction(rows: list[dict[str, str]]) -> float:
    worst_load_ma = sum(float(row["worst_ma"]) for row in rows)
    return (CONSERVATIVE_5V_CAPACITY_MA - worst_load_ma) / CONSERVATIVE_5V_CAPACITY_MA


def validate_power_budget(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        if float(row["nominal_ma"]) < 0 or float(row["worst_ma"]) < 0:
            errors.append(f"{row['device']}: current must be non-negative")
        if float(row["worst_ma"]) < float(row["nominal_ma"]):
            errors.append(f"{row['device']}: worst current is below nominal")
    margin = power_margin_fraction(rows)
    if margin < 0.25:
        errors.append(f"5 V rail margin {margin:.1%} is below 25%")
    return errors


def validate_interfaces(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    required = {
        "function",
        "resource_type",
        "serial",
        "pad",
        "resource_group",
        "protocol",
        "stage",
        "pad_exposed",
        "evidence_state",
        "source_url",
    }
    for index, row in enumerate(rows, start=2):
        missing = required - set(row)
        if missing:
            errors.append(f"row {index}: missing columns {sorted(missing)}")
            continue
        if row["stage"] == "STAGE_1" and row["pad_exposed"] != "yes":
            errors.append(f"{row['function']}: Stage 1 pad is not confirmed exposed")
        if row["evidence_state"] == "BLOCKER":
            errors.append(f"{row['function']}: unresolved BLOCKER")

    for field in ("serial", "pad"):
        values = [row[field] for row in rows if row.get(field)]
        duplicates = sorted({value for value in values if values.count(value) > 1})
        if duplicates:
            errors.append(f"duplicate {field}: {', '.join(duplicates)}")

    motor_protocols: dict[str, set[str]] = {}
    for row in rows:
        if row.get("resource_type") == "motor_output":
            motor_protocols.setdefault(row["resource_group"], set()).add(row["protocol"])
    for group, protocols in sorted(motor_protocols.items()):
        if len(protocols) != 1:
            errors.append(f"{group}: incompatible motor protocols {sorted(protocols)}")
    return errors


def main() -> None:
    rows = load_interfaces()
    errors = validate_interfaces(rows)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    power_rows = load_power_budget()
    power_errors = validate_power_budget(power_rows)
    if power_errors:
        for error in power_errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print(f"PASS: {len(rows)} hardware interfaces; no resource conflicts")
    print(f"PASS: conservative 5 V rail margin {power_margin_fraction(power_rows):.1%}")


if __name__ == "__main__":
    main()
