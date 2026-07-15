# Wiring and Power Architecture

Compiled 2026-07-15, before frame CAD. This documents the full electrical
interconnect for the Stage 1 flying stack so the frame can be designed around
the harness, not the other way around. Serial/pad assignments are the
authoritative ones in [hardware_interfaces.csv](hardware_interfaces.csv);
rail loads are from [power_budget.csv](power_budget.csv); receipt checks live
in [component_verification.csv](component_verification.csv).

**Headline design fact: no separate converter or regulator is needed.** The
two conversions the system requires already exist inside locked parts:

1. **Motors** — brushless motors do not take DC. The Flywoo G45M 4-in-1 ESC
   *is* the converter (battery DC → commutated 3-phase, one channel per
   motor). The battery connects to the ESC raw.
2. **Electronics** — the Kakute H7 Mini accepts battery voltage directly
   (2-6S) and its onboard BEC generates the 5 V rail. Worst-case planned
   peripheral load is 620 mA against the conservative 1.5 A budget (58.7%
   margin). Per the gate policy in
   [stage1-verification-gates.md](../Engineering%20Plan/stage1-verification-gates.md),
   a separate 5 V regulator is added only if that margin fails on the bench —
   it is not purchased speculatively.

## Voltage domains

| Domain | Source | Consumers |
|---|---|---|
| VBAT (7.0-8.7 V, 2S LiHV) | Battery via XT30 → ESC pads | ESC power stage → 4x EX1103; FC VBAT input (via ESC harness) |
| 5 V | FC onboard BEC (2 A spec, 1.5 A budget) | Nicla Vision, MTF-01, ELRS Lite, WS2812, VIFLY charging |
| 3.3 V logic | FC internal; Nicla `VDDIO_EXT=3.3 V` | All UART signalling (common ground required) |

```
GNB 2S 550 mAh (XT30)
   |
   v  XT30 pigtail soldered to ESC B+/B- pads (+ ships-with low-ESR cap at the pads)
Flywoo G45M 4-in-1 ESC  ── M1..M4 phase pads ──> 4x EX1103 (3 phase wires each)
   |
   v  8-pin JST-SH stack harness: VBAT, GND, CURRENT, TELEM, M1-M4 signals
Holybro Kakute H7 Mini  ── 5 V pads + UARTs ──> peripherals (table below)
```

## Connection map

| # | Connection | Detail | Register reference |
|---|---|---|---|
| 1 | Battery → ESC | XT30 pigtail to B+/B- pads; capacitor across the pads, minimal lead length | Battery gate thresholds in [stage1-verification-gates.md](../Engineering%20Plan/stage1-verification-gates.md) |
| 2 | ESC ↔ FC | 8-pin JST-SH harness carrying VBAT, GND, current-sense, telemetry, M1-M4 DShot | **Pin order must be verified before power** (see hazards) |
| 3 | Motors → ESC | 3 phase wires per motor to that corner's pads; phase order arbitrary — rotation direction is set in AM32/DShot, not by wire swapping | M1/M4 and M2/M3 timer groups in [hardware_interfaces.csv](hardware_interfaces.csv) |
| 4 | Nicla Vision | FC 5 V + GND; UART2 (SERIAL2) TX↔RX crossed; MAVLink2; `VDDIO_EXT=3.3 V` | hardware_interfaces row 4 |
| 5 | MTF-01 | FC 5 V + GND; UART4 (SERIAL4) TX↔RX crossed; MAVLink1 | hardware_interfaces row 3 |
| 6 | ELRS Lite RX | FC 5 V + GND; UART6 (SERIAL6) TX↔RX crossed; CRSF | hardware_interfaces row 2 |
| 7 | WS2812 LED | FC LED pad + 5 V + GND (dedicated NeoPixel output 9) | hardware_interfaces row 13 |
| 8 | VIFLY Finder Mini | FC BUZZER pads (active low); finder is internally battery-powered | hardware_interfaces row 14 |

All grounds are common: peripherals ground to the FC, the FC grounds to the
ESC through the stack harness. No isolated grounds anywhere in the vehicle.

## Wire gauge

| Run | Gauge | Sizing case |
|---|---|---|
| Battery pigtail (XT30 → ESC) | **18-20 AWG** | 36.8 A full-throttle transient (4 x 9.2 A). 22 AWG is undersized for this run — sag/heating at the transient peak |
| Motor phase wires | As delivered on EX1103 (~28 AWG class) | 9.2 A peak per motor, transient; verify temperature during the bench sweep |
| 5 V feeds | 26 AWG | ≤250 mA per device worst case |
| UART/signal | 26-28 AWG | Signal only |

## Hazards / receipt checks (blocking, before first power)

1. **ESC↔FC harness pin order.** Flywoo and Holybro 8-pin JST-SH orders are
   frequently different; a mismatched harness puts VBAT on a signal pin and
   destroys the FC. Verify pin-for-pin against both boards' printed pinout
   diagrams and re-pin the connector if they differ. Already registered as
   the G45M mounting follow-up in
   [component_verification.csv](component_verification.csv).
2. **First power-up goes through the XT30 smoke stopper** (Wave 1 item), on
   the bench supply at 7.0 V where possible, before any battery connection.
3. **2S support on the G45M is unverified (OQ-009)** — spin-up and
   full-throttle at 7.0 V on the bench before the propulsion gate.
4. **XT30 connector temperature** at the 36.8 A transient is a bench
   observation item (connector is ~30 A continuous class; the peak is
   transient, not continuous).

## Frame CAD implications

- **One 20x20 M2 stack, two boards**: ESC below (battery pads toward the
  pigtail exit), FC above. Reserve ~15-18 mm stack height including grommets
  and the capacitor (taller than the ESC body).
- **Battery bay is the trim variable**: the ≤0.5 mm thrust-line offset build
  requirement (Monte Carlo CG finding) is met by adjusting battery position —
  design a sliding/strap mount, not a fixed pocket.
- **Motor wire channels** along each arm from corner to ESC; the routed
  length also documents the real motor arm (60 mm ASSUMED in the mixer
  model — report the as-built value with the CAD mass table).
- **Sensor placement drives geometry**: Nicla camera needs an unobstructed
  view, MTF-01 faces straight down with a clear window, ELRS antenna kept
  clear of the battery.
