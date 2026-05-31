# Bill of Materials

This BOM is a starting point for a 140-170 g protected micro-UAV. Prices and masses are planning values until parts are selected and weighed. Do not freeze the CAD until measured mass replaces estimates.

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

| Item | Qty | Est. Mass | Est. Cost | Baseline Candidate | Notes |
|---|---:|---:|---:|---|---|
| Flight controller | 1 | 5.5-8 g | $55-$80 | Holybro Kakute H7 Mini or Matek H743 Mini | ArduPilot/PX4-capable class; verify availability before purchase |
| 4-in-1 ESC | 1 | 5-8 g | $35-$60 | 20x20 2S-4S 12 A class ESC | Current rating must match motor peak current |
| Brushless motors | 4 | 15-18 g total | $35-$60 | Happymodel EX1103 KV11000 class | Published data shows 100 g+ thrust possible on 2S with matching prop |
| Propellers | 3-5 sets | 1-4 g/set | $8-$20 | 2.0-2.3 in props matching motor data | Buy spares immediately |
| Battery | 3-4 | 25-40 g each | $30-$70 | 2S 450-650 mAh LiPo | Final size depends on mass and hover current |
| Receiver/control link | 1 | 1-3 g | $15-$30 | ELRS micro receiver | Manual override required |
| Vision processor | 1 | TBD | $20-$150 | OpenMV RT1062 or ESP32-S3 camera board | OpenMV is stronger for AprilTag; ESP32-S3 is cheaper |
| Camera/lens | 1 | included/TBD | included-$25 | camera matched to vision board | Need wide enough FOV for marker tracking |
| Frame/guards | 1 set | 25-45 g | $20-$60 | custom printed PETG/nylon | Must be weighed after each revision |
| Fasteners/inserts | 1 set | 3-8 g | $10-$25 | M1.4/M1.6/M2 hardware | Keep serviceable |
| Wiring/connectors | 1 set | 3-8 g | $10-$25 | silicone wire, battery connector, heat shrink | Easy to underestimate |
| Buzzer/status LED | 1 | 1-3 g | $5-$15 | active buzzer/LED | Useful for safety and debugging |
| Battery charger | 1 | N/A | $25-$60 | 2S LiPo-compatible charger | Required support equipment |
| Test cage materials | 1 | N/A | $50-$150 | PVC/wood frame, netting, padding | Build before hover tests |
| Release fixture materials | 1 | N/A | $20-$60 | simple drop/release rig | Stage 2, not first hover |

## Initial Mass Budget

| Group | Target Mass |
|---|---:|
| Motors and props | 18-22 g |
| Flight controller and ESC | 11-16 g |
| Receiver, buzzer, wiring | 8-14 g |
| Battery | 25-40 g |
| Vision board and camera | 10-25 g |
| Frame, guards, mounts, fasteners | 35-50 g |
| Margin | 10-20 g |
| Target total | 140 g |
| Absolute max | 170 g |

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

- Happymodel EX1103 KV11000 data lists 1-2S support and bench thrust exceeding 100 g with a 2S setup and matching prop.
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
