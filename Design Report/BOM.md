# Bill of Materials

This is the canonical Stage 1 catalog selection. Component identities are
locked for ordering, but catalog mass, thrust, current and price remain planning
evidence until delivered parts are weighed and bench-tested. Do not freeze the
maximum mass until the complete CAD mass model exists.

A spreadsheet-friendly version is available in [BOM.csv](BOM.csv).

## Baseline Architecture

| Subsystem | Baseline Direction |
|---|---|
| Vehicle | guarded quadcopter |
| Propulsion | EX1103 11000KV motors with Gemfan 2023-3 props on 2S |
| Flight control | Holybro Kakute H7 Mini v1.5 running ArduPilot 4.6+ |
| ESC | HGLRC XJB BS13A 2-3S 4-in-1 |
| Vision | Arduino Nicla Vision ABX00051 |
| Positioning | Matek 3901-L0X optical flow + lidar over one MSP UART |
| Battery | removable GNB GNB5502S100AHV 2S LiHV with XT30 |
| Frame | custom guarded frame, PETG/nylon prototype |
| Test setup | netted cage and release fixture |

## Recommended Planning BOM

The authoritative row-level BOM is [BOM.csv](BOM.csv), and the authoritative flying-mass rollup is [mass_budget.csv](../Engineering%20Data/mass_budget.csv). Every uncertain flying mass is recorded as best, nominal, and worst with a basis and source.

## Current Catalog Mass Budget

| Result | Current Planning Value |
|---|---:|
| Sigma best | 117.96 g |
| Sigma nominal | 129.76 g |
| Sigma worst | 149.5 g |
| Unmodeled-hardware allowance | 5.0 g |
| Proposed frozen maximum | 155.0 g |
| Nominal margin to proposed maximum | 25.24 g |
| Abort threshold | 225 g |

The proposed `155 g` maximum is not frozen. It must be recalculated after
receipt measurements and completion of the CAD mass model.

## Cost Budget

| Group | Target Cost |
|---|---:|
| Flight controller and ESC | $90-$140 |
| Motors and props | $45-$80 |
| Batteries and charger | $60-$130 |
| Vision system | $30-$160 |
| Receiver/control link | $15-$30 |
| Frame/guard materials and hardware | $30-$85 |
| Cage/release fixture | $70-$200 |
| Spares/contingency | 20-30% |

Expected total: approximately $350-$650 depending on vision board, test cage, and spare parts.

## Evidence Notes

- Kakute H7 Mini **v1.5** is required; earlier revisions use different IMUs and
  ArduPilot targets.
- The HGLRC XJB BS13A is a legacy part. Its electrical and mass specifications
  are supported by archived listings, but standalone stock must be verified.
- The EX1103 thrust/current point is a vendor result, not independent evidence.
  Acceptance is measured at 7.0 V under load.
- Nicla image-capture current is documented; inference latency and peak current
  remain bench-required.
- Nicla has no microSD socket. The prior standalone-card line was removed;
  Stage 1 numeric event data is sent to the FC over MAVLink.

## Do-Not-Buy-Yet List

Do not buy these until the basic propulsion and mass budget closes:

- alternate vision computer
- larger battery for longer flight time
- custom PCB
- carbon or nylon production frame
- extra sensors for "mother drone" coordination
- outdoor GPS/positioning stack

Those are later upgrades, not V1 blockers.
