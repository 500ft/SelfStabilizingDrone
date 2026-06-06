#!/usr/bin/env python3
"""Conservative first-order release-recovery envelope model.

This is not a 3-D rigid-body flight controller simulation. It estimates
altitude loss using bounded single-axis attitude dynamics and vertical motion.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import pi, sqrt

G = 9.81
RHO_AIR = 1.225


@dataclass(frozen=True)
class RecoveryCase:
    name: str
    mass_kg: float
    inertia_kg_m2: float
    initial_rate_rad_s: float
    initial_tilt_rad: float
    detection_latency_s: float
    motor_start_latency_s: float
    control_torque_n_m: float
    total_thrust_n: float
    battery_voltage_v: float
    reference_voltage_v: float
    drag_coefficient: float
    projected_area_m2: float
    gyro_limit_rad_s: float
    gyro_margin_fraction: float = 0.8
    available_height_m: float = 3.0


def arrest_time(inertia: float, angular_rate: float, torque: float) -> float:
    if torque <= 0:
        return float("inf")
    return inertia * abs(angular_rate) / torque


def rotate_upright_time(inertia: float, angle: float, torque: float) -> float:
    """Bang-bang rest-to-rest rotation time with equal accel/decel phases."""
    if torque <= 0:
        return float("inf")
    alpha = torque / inertia
    return 2.0 * sqrt(abs(angle) / alpha)


def vertical_acceleration(
    velocity_down_m_s: float,
    mass_kg: float,
    thrust_up_n: float,
    drag_coefficient: float,
    area_m2: float,
) -> float:
    """Return downward-positive acceleration."""
    drag_up_n = 0.5 * RHO_AIR * drag_coefficient * area_m2 * velocity_down_m_s**2
    return G - (thrust_up_n + drag_up_n) / mass_kg


def integrate_vertical(
    duration_s: float,
    mass_kg: float,
    initial_velocity_down_m_s: float = 0.0,
    thrust_up_n: float = 0.0,
    drag_coefficient: float = 0.0,
    area_m2: float = 0.0,
    stop_at_zero_velocity: bool = False,
    dt: float = 0.0005,
) -> tuple[float, float, float]:
    """Return elapsed time, downward distance, and final downward velocity."""
    elapsed = 0.0
    distance = 0.0
    velocity = initial_velocity_down_m_s
    while elapsed < duration_s:
        step = min(dt, duration_s - elapsed)
        acceleration = vertical_acceleration(
            velocity, mass_kg, thrust_up_n, drag_coefficient, area_m2
        )
        next_velocity = velocity + acceleration * step
        distance += max(0.0, 0.5 * (velocity + next_velocity) * step)
        velocity = next_velocity
        elapsed += step
        if stop_at_zero_velocity and velocity <= 0:
            return elapsed, distance, velocity
    return elapsed, distance, velocity


def evaluate_case(case: RecoveryCase) -> dict[str, float | bool | str]:
    verified_gyro_limit = case.gyro_limit_rad_s * case.gyro_margin_fraction
    gyro_ok = abs(case.initial_rate_rad_s) < verified_gyro_limit
    voltage_scale = max(0.0, case.battery_voltage_v / case.reference_voltage_v)
    effective_torque = case.control_torque_n_m * voltage_scale
    effective_thrust = case.total_thrust_n * voltage_scale
    attitude_arrest_s = arrest_time(
        case.inertia_kg_m2, case.initial_rate_rad_s, effective_torque
    )
    upright_rotation_s = rotate_upright_time(
        case.inertia_kg_m2, case.initial_tilt_rad, effective_torque
    )
    passive_time_s = (
        case.detection_latency_s
        + case.motor_start_latency_s
        + attitude_arrest_s
        + upright_rotation_s
    )
    _, passive_loss_m, velocity_down_m_s = integrate_vertical(
        passive_time_s,
        case.mass_kg,
        drag_coefficient=case.drag_coefficient,
        area_m2=case.projected_area_m2,
    )
    net_up_accel = effective_thrust / case.mass_kg - G
    thrust_ok = net_up_accel > 0
    if thrust_ok:
        max_arrest_duration = velocity_down_m_s / max(net_up_accel, 1e-9) * 3.0
        vertical_arrest_s, arrest_loss_m, _ = integrate_vertical(
            max_arrest_duration,
            case.mass_kg,
            initial_velocity_down_m_s=velocity_down_m_s,
            thrust_up_n=effective_thrust,
            drag_coefficient=case.drag_coefficient,
            area_m2=case.projected_area_m2,
            stop_at_zero_velocity=True,
        )
    else:
        vertical_arrest_s = float("inf")
        arrest_loss_m = float("inf")
    minimum_height_m = passive_loss_m + arrest_loss_m
    success = gyro_ok and thrust_ok and minimum_height_m <= case.available_height_m
    return {
        "name": case.name,
        "gyro_ok": gyro_ok,
        "thrust_ok": thrust_ok,
        "effective_control_torque_n_m": effective_torque,
        "effective_total_thrust_n": effective_thrust,
        "attitude_arrest_s": attitude_arrest_s,
        "upright_rotation_s": upright_rotation_s,
        "passive_time_s": passive_time_s,
        "vertical_arrest_s": vertical_arrest_s,
        "minimum_height_m": minimum_height_m,
        "available_height_m": case.available_height_m,
        "testable_now": success,
    }


def default_cases() -> list[RecoveryCase]:
    gyro_limit = 2000.0 * pi / 180.0
    return [
        RecoveryCase(
            "best",
            0.1065,
            0.00020,
            2.0,
            pi / 6,
            0.020,
            0.030,
            0.0060,
            5.0,
            8.4,
            8.4,
            1.3,
            0.016,
            gyro_limit,
        ),
        RecoveryCase(
            "nominal",
            0.14075,
            0.00035,
            5.0,
            pi / 3,
            0.050,
            0.060,
            0.0040,
            4.2,
            7.6,
            8.4,
            1.0,
            0.012,
            gyro_limit,
        ),
        RecoveryCase(
            "worst",
            0.180,
            0.00055,
            8.0,
            pi / 2,
            0.100,
            0.120,
            0.0025,
            3.5,
            7.0,
            8.4,
            0.8,
            0.008,
            gyro_limit,
        ),
    ]


def no_drag(case: RecoveryCase) -> RecoveryCase:
    return replace(case, name=f"{case.name}_no_drag", drag_coefficient=0.0, projected_area_m2=0.0)


def sensitivity(case: RecoveryCase, fraction: float = 0.05) -> list[tuple[str, float]]:
    baseline = float(evaluate_case(case)["minimum_height_m"])
    fields = [
        "mass_kg",
        "inertia_kg_m2",
        "initial_rate_rad_s",
        "detection_latency_s",
        "motor_start_latency_s",
        "control_torque_n_m",
        "total_thrust_n",
        "battery_voltage_v",
        "drag_coefficient",
        "projected_area_m2",
    ]
    results: list[tuple[str, float]] = []
    for field in fields:
        original = getattr(case, field)
        varied = replace(case, **{field: original * (1.0 + fraction)})
        changed = float(evaluate_case(varied)["minimum_height_m"])
        results.append((field, (changed - baseline) / (original * fraction)))
    return sorted(results, key=lambda item: abs(item[1]), reverse=True)


def main() -> None:
    print("Preliminary recovery envelope; replace placeholders with CAD and bench data")
    for case in default_cases():
        print(evaluate_case(case))
    print("Conservative no-drag nominal:", evaluate_case(no_drag(default_cases()[1])))
    print("Nominal sensitivity ranking:", sensitivity(default_cases()[1]))


if __name__ == "__main__":
    main()
