# Propulsion bench input register — DR-CAD-01

Prepared 2026-09-08. **Input reconciliation only: not a fabrication-ready CAD model.**
The [parameter register](parameters.csv) separates manufacturer nominal envelopes,
model assumptions, frozen protocol constants and missing measurements. Blank numeric
cells mean unavailable, never zero. No row is an inspected or calibrated result.

## Source decisions

The current component register selects Happymodel EX1103 KV11000 and Gemfan
Hurricane 2023-3. On 2026-09-08 the [exact motor manufacturer page](https://www.happymodel.cn/index.php/2022/09/05/bassline-spare-part-ex1103-kv11000-brushless-motor/)
listed a 13.5 mm diameter, 15.5 mm length and 1.5 mm shaft. These are nominal
specifications, not a toleranced mounting drawing. Do not substitute the older
EX1103 6000/7000/8000/12000 family dimensions for the selected 11000 KV motor.
The [propeller manufacturer page](https://www.gemfanhobby.com/2023-hurricane-pc-3-blade.html)
listed a 52.17 mm disk and 1.5 mm T-mount. Matching shaft diameter alone does
not prove bell screw-pattern compatibility or dynamic clearance.
The same Gemfan page lists 1105–1108 as its adaptive-motor range, not the selected
1103. Happymodel's table uses a 2023R propeller at 7.4 V; this does not certify
the exact selected prop revision or the registered 7.0 V campaign. Owner fit
verification and measured performance therefore remain required.

No inspected motor-mount, load-cell or stand drawing is committed. Their fit
dimensions deliberately remain pending. The electrical
[hardware interface register](../../Engineering%20Data/hardware_interfaces.csv)
and wire data are not mechanical mounting evidence. Vendor specifications are
not licensed CAD exports and are not actual measurements of purchased hardware.

## Coordinate and evidence mapping

| Quantity | Definition and datum to record | Evidence destination |
| --- | --- | --- |
| Stand thrust axis | Unit vector along motor shaft and calibrated force-sensitive direction; record misalignment and positive force sign | Calibration artifact; raw `thrust_n` is calibrated force in N, not ADC counts or grams |
| Stand calibration lever | Perpendicular pivot-to-applied-force-line distance, with load/fixture deflection and uncertainty | Calibration/derivation artifact; not automatically raw `arm_m` |
| Vehicle authority radius | Body origin to motor center in the symmetric X-frame mixer; projected roll/pitch lever is radius divided by sqrt(2) | Raw `arm_m` plus geometry source/calibration and uncertainty |
| Derived authority | Four-motor symmetric prediction uses `2*sqrt(2)*arm_m*min(T_total*c/4,T_total*(1-c)/4)` | Reviewed derivation explains per-motor curves and produces `tau_rp_n_m` |
| Uncertainty | Force, radius, alignment, calibration, motor variation and covariance with stated coverage assumptions | Reviewed artifact and `expanded_uncertainty_n_m`, subtracted once by evaluator |

The [evidence contract](../../docs/specs/measured-authority-gate/evidence-contract.md)
requires unique raw and derived IDs, six sampled motors at every collective,
calibration identity and hashed artifacts. Six sampled motors characterize a
four-motor aircraft. The evaluator verifies bundle consistency, not the physical
truth or adequacy of the derivation. Neither the 60 mm assumed radius nor the
4.2 N modeled thrust may silently fill measured columns.

## Smallest owner input package (DR-CAD-02)

Supply the selected motor/prop revisions and measured screw/hub interfaces;
load-cell model, mounting drawing, rated/overload capacity and calibration;
bench anchor geometry; measured authority radius with body axes; and a
qualified operator's containment/stop-access review. Record dimension datums,
units, uncertainty and source revision, including a photo or approved drawing
where needed. Complete vehicle packaging is not required to design this stand.

DR-CAD-01 completes the sourced register with explicit unknowns as its work order
allows. It does **not** close DR-CAD-02, geometry tooling, fit-critical dimensions,
fabrication, calibration, containment approval or the physical authority gate.
Before downstream use, replace each relevant pending entry with reviewed evidence
and inspect vendor-nominal dimensions. Retain the
[energized-test safety gate](../../Instrumentation/propulsion-bench-safety-checklist.md).
