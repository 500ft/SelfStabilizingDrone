# Challenges

This project should start with the challenges that can kill the design earliest: mass/thrust, safe manual flight, and clean sensor data. Marker tracking and launch logic matter, but they come after the vehicle is physically viable.

## Hardware Challenges

- **Mass budget closure:** keep the complete drone under 170 g; every part needs an estimated and measured mass.
- **Motor, prop, and battery selection:** find motors with published thrust data showing 100 g+ thrust each with the exact prop and voltage.
- **1S vs 2S decision:** compare thrust, current draw, heat, battery mass, and flight time.
- **Flight controller choice:** pick one stack, preferably ArduPilot or PX4, and learn setup, calibration, and logging.
- **Power distribution:** design clean wiring, correct ESC current rating, battery connector choice, and voltage monitoring.
- **Vision board choice:** start with OpenMV or ESP32-S3, then prove marker detection speed before committing.
- **Failsafe hardware:** include reliable manual override, kill switch or disarm method, spare batteries, and spare props.

## Mechanical Challenges

- **Guarded frame design:** prop guards need enough stiffness and clearance so they do not flex into the props.
- **Center of gravity placement:** battery, camera, and electronics must keep the CG near the middle of the drone.
- **Battery retention:** the battery cannot eject during bumps, drops, or cage contact.
- **Camera mount:** the mount needs a fixed angle, low vibration, impact protection, and correct aiming for marker tracking.
- **Flight controller mounting:** isolate vibration without making the board loose.
- **Serviceability:** motors, guards, battery, and electronics should be easy to replace after crashes.
- **Test cage and release fixture:** build the cage early; the release fixture is what allows safe recovery testing later.

## Coding Challenges

- **Data logging first:** log IMU acceleration, gyro, attitude, battery, timestamps, and state-machine decisions.
- **Marker tracking pipeline:** detect the marker, estimate image-center error, measure FPS and latency, then command yaw-only centering.
- **Command limits:** cap velocity, yaw rate, altitude change, and target-follow distance.
- **State machine:** implement `SAFE_IDLE`, `DETECTION_CANDIDATE`, `AIRBORNE_CONFIRMED`, `RECOVERY_ALLOWED`, `STABLE_HOVER`, `TARGET_TRACK`, and `FAILSAFE`.
- **Launch classifier:** start with thresholds from logged IMU data, not guesses.
- **Failsafe handling:** handle target lost, camera blocked, companion disconnect, low battery, and excessive tilt/rate.
- **Ground analysis tools:** build scripts or notebooks to plot IMU data and create a confusion matrix.

## Best Starting Order

1. Build the mass, thrust, and power spreadsheet.
2. Choose motors, props, battery, flight controller, and frame size.
3. CAD the guarded frame and battery/camera/electronics layout.
4. Build the test cage.
5. Get manual hover working.
6. Add marker tracking during normal hover.
7. Add launch/drop logging.
8. Attempt controlled release recovery only after the earlier milestones pass.

## First Real Technical Milestone

The first serious milestone is:

> A guarded 140-170 g drone can manually hover for 30 seconds in a cage while logging clean IMU data.

Everything else depends on that.
