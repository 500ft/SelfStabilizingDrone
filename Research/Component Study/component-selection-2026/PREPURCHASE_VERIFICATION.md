# Stage 1 Pre-Purchase Verification

**Date:** 2026-06-21  
**Firmware baseline:** ArduPilot 4.6+  
**Decision policy:** retain the locked part unless evidence proves a blocker.

## Decision summary

The Stage 1 architecture closes at the desk: the Kakute H7 Mini exposes enough
serial ports and output groups for the Stage 1 devices while reserving GPS and
FPV control resources. The conservative 5 V peripheral budget uses 550 mA of a
1.5 A design capacity, leaving **63.3% margin**. No FC substitution is required.

One incompatibility was found and resolved: Nicla Vision has no microSD socket.
The standalone microSD was removed from the flying BOM. Stage 1 sends numeric
release-event data to the FC over MAVLink; an SPI storage board is considered
only if later image-log experiments prove it necessary. The revised nominal
flying mass is **129.76 g** and catalog cost is approximately **USD 333**.

## Evidence that changes an order

| Item | Finding | State | Purchase decision |
|---|---|---|---|
| Kakute H7 Mini | Revision v1.5 is supported by ArduPilot 4.6+ and provides the required serial/output resources | CONFIRMED | Order v1.5 only |
| HGLRC XJB BS13A | Electrical/mass specifications are consistent across legacy listings, but it is an old part | INFERRED | Confirm standalone stock before ordering |
| EX1103 + 2023-3 | The 121.9 gf/9.2 A point is not independent and is not at the 7.0 V acceptance condition | BENCH_REQUIRED | Order baseline; do not freeze performance |
| Gemfan 2023-3 | Geometry and mass are official, but Gemfan lists 1105-1108 as the recommended motor class | BENCH_REQUIRED pairing | Confirm mount and thrust on the exact EX1103 |
| GNB pack | Identity and 29 g mass are consistently listed; 100C is not accepted as proof | BENCH_REQUIRED | Order only after manual logistics confirmation |
| Nicla Vision | 5 V input, translated 3.3 V UART and 105 mA average capture current are documented | CONFIRMED | Order; measure inference peak and latency |
| Matek 3901-L0X | One MSP UART carries both flow and range data; manufacturer marks it EOL | CONFIRMED / stock risk | Confirm stock before ordering |

## Resource conclusion

- Stage 1 uses SERIAL6 for CRSF, SERIAL4 for MSP flow/range and SERIAL2 for
  Nicla MAVLink.
- SERIAL3 remains reserved for GPS, SERIAL1 for future VTX control and SERIAL7
  for optional receive-only ESC telemetry.
- M1/M4 share PWM group 1; M2/M3 share group 2. All four use the same DShot
  protocol and rate. LED output 9 is isolated in group 5; buzzer has dedicated
  pads.
- Bidirectional DShot is optional, not assumed. The legacy BB2 ESC may require
  compatible firmware; without it, UART7 remains the telemetry option.

The executable source of truth is
[`hardware_interfaces.csv`](../../../Engineering%20Data/hardware_interfaces.csv),
validated by `python3 Analysis/hardware_resources.py`.

## Pre-registered bench decisions

Thrust is measured at 8.4 V, 7.6 V and **7.0 V at the ESC input under load**.
The uncertainty-adjusted 7.0 V result controls the decision:

- `>=112.5 gf/motor`: full 225 g reserve;
- `100-112.4 gf/motor`: 200 g planning ceiling;
- below 100 gf/motor: allowable frozen mass is twice measured per-motor thrust;
- actual frozen mass above that limit: blocker.

ESC unconditional current is `<=10.4 A/motor`; battery unconditional current is
`<=44 A pack`. Nicla p95 event-to-MAVLink latency must be `<=100 ms` for Stage 1
log-only use and `<=50 ms` for any future recovery candidate.

## Explicitly deferred

- Battery shipping/customs research. Checklist status remains
  `LOGISTICS_UNVERIFIED` and must be cleared manually before placing that order.
- Independent propulsion truth, battery sag, ESC temperature and Nicla latency.
- Alternate propulsion hardware. Mass freeze is the primary response to a
  shortfall; no speculative fallback prop is ordered.
- External image storage, GPS and FPV.
