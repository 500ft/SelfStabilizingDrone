# Stage 1 - No "Throw"

## Summary

Stage 1 is the protected test-platform version of the larger throwable micro-UAV idea.

The goal is to build a guarded micro-drone that flies normally inside a cage, tracks a defined marker slowly, logs launch/drop events without auto-spinning motors, and prepares for controlled release recovery later.

Stage 1 does not include full hand throws, autonomous throw arming, general object following, outdoor flight, or chasing people/objects.

Stage 1 is successful when:

- the drone can hover manually
- the frame and guards are mechanically credible
- marker tracking works during normal hover
- launch/drop detection produces logs only
- all dangerous actions remain disabled unless manually commanded

## Build Targets

| Item | Requirement |
|---|---:|
| Target mass | 140 g |
| Absolute max mass | 170 g |
| Preferred total thrust | 400 g+ |
| Minimum thrust per motor | 85 g |
| Preferred thrust per motor | 100 g+ |
| Flight environment | indoor cage/netted enclosure |
| First tracking target | ArUco, AprilTag, or large color marker |
| Launch detection mode | log-only |
| Recovery mode | disabled in Stage 1 |
| Manual override | required |
| Emergency stop | required |

## Work Package 1: Requirements and Budget

Create a spreadsheet before buying parts.

Include:

- component name
- estimated mass
- measured mass after purchase
- cost
- current draw
- thrust data source
- notes/risk
- replacement/spare quantity

Budget allocation:

| Category | Target |
|---|---:|
| Flight controller/ESC | $50-$120 |
| Motors/props | $50-$120 |
| Batteries/charger | $50-$100 |
| Camera/vision board | $40-$120 |
| Frame/guard material | $30-$80 |
| Test cage materials | $50-$150 |
| Spares/contingency | 20-30% of total |

Do not buy the final hardware stack until the mass and thrust budget closes under 170 g.

## Work Package 2: Hardware Selection

Pick parts using this priority order:

1. published thrust data
2. weight
3. reliability/community support
4. replacement part availability
5. cost

Baseline architecture:

| Subsystem | Stage 1 Choice |
|---|---|
| Flight controller | micro STM32 board running ArduPilot or PX4 |
| ESC | micro 4-in-1 or integrated whoop board |
| Motors | brushless, 100 g+ thrust each preferred |
| Battery | 1S or 2S LiPo chosen from thrust/current data |
| Frame | custom guarded whoop-style frame or modified guarded frame |
| Vision | OpenMV or ESP32-S3 camera board |
| Target | ArUco/AprilTag preferred; color marker acceptable backup |

Battery decision:

- choose 1S only if thrust margin is still comfortable near full build mass
- choose 2S if 1S is too weak or requires excessive throttle
- document the reason in the build log

## Work Package 3: Mechanical Platform

Design the drone as a protected engineering test platform.

Required CAD outputs:

- full assembly
- guarded frame
- motor mounts
- prop guard geometry
- battery retention
- camera mount
- electronics stack
- CG location
- exploded view
- simple drawing set

Guard starting requirements:

| Feature | Requirement |
|---|---|
| Prop tip clearance | 2-3 mm minimum |
| Wall thickness | 1.5-2.5 mm starting point |
| Material | PETG, nylon, or reinforced filament |
| Repairability | modular/reprintable guard sections preferred |
| Validation | minor bump test and post-impact inspection |

Mechanical acceptance:

- battery cannot eject during minor cage bump
- camera angle remains fixed
- flight controller is mounted cleanly
- props do not contact guards under normal flex
- CG is near vehicle centerline
- frame can be disassembled and repaired

## Work Package 4: Test Cage

Build the cage before live testing.

Cage requirements:

| Feature | Requirement |
|---|---|
| Size | about 6 ft x 6 ft x 6 ft or larger if possible |
| Sides | netted or otherwise contained |
| Floor | padded |
| Access | closable door/flap |
| Safety | external emergency stop access |
| Recording | fixed camera/tripod angle |
| Marker | mountable target location |

The cage is part of the project, not just a workspace. Document it with sketches, photos, and test notes.

## Work Package 5: Manual Hover

Manual flight is the first real milestone.

Test sequence:

1. props-off motor direction check
2. calibration check
3. emergency stop check
4. restrained low-throttle test
5. short hop inside cage
6. 10-second hover
7. 30-second hover
8. minor bump/guard inspection

Pass criteria:

| Function | Pass condition |
|---|---|
| Arm/disarm | reliable |
| Emergency stop | reliable |
| Hover | 30 seconds without cage contact |
| Vibration | IMU data usable during hover |
| Guards | survive minor bumps |
| Battery/motors | no overheating |
| Pilot control | stable enough for repeat testing |

If manual hover fails, stop autonomy work and fix propulsion, vibration, CG, tuning, or frame stiffness first.

## Work Package 6: Marker Tracking During Normal Hover

Debug tracking only after manual hover works.

Tracking progression:

1. detect marker on bench
2. measure camera frame rate
3. measure detection latency
4. detect marker while drone is powered but grounded
5. detect marker during hover
6. yaw-only centering
7. slow forward/back movement
8. target-loss failsafe

Command limits:

| Command | Limit |
|---|---:|
| Horizontal velocity | 0.3 m/s max |
| Yaw rate | 30 deg/s max |
| Altitude change rate | 0.2 m/s max |
| Target distance | 1.0-1.5 m |
| Target lost hold | 2 seconds |
| Target lost land | 5-10 seconds |

Pass criteria:

- marker is detected reliably in cage lighting
- yaw-only centering works before translation is enabled
- drone does not contact cage during tracking
- target loss causes hold, then land
- camera blocked behavior is tested

## Work Package 7: Launch/Drop Detection Logs

Stage 1 launch detection is log-only.

The system records what it would do, but motors stay under normal manual control.

Log fields:

- acceleration magnitude
- gyro magnitude
- attitude estimate
- event timestamp
- state-machine state
- classifier decision
- battery status
- cage/test-mode flag

Test cases:

| Actual event | Expected decision |
|---|---|
| held still | no launch |
| hand movement | no launch |
| bump while held | no launch |
| walking with drone | no launch |
| placed on table | no launch |
| short drop onto padding | launch candidate |
| gentle toss onto padding | launch candidate |
| bad attitude event | reject recovery |

Pass criteria:

- zero false live-arm decisions in handling tests
- above 90% detection on controlled drop/release tests after tuning
- confusion matrix created
- plots created for acceleration, gyro, attitude, and state transitions

## Stage 1 Final Demo

A successful Stage 1 demo shows:

1. CAD and mass/thrust budget.
2. Guarded drone platform.
3. Test cage.
4. Manual 30-second hover.
5. Marker tracking during normal hover.
6. Target-loss behavior.
7. Launch/drop log-only classifier.
8. Emergency stop/manual override.

Do not include full throw recovery in Stage 1. That becomes Stage 2 after Stage 1 data proves the platform is stable and safe enough.

## Stage 1 Exit Criteria

Stage 1 is complete when:

- complete flying mass is under 170 g
- manual hover is reliable inside cage
- marker tracking works slowly during normal hover
- launch/drop classifier logs decisions without motor response
- no-go conditions are documented
- emergency stop and manual override are verified
- portfolio artifacts are collected

Stage 2 may begin only after these are true.
