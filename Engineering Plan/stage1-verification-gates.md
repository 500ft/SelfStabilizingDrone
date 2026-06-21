# Stage 1 Verification Gates and Resource Map

**Status:** pre-registered before bench measurement. Thresholds are encoded in
`Analysis/gates.py` and enforced by `Analysis/tests/test_gates.py`. Do not edit a
threshold to fit a result — record the result against the threshold as written.

Authoritative supporting registers:

- [`hardware_interfaces.csv`](../Engineering%20Data/hardware_interfaces.csv)
- [`power_budget.csv`](../Engineering%20Data/power_budget.csv)
- [`component_verification.csv`](../Engineering%20Data/component_verification.csv)
- [`purchase_checklist.csv`](../Engineering%20Data/purchase_checklist.csv)

Firmware target: **ArduPilot** (PX4 informational only). BOM change policy:
retain locked parts unless evidence proves a **blocker** (incompatibility,
unavailability in all target markets, unsafe margin, or unsupported critical
claim). "A better part exists" is not a blocker.

## 1. Resource and power closure (verify vs the exact Kakute H7 Mini revision)

| Function | Serial | Pad | Timer group | Stage |
|---|---|---|---|---|
| ELRS/CRSF receiver | SERIAL6 | UART6 | — | Stage 1 |
| Matek 3901-L0X flow+lidar (MSP v2) | SERIAL4 | UART4 | — | Stage 1 |
| Nicla Vision MAVLink | SERIAL2 | UART2 | — | Stage 1 |
| GPS | SERIAL3 | UART3 | — | Stage 2 reserved |
| FPV/VTX control | SERIAL1 | UART1 | — | Stage 2 reserved |
| ESC telemetry | SERIAL7 (RX-only) | UART7 | — | Optional |
| Configuration/diagnostics | SERIAL0 | USB | — | Bench |
| Motor 1 / Motor 4 | — | M1 / M4 | PWM group 1 | Stage 1 |
| Motor 2 / Motor 3 | — | M2 / M3 | PWM group 2 | Stage 1 |
| Status LED (NeoPixel) | — | LED | PWM group 5 | Stage 1 |
| Buzzer | — | BUZZER pad | GPIO | Stage 1 |

Notes: the 3901-L0X carries flow **and** lidar over one MSP UART (no separate
I²C). M1/M4 and M2/M3 share timer groups and must run compatible output rates.
Prefer bidirectional DShot for RPM telemetry, which frees SERIAL7. Confirm every
pad is **physically broken out on the Mini** (it omits pads the full-size board
has), and verify Nicla↔Kakute UART logic levels (3.3 V) and common ground.

Sources: Holybro pinout
(https://docs.holybro.com/autopilot/kakute-h7-v1-v2-mini/kakute-h7-mini/pinout),
ArduPilot Kakute mapping
(https://ardupilot.org/sub/docs/common-holybro-kakuteh7mini-v13.html).

Power: budget the 5 V rail at the **conservative 1.5 A** peripheral limit until
the 1.5 A / 2 A doc discrepancy is resolved; require ≥25% margin; if it does not
close, add a separate 5 V regulator rather than replacing the FC. The current
worst planning load is 550 mA, leaving **63.3% margin**; Nicla, ELRS and status
hardware peak currents remain measurement items.

Resolved interface blocker: Nicla Vision has no microSD socket. The standalone
card was removed from the Stage 1 flying BOM; numeric events are logged through
MAVLink to the flight controller. External SPI storage is deferred unless image
logging becomes a demonstrated requirement.

## 2. Pre-registered propulsion gate

Test at 8.4 V (full), 7.6 V (nominal), and **7.0 V under load (acceptance,
3.5 V/cell)**. Use the uncertainty-adjusted lower bound. The 121.9 gf vendor
claim has only **8.4% reserve** over the 225 g boundary and is BENCH_REQUIRED.

| 7.0 V result (gf/motor) | Decision |
|---|---|
| ≥ 112.5 | Full 225 g reserve passes |
| 100 – 112.4 | Supports 200 g ceiling; freeze max ≤ 2 × measured |
| < 100 but frozen mass ≤ 2 × measured | Conditional pass, reduced frozen max |
| frozen mass > 2 × measured | Propulsion BLOCKER |

**Mass freeze is the primary response to a shortfall** (every gf/motor buys 2 g
of frozen mass; at 129.8 g only 64.9 gf/motor is needed). Do not change
propulsion if the system still closes against the frozen mass. Reopen propulsion
only when required frozen mass exceeds the limit, in this lever order:
(1) higher-solidity 2-inch prop, (2) larger-diameter prop with revised guards,
(3) motor/prop change — each requires evidence of higher **7.0 V static thrust**
within current limits. Do not order a speculative fallback prop now.

## 3. ESC, battery, vision gates

- **ESC** (per motor, peak + uncertainty): ≤10.4 A PASS · 10.4–13 A thermal
  validation · >13 A sustained or >20 A transient FAIL.
- **Battery** (pack peak): ≤44 A PASS · 44–55 A sag+thermal validation · >55 A
  or unacceptable sag/temp FAIL. C-rating BENCH_REQUIRED regardless of vendor
  spec.
- **Nicla** (p95 sensor-event→MAVLink latency): ≤50 ms recovery candidate ·
  50–100 ms log-only · >100 ms ineligible. ≤25 ms acquisition + ≤25 ms
  inference/fusion/tx ⇒ a one-frame path needs ≥40 effective FPS.

## 4. Research batches (5 working days, then stop)

1. Exact FC revision, pads/resources, propulsion evidence, power, interfaces.
2. Exact SKUs, connectors, mounting hardware, accessories, credible suppliers,
   blocker-triggered substitutes.

Ignore country-specific customs/hazmat shipping during research. Availability
passes when a credible local, international, or Chinese supplier exists.
Unresolved noncritical claims become ASSUMED or BENCH_REQUIRED and do not delay
ordering.

## 5. Purchase checklist (carry forward)

> **Battery hazmat/logistics: UNVERIFIED — confirm before placing the battery
> order.** Any battery substitution reopens the mass, connector, continuous-
> current, voltage-sag, and thermal screens.

Each line: exact SKU · qty · supplier · required accessories · "verify on
receipt" measurement · evidence state · blocker status.
