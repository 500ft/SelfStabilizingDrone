# Preliminary Calculations

These calculations are the first sizing pass for the protected throwable micro-UAV. Replace assumptions with measured values as parts are selected.

## Mass and Thrust Requirements

The maximum mass is not frozen. Current planning rollup:

| Value | Result |
|---|---:|
| Sigma best | 117.96 g |
| Sigma nominal | 129.76 g |
| Sigma worst | 149.5 g |
| Proposed frozen maximum | 155.0 g |

Freeze rule:

```text
frozen maximum mass = roundup_to_5g(Sigma worst + 5 g)
nominal margin = frozen maximum mass - Sigma nominal
```

At the current proposed 155 g maximum:

```text
T_required_total = 2.0 * 155 g = 310 g
T_required_motor = 310 g / 4 = 77.5 g
```

This is only the static requirement. The recovery case may require greater thrust and torque.

Hover thrust per motor:

```text
T_hover_motor = mass / 4
```

| Mass | Hover Thrust Per Motor |
|---:|---:|
| 140 g | 35.0 g |
| 150 g | 37.5 g |
| 160 g | 40.0 g |
| 180 g | 45.0 g |
| 200 g | 50.0 g |

The selected motor/prop/battery combination should produce hover thrust well below maximum throttle.

## Locked Propulsion Gate

The catalog combination is EX1103 11000KV + Gemfan 2023-3 + GNB 2S 550 mAh.
Its performance is not settled: the 121.9 gf/motor and 9.2 A/motor point is a
vendor result and must be reproduced.

Planning interpretation:

- Static per-motor thrust must be at least one quarter of twice the frozen maximum mass.
- Recovery torque and angular acceleration may drive a higher requirement.
- ESC current rating should cover peak current with margin.
- Hover current must be estimated from thrust data, then measured on the built vehicle.

The bench sweep is performed at 8.4 V, 7.6 V, and **7.0 V at the ESC input under
load**. The uncertainty-adjusted 7.0 V value controls acceptance:

```text
T_required_per_motor = 2 * vehicle_mass / 4
M_allowable = 2 * measured_per_motor_thrust
```

At 225 g, the full-reserve threshold is 112.5 gf/motor. At the current 129.8 g
nominal mass, the threshold is 64.9 gf/motor. A shortfall against 225 g first
reduces the frozen mass; it does not automatically trigger a prop change.

## Battery and Flight Time

Estimated flight time:

```text
t_min = 60 * C_usable / I_avg
```

Where:

- `C_usable = nominal capacity * 0.8`
- `I_avg = average current during flight`

Example for a 2S 550 mAh pack:

```text
C_usable = 0.550 Ah * 0.8 = 0.440 Ah
```

If average hover current is 9 A:

```text
t_min = 60 * 0.440 / 9 = 2.93 min
```

If average hover current is 7 A:

```text
t_min = 60 * 0.440 / 7 = 3.77 min
```

Expected early prototype flight time:

```text
2-4 minutes
```

Longer flight time should not be pursued by adding battery mass until hover and recovery control margins are proven.

## Prop Guard Geometry

Guard inner diameter:

```text
D_inner = D_prop + 2c
```

Where:

- `D_prop` is propeller diameter
- `c` is radial clearance, target `2-3 mm`

Guard outer diameter:

```text
D_outer = D_inner + 2t_wall
```

Where:

- `t_wall` is guard wall thickness, starting target `1.5-2.5 mm`

Example for a 2.0 in prop:

```text
D_prop = 50.8 mm
c = 2.5 mm
t_wall = 2.0 mm

D_inner = 50.8 + 2(2.5) = 55.8 mm
D_outer = 55.8 + 2(2.0) = 59.8 mm
```

With four circular guards in an X layout, a 90-100 mm diagonal motor wheelbase gives a compact but plausible 125-140 mm outer footprint depending on guard spacing.

## Guard Functional Elastic Check

Define:

- `k`: radial guard stiffness, `N/m`
- `c_sigma`: stress per unit force, `Pa/N`
- `E_impact`: conservatively assigned impact energy, `J`

```text
delta_impact = sqrt(2 E_impact / k)
F_equivalent = sqrt(2 E_impact k)
sigma_impact = c_sigma F_equivalent
```

Acceptance:

```text
available clearance / delta_impact >= 2
elastic allowable stress / sigma_impact >= 3
```

This is a low-energy linear-elastic functional check only. It cannot establish high-energy fracture survival.

## Recovery Timing

Recovery cannot be specified only as "stable within 3 seconds." During ideal free fall, distance grows with the square of time:

```text
d = 0.5 * g * t^2
```

| Unarrested Fall Time | Ideal Fall Distance |
|---:|---:|
| 0.25 s | 0.31 m |
| 0.50 s | 1.23 m |
| 0.75 s | 2.76 m |
| 1.00 s | 4.91 m |

The recovery test must separately measure:

- launch-detection latency
- motor-start latency
- attitude-arrest time
- vertical-velocity-arrest time
- time until stable hover
- minimum successful release height
- gyro saturation and estimator disagreement

The fixed 3 s value is used only as the stable-hover confirmation window after recovery, not as an acceptable time to recover.

Stable-hover confirmation:

- roll/pitch within +/-5 deg
- yaw rate below low threshold selected during tuning
- no cage contact
- altitude remains inside test envelope
- all conditions hold for 3 s

Recovery success criteria must be set from fixture data after the propulsion system, controller, and release conditions are defined. Tests should report success rate across release height, initial attitude, initial angular rate, and battery voltage.

The initial angular rate must remain below 80% of the verified gyro range. Recovery outside the externally validated estimator envelope is rejected.

The executable preliminary model and its verification tests are under [Analysis](../Analysis/README.md).

## Marker Tracking Limits

Initial command envelope:

| Command | Limit |
|---|---:|
| Horizontal velocity | 0.3 m/s |
| Yaw rate | 30 deg/s |
| Altitude change rate | 0.2 m/s |
| Target distance | 1.0-1.5 m |
| Target lost hold | 2 s |
| Target lost land | 5-10 s |

The first tracking controller should be yaw-only. Translational following should be enabled only after marker detection latency and hover stability are measured.

## Launch Detection Signals

Initial log channels:

- acceleration magnitude
- gyro magnitude
- attitude estimate
- battery voltage
- flight mode
- state-machine state
- classifier decision
- timestamp

Initial event classes:

| Actual Event | Expected Classification |
|---|---|
| held still | no launch |
| normal hand motion | no launch |
| bump while held | no launch |
| walking with drone | no launch |
| placed on table | no launch |
| controlled drop | launch candidate |
| controlled release | launch candidate |
| excessive tilt/rate | reject recovery |

No live recovery threshold should be trusted until a log dataset, confidence-bound analysis, and confusion matrix exist. Zero observed events are never reported as a true zero event rate.
