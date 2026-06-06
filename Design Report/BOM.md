# Bill of Materials

This BOM is a starting point for a protected micro-UAV. Prices and masses are planning values until parts are selected and weighed. Do not freeze the maximum mass until selected-component data and the complete CAD mass model exist.

A spreadsheet-friendly version is available in [BOM.csv](BOM.csv).

## Baseline Architecture

| Subsystem | Baseline Direction |
|---|---|
| Vehicle | guarded quadcopter |
| Propulsion | 2S, 1103-class brushless motors, 2.0-2.3 in props |
| Flight control | ArduPilot-capable STM32 H7/F7 flight controller |
| ESC | 4-in-1 ESC, 12 A per channel minimum preferred |
| Vision | OpenMV for AprilTag/marker tracking, or ESP32-S3 for lower-cost color tracking |
| Battery | removable central 2S LiPo |
| Frame | custom guarded frame, PETG/nylon prototype |
| Test setup | netted cage and release fixture |

## Recommended Planning BOM

The authoritative row-level BOM is [BOM.csv](BOM.csv), and the authoritative flying-mass rollup is [mass_budget.csv](../Engineering%20Data/mass_budget.csv). Every uncertain flying mass is recorded as best, nominal, and worst with a basis and source.

## Initial Mass Budget

| Result | Current Planning Value |
|---|---:|
| Sigma best | 106.5 g |
| Sigma nominal | 140.75 g |
| Sigma worst | 175.0 g |
| Unmodeled-hardware allowance | 5.0 g |
| Proposed frozen maximum | 180.0 g |
| Nominal margin to proposed maximum | 39.25 g |
| Abort threshold | 225 g |

The proposed `180 g` maximum is not frozen. It must be recalculated after component selection and completion of the CAD mass model.

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

## Candidate Source Notes

- The prior `15-18 g` total motor estimate was unsupported and has been replaced by a conservative `20 | 23 | 26 g` planning range until a motor is selected.
- Holybro Kakute H7 Mini and Matek H743 Mini are useful reference classes because they support modern autopilot firmware and onboard logging, but exact availability must be checked before purchase.
- OpenMV is the preferred marker-tracking path if AprilTag performance is the priority. ESP32-S3 is the lower-cost learning path if color-marker tracking is acceptable first.

## Do-Not-Buy-Yet List

Do not buy these until the basic propulsion and mass budget closes:

- expensive AI camera
- larger battery for longer flight time
- custom PCB
- carbon or nylon production frame
- extra sensors for "mother drone" coordination
- outdoor GPS/positioning stack

Those are later upgrades, not V1 blockers.
