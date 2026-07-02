# Procurement Plan — 2026-07 (two-wave, bench-gated)

Derived from the locked Stage 1 BOM (`Research/Component Study/component-selection-2026/STAGE1_BOM.md`)
and `Engineering Data/purchase_checklist.csv`, updated for the 2026-07-02 audit findings:
the thrust stand is now the **decisive** purchase (EST-REC-007 must be measured — it decides
Monte Carlo scenario A vs C), and the checklist had **no radio transmitter** (RX only), which
the manual cage hover requires.

Prices are the 2026-06-19 catalog figures, ±10% + shipping. Stock risks: HGLRC 13A BB2
(legacy — confirm stock), Matek 3901-L0X (EOL — buy early if Wave 2 is likely).

## Wave 1 — bench-decisive (~$314). Order now.

| Item | Order qty | ~USD | Fallback use if the drone path dies |
|---|---:|---:|---|
| Holybro Kakute H7 Mini v1.5 | 1 | 65 | Generic ArduPilot/PX4 dev + logging IMU node for any vehicle |
| HGLRC 13A BB2 4-in-1 (20x20) | 1 | 18 | Micro-BLDC driver, pairs with the motors |
| Happymodel EX1103 11000KV | 6 | 54 | Micro builds; BLDC characterization specimens |
| Gemfan 2023-3 CW/CCW | 3 sets | 9 | Consumable |
| GNB 2S 550 mAh 100C LiHV XT30 | 2 | 28 | Bench/portable power. Batteries age: buy minimum now, 3rd pack in Wave 2 |
| ToolkitRC M6AC charger | 1 | 60 | Lifetime 1-6S bench charger (works for future RoboRacer packs) |
| 1-2 kg load cell + HX711 + cal masses | 1 | 30 | Highest cross-project reuse: drone thrust + EST-REC-007 torque + guard push test + RoboRacer mast deflection measurement |
| Torque-arm jig (printed + pivot hardware) | 1 | 10 | Part of the rig; measures per-motor thrust at a known arm -> tau_rp |
| Smoke stopper XT30 | 1 | 12 | Permanent bench insurance |
| LiPo charge bag | 1 | 10 | Safety stock |
| Wiring lot + M2 hardware | 1 | 18 | Universal shop stock |

## Wave 2 — gated on EST-REC-007 PASS (~$325)

Gate: measured tau_rp(hover) comfortably above the 0.004 N*m placeholder and the MC re-run
(`Analysis/monte_carlo_recovery.py` with measured authority) >= 95% lower-bound recovery at
2 rad/s. If the gate FAILS, stop here and write the negative design study (see PLAN.md park
criteria) — Wave 1 gear keeps ~80% of its value via reuse.

| Item | Order qty | ~USD | Fallback use |
|---|---:|---:|---|
| Arduino Nicla Vision | 1 | 90 | Standalone cam+IMU+ToF; release-detection classifier is a standalone deliverable |
| Matek 3901-L0X | 1 | 26 | Flow/height for any indoor robot (EOL — consider buying in Wave 1) |
| BetaFPV ELRS Lite RX | 1 | 12 | Needs an ELRS TX |
| VIFLY Finder Mini + WS2812 | 1 | 18 | Any future UAV |
| GNB 2S 550 (3rd pack) | 1 | 14 | As above |
| Frame + guard print + fasteners | 1 | 40 | Filament/hardware |
| PVC + net cage | 1 | 40 | Generic UAV test enclosure |
| Tethered release fixture | 1 | 20 | Generic rigging |
| RadioMaster Pocket ELRS TX | 1 | 65 | Any RC/UAV project. **Was missing from the checklist entirely.** Skip if a TX is already owned |

**Totals: Wave 1 ~$314 · Wave 2 ~$325 · all-in ~$639 (~$574 with an owned TX).**

## CAD notes for the modeling pass (Lane A+)

- Record masses against `Engineering Data/cad_mass_properties_template.csv`; use the
  verify-on-receipt masses from `purchase_checklist.csv` until real parts arrive.
- **Battery placement is the trim variable: thrust-line offset <= 0.5 mm** (build requirement
  derived from the Monte Carlo CG finding, `Analysis/current-results.md`).
- Guard geometry stays parametric: all placeholder guard cases currently FAIL the
  clearance SF >= 2.0 check; the real geometry must resolve them (FEA + push test with the
  Wave-1 load cell).
- Motor arm length is the other load-bearing dimension: it sets tau_rp in the mixer model
  (60 mm ASSUMED in scenario C) — model it explicitly and report it with the mass table.
