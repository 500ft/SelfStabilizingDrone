# Bill of Materials

This is the canonical Stage 1 catalog selection. Component identities are
locked for ordering, but catalog mass, thrust, current and price remain planning
evidence until delivered parts are weighed and bench-tested. Do not freeze the
maximum mass until the complete CAD mass model exists.

A spreadsheet-friendly version is available in [BOM.csv](BOM.csv). Vendor
performance figures under load for every part are collected in
[component_specs_under_load.md](../Engineering%20Data/component_specs_under_load.md).

## Baseline Architecture

| Subsystem | Baseline Direction |
|---|---|
| Vehicle | guarded quadcopter |
| Propulsion | EX1103 11000KV motors with Gemfan 2023-3 props on 2S |
| Flight control | Holybro Kakute H7 Mini v1.5 running ArduPilot 4.6+ (stable 4.6.3) |
| ESC | Flywoo GOKU G45M 45A 2-6S AM32 4-in-1 (20x20) |
| Vision | Arduino Nicla Vision ABX00051 |
| Positioning | MicoAir MTF-01 optical flow + lidar over one MAVLink UART |
| Battery | removable GNB GNB5502S100AHV 2S LiHV with XT30 |
| Frame | custom guarded frame, PETG/nylon prototype |
| Test setup | netted cage and release fixture |

## Recommended Planning BOM

The authoritative row-level BOM is [BOM.csv](BOM.csv), and the authoritative flying-mass rollup is [mass_budget.csv](../Engineering%20Data/mass_budget.csv). Every uncertain flying mass is recorded as best, nominal, and worst with a basis and source.

## Current Catalog Mass Budget

| Result | Current Planning Value |
|---|---:|
| Sigma best | 123.86 g |
| Sigma nominal | 135.66 g |
| Sigma worst | 156.0 g |
| Unmodeled-hardware allowance | 5.0 g |
| Proposed frozen maximum | 165.0 g |
| Nominal margin to proposed maximum | 29.34 g |
| Abort threshold | 225 g |

Updated 2026-07-03 for the ESC and flow-sensor substitutions (+5.9 g nominal
vs the prior 129.76 g; T/W at nominal drops from ~3.75 to ~3.59, still well
above the 2.0 requirement). The proposed `165 g` maximum is not frozen. It must
be recalculated after receipt measurements and completion of the CAD mass model.

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

## Availability Audit (re-checked 2026-07-03)

Every part was re-verified against live listings on 2026-07-03. The 2026-06-22
availability risks are resolved: two parts were substituted (blocker: no longer
purchasable), and one prior claim was found stale. OQ-007 and OQ-008 in
[OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md) are closed.

| Part | 2026-07-03 finding | Resolution |
|---|---|---|
| Holybro Kakute H7 Mini **v1.5** | **In stock at Holybro direct, $58.99** (v1.3 sold out). The 2026-06-22 "effectively unavailable" claim was stale. | **Keep.** OQ-007 closed. |
| HGLRC XJB BS13A | Discontinued. 8-bit BLHeli_S BB2, 3S max, no current sensor — outdated even where old stock exists. | **Substituted:** Flywoo GOKU G45M 45A 2-6S AM32 4-in-1, 6.4 g, current sensor, bidirectional DShot, in production (~$45). |
| Matek 3901-L0X | Manufacturer-confirmed EOL. | **Substituted:** MicoAir MTF-01 (PMW3901 flow + 8 m ToF, 4.5 g, MAVLink, native ArduPilot support), in production (~$30). |
| All other flying parts | EX1103, Gemfan 2023-3, GNB 550 2S 100C, ELRS Lite Flat V1.2, VIFLY Finder Mini, Nicla Vision: all confirmed in production and stocked. | Keep. Nicla official price dropped to $68.17. |

## Evidence Notes

- Kakute H7 Mini **v1.5** is required; earlier revisions use different IMUs and
  ArduPilot targets. In stock at Holybro direct as of 2026-07-03.
- The GOKU G45M is rated 2-6S by Flywoo (some retailer pages say 3-6S);
  2S-LiHV operation at 7.0-8.4 V is a **receipt-check item** before the ESC
  gate. Its current sensor gives battery telemetry the BS13A never had; the
  scale (`BATT_AMP_PERVLT`) must be calibrated on the bench.
- The MTF-01 talks MAVLink1 to ArduPilot (`SERIALx_PROTOCOL=1`,
  `SERIALx_OPTIONS=1024`, `FLOW_TYPE=5`, `RNGFND1_TYPE=10`, sensor
  `mav_id=200` set via MicoAssistant).
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
