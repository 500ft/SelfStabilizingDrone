# Preliminary Calculations

These calculations are the first sizing pass for the protected throwable micro-UAV. Replace assumptions with measured values as parts are selected.

## Mass and Thrust Targets

Given:

- target mass: `m_target = 140 g = 0.140 kg`
- maximum mass: `m_max = 170 g = 0.170 kg`
- minimum thrust-to-weight ratio: `T/W = 2.0`
- number of motors: `n = 4`

Required total thrust at maximum mass:

```text
T_required_total = 2.0 * 170 g = 340 g
```

Required thrust per motor:

```text
T_required_motor = 340 g / 4 = 85 g
```

Preferred design target:

```text
T_preferred_motor >= 100 g
T_preferred_total >= 400 g
```

At 170 g mass and 400 g total thrust:

```text
T/W = 400 / 170 = 2.35
```

## Hover Thrust

Hover thrust per motor:

```text
T_hover_motor = mass / 4
```

| Mass | Hover Thrust Per Motor |
|---:|---:|
| 140 g | 35.0 g |
| 150 g | 37.5 g |
| 160 g | 40.0 g |
| 170 g | 42.5 g |

The selected motor/prop/battery combination should produce hover thrust well below maximum throttle.

## Example Motor Data Check

Example reference: Happymodel EX1103 KV11000 on 2S with matching small propeller data shows thrust values above 100 g at high throttle. That makes the 1103 2S class plausible for a 170 g vehicle, but current draw and heat must be respected.

Planning interpretation:

- `85 g/motor` is the minimum acceptable thrust.
- `100 g+/motor` is the preferred selection threshold.
- ESC current rating should cover peak current with margin.
- Hover current must be estimated from thrust data, then measured on the built vehicle.

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

The fixed 3 s value is used only as the stable-hover confirmation window after recovery, not as an acceptable time to recover.

Stable-hover confirmation:

- roll/pitch within +/-5 deg
- yaw rate below low threshold selected during tuning
- no cage contact
- altitude remains inside test envelope
- all conditions hold for 3 s

Recovery success criteria must be set from fixture data after the propulsion system, controller, and release conditions are defined. Tests should report success rate across release height, initial attitude, initial angular rate, and battery voltage.

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

No live recovery threshold should be trusted until a log dataset and confusion matrix exist.
