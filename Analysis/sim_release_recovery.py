#!/usr/bin/env python3
"""Closed-loop 6-DoF release-to-stabilization simulation (Lane A deliverable).

Unlike ``recovery.py`` — which is a conservative *algebraic* altitude-loss envelope — this
module is an actual time-domain rigid-body flight simulation: full quaternion attitude
dynamics (reusing the ``rigid_body`` kernel's conventions) plus translational dynamics with
attitude-coupled thrust, driven by a saturated stabilization controller. It demonstrates the
guarded micro-UAV being released with an initial tumble + tilt, detecting the release after a
sensing/actuation latency, arresting the tumble, righting itself, and recovering to hover —
the maneuver the whole project is about.

Frames: world z is up; body z is the thrust axis. Quaternion ``q = (w, x, y, z)`` maps body→world.
All actuation respects the locked-BOM limits (max control torque, max collective thrust).
Parameters are taken from ``recovery.py``'s characterized cases so the two analyses agree.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, cos, sin, sqrt

import numpy as np

G = 9.81
RHO_AIR = 1.225


@dataclass(frozen=True)
class DroneParams:
    """Locked-BOM physical + actuation limits (see recovery.RecoveryCase)."""

    mass_kg: float
    inertia_lateral_kg_m2: float           # roll/pitch (the recovery-relevant axes)
    inertia_yaw_factor: float = 1.6        # ASSUMED Izz / Ixx for a small quad
    max_torque_n_m: float = 0.004          # per-axis control-torque saturation
    max_thrust_n: float = 4.2              # collective-thrust saturation
    drag_coefficient: float = 1.0
    projected_area_m2: float = 0.012
    detection_latency_s: float = 0.05
    motor_start_latency_s: float = 0.06
    gyro_limit_rad_s: float = 2000.0 * np.pi / 180.0
    available_height_m: float = 3.0

    @property
    def inertia(self) -> np.ndarray:
        i = self.inertia_lateral_kg_m2
        return np.array([i, i, i * self.inertia_yaw_factor])


# control gains (tuned so the torque-limited arrest saturates, then eases — see __main__)
KP_ATT, KD_ATT = 0.012, 0.0026
KP_ALT, KD_ALT = 2.2, 2.2


def quat_to_rotmat(q: np.ndarray) -> np.ndarray:
    w, x, y, z = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
    ])


def quat_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array([
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    ])


def axis_angle_quat(axis: np.ndarray, angle: float) -> np.ndarray:
    axis = np.asarray(axis, float)
    n = np.linalg.norm(axis)
    if n == 0:
        return np.array([1.0, 0.0, 0.0, 0.0])
    axis = axis / n
    return np.array([cos(angle / 2), *(axis * sin(angle / 2))])


def _control(q, omega, pos, vel, p: DroneParams):
    """Saturated attitude + altitude controller. Returns (torque_body[3], thrust_collective)."""
    R = quat_to_rotmat(q)
    body_up_world = R[:, 2]
    tilt = acos(np.clip(body_up_world[2], -1.0, 1.0))
    # attitude: drive body-up toward world-up; correcting rotation vector in the body frame
    e_world = np.cross(body_up_world, np.array([0.0, 0.0, 1.0]))
    e_body = R.T @ e_world
    torque = KP_ATT * e_body - KD_ATT * omega
    torque = np.clip(torque, -p.max_torque_n_m, p.max_torque_n_m)
    # altitude: tilt-compensated hold. Command the vertical force (gravity + PD recovery), then
    # divide by cos(tilt) so the body-up thrust still delivers it while righting; cut once past
    # ~78 deg (cos<0.2), where thrust can no longer help vertically and would only fight the
    # attitude loop. This is the standard release-recovery priority: limit the fall *while*
    # righting, instead of free-falling until upright.
    cos_tilt = R[2, 2]
    if cos_tilt > 0.2:
        desired_fz = p.mass_kg * G - KP_ALT * pos[2] - KD_ALT * vel[2]
        thrust = float(np.clip(desired_fz / cos_tilt, 0.0, p.max_thrust_n))
    else:
        thrust = 0.0
    return torque, thrust, tilt


def simulate(p: DroneParams, initial_rate_rad_s: float, initial_tilt_rad: float,
             *, tumble_axis=(1.0, 1.0, 0.0), tilt_axis=(0.0, 1.0, 0.0),
             dt: float = 5e-4, t_max: float = 6.0) -> dict:
    """Release the drone with an initial tumble + tilt and run closed-loop recovery.

    Motors are off for ``detection_latency + motor_start_latency`` (passive tumble + free
    fall), then the controller engages. Returns time-series arrays + recovery metrics.
    """
    q = axis_angle_quat(np.asarray(tilt_axis, float), initial_tilt_rad)
    omega = initial_rate_rad_s * (np.asarray(tumble_axis, float)
                                  / np.linalg.norm(tumble_axis))
    pos = np.zeros(3)
    vel = np.zeros(3)
    passive_time = p.detection_latency_s + p.motor_start_latency_s
    I = p.inertia

    T = int(t_max / dt)
    log = {k: np.empty(T) for k in ("t", "tilt", "omega_mag", "z", "vz", "thrust")}
    recovered_at = None
    settled_steps = 0

    for k in range(T):
        t = k * dt
        R = quat_to_rotmat(q)
        tilt = acos(np.clip(R[2, 2], -1.0, 1.0))
        motors_on = t >= passive_time
        if motors_on:
            torque, thrust, _ = _control(q, omega, pos, vel, p)
        else:
            torque, thrust = np.zeros(3), 0.0

        # translational dynamics (world frame): thrust along body-up, gravity, quadratic drag
        F = R @ np.array([0.0, 0.0, thrust])
        F[2] -= p.mass_kg * G
        speed = np.linalg.norm(vel)
        if speed > 0:
            F -= 0.5 * RHO_AIR * p.drag_coefficient * p.projected_area_m2 * speed * vel
        acc = F / p.mass_kg

        # attitude dynamics (Euler equations with gyroscopic coupling) + quaternion integration
        gyro = np.cross(omega, I * omega)
        alpha = (torque - gyro) / I

        log["t"][k] = t; log["tilt"][k] = tilt; log["omega_mag"][k] = np.linalg.norm(omega)
        log["z"][k] = pos[2]; log["vz"][k] = vel[2]; log["thrust"][k] = thrust

        vel = vel + acc * dt
        pos = pos + vel * dt
        omega = omega + alpha * dt
        q = q + 0.5 * quat_mul(q, np.array([0.0, *omega])) * dt
        q = q / np.linalg.norm(q)

        if pos[2] <= -p.available_height_m:        # hit the ground while recovering
            for key in log:
                log[key] = log[key][:k + 1]
            return _result(p, log, success=False, crashed=True,
                           recovery_time=None, initial_rate_rad_s=initial_rate_rad_s)

        # stabilized = upright, low rate, near-zero vertical speed, after motors engaged
        if motors_on and tilt < np.radians(5) and np.linalg.norm(omega) < 0.3 and abs(vel[2]) < 0.2:
            settled_steps += 1
            if settled_steps * dt >= 0.25 and recovered_at is None:   # held for 0.25 s
                recovered_at = t - passive_time
        else:
            settled_steps = 0

    for key in log:
        log[key] = log[key][:T]
    return _result(p, log, success=recovered_at is not None, crashed=False,
                   recovery_time=recovered_at, initial_rate_rad_s=initial_rate_rad_s)


def _result(p, log, *, success, crashed, recovery_time, initial_rate_rad_s):
    max_descent = float(-np.min(log["z"])) if log["z"].size else float("nan")
    return {
        "initial_rate_rad_s": initial_rate_rad_s,
        "success": bool(success),
        "crashed": bool(crashed),
        "recovery_time_s": recovery_time,
        "max_descent_m": max_descent,
        "available_height_m": p.available_height_m,
        "final_tilt_deg": float(np.degrees(log["tilt"][-1])) if log["tilt"].size else float("nan"),
        "peak_thrust_n": float(np.max(log["thrust"])) if log["thrust"].size else 0.0,
        "log": log,
    }


def max_recoverable_rate(p: DroneParams, initial_tilt_rad: float,
                         hi: float = 40.0, step: float = 0.5) -> float:
    """Largest initial tumble rate that still recovers, scanning up to the first failure.

    Scanning to the *first* failure (rather than bisecting) defines the usable envelope edge
    robustly even if recovery is not perfectly monotonic in rate near the boundary.
    """
    last_ok = 0.0
    rate = 0.0
    while rate <= hi:
        if simulate(p, rate, initial_tilt_rad)["success"]:
            last_ok = rate
            rate += step
        else:
            break
    return last_ok


# locked-BOM cases, mirroring recovery.default_cases() so the two analyses agree
def nominal_params() -> DroneParams:
    return DroneParams(mass_kg=0.12976, inertia_lateral_kg_m2=0.00035,
                       max_torque_n_m=0.0040, max_thrust_n=4.2,
                       drag_coefficient=1.0, projected_area_m2=0.012,
                       detection_latency_s=0.05, motor_start_latency_s=0.06)


def best_params() -> DroneParams:
    return DroneParams(mass_kg=0.11796, inertia_lateral_kg_m2=0.00020,
                       max_torque_n_m=0.0060, max_thrust_n=5.0,
                       drag_coefficient=1.3, projected_area_m2=0.016,
                       detection_latency_s=0.02, motor_start_latency_s=0.03)


def worst_params() -> DroneParams:
    return DroneParams(mass_kg=0.155, inertia_lateral_kg_m2=0.00055,
                       max_torque_n_m=0.0025, max_thrust_n=3.5,
                       drag_coefficient=0.8, projected_area_m2=0.008,
                       detection_latency_s=0.10, motor_start_latency_s=0.12)


if __name__ == "__main__":
    for name, p in [("nominal", nominal_params()), ("worst", worst_params())]:
        r = simulate(p, initial_rate_rad_s=5.0, initial_tilt_rad=np.radians(60))
        mr = max_recoverable_rate(p, np.radians(60))
        print(f"{name}: success={r['success']} recovery_time={r['recovery_time_s']} "
              f"max_descent={r['max_descent_m']:.2f}/{p.available_height_m} m "
              f"peak_thrust={r['peak_thrust_n']:.2f}/{p.max_thrust_n} N "
              f"max_recoverable_rate={mr:.1f} rad/s ({np.degrees(mr):.0f} deg/s)")
