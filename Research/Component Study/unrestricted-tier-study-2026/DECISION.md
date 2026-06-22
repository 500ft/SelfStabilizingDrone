# Weight-Unrestricted Architecture Decision

**Research date:** 2026-06-22
**Scope:** Retain the guarded release/recovery mission and ArduPilot safety architecture; remove the 225 g, 2S, and 2-inch constraints. Prices are catalog snapshots or clearly identified engineering allowances, before tax and shipping.

## Decision

Build the **mission-optimal 3.5-inch architecture only if its propulsion mock-up passes the guarded thrust gate**. Do not replace the current Stage 1 value build merely because the mass ceiling was removed.

The winning architecture is a GEP-CL35 V2 guarded frame, Pixhawk 6C Mini, 6S 2105.5 propulsion, OAK-D Lite plus Pi Zero 2 W, and ARK Flow. It materially improves the three weak points in the locked build:

1. dual isolated/heated flight IMUs instead of one FC IMU;
2. global-shutter stereo vision with onboard inference instead of a rolling-shutter Nicla camera;
3. DroneCAN flow/range sensing instead of an MSP-UART peripheral.

It deliberately rejects the most expensive hardware. A Pixhawk 6X Pro, Jetson AGX Orin Industrial, OAK 4 D Pro W, and multi-kilogram industrial propulsion add compute and sensor ceiling but worsen inertia, power, guard size, integration time, and release safety.

## Three coherent tiers

| Tier | Purpose | Estimated flying hardware | Expected scale | Decision |
|---|---|---:|---:|---|
| Value | Cheapest credible recovery research vehicle | **about $333** | **129.8 g nominal** | Keep as the first build and control case |
| Capability ceiling | Highest rational COTS capability, independent of cost | **>$6,200 catalog airborne subtotal; likely >$9,000 complete** | Multi-kilogram, custom guarded airframe | Do not build for the original release mission |
| Mission-optimal | Maximize recoverability, evidence quality, and safe integration | **about $1,030; plan $1,000-$1,150** | **roughly 0.55-0.70 kg, bench-frozen** | Recommended only after propulsion gate |

The premium total is not a claim that a literal "most expensive" drone exists; cost has no upper bound. It is the highest-capability COTS reference assembled from defensible professional parts. Custom frame, carrier, cooling, SF45/B, and Herelink costs are not in its $6,200 airborne subtotal.

## Item selection

| Subsystem | Value / cheapest | Capability ceiling / expensive | Mission-optimal / recommended |
|---|---|---|---|
| Frame and guards | Existing custom 2-inch nylon frame | Custom 23-inch guarded industrial quad | **GEPRC GEP-CL35 V2**, $69.99 |
| Flight controller | **Kakute H7 Mini v1.5**, $58.99 | **Pixhawk 6X Pro + PM02D**, $797.99 | **Pixhawk 6C Mini Model A + PM02 V3**, $149.98 |
| ESC / distribution | HGLRC 13A 2-3S BB2 | Four integrated A6-M FOC/CAN arms | **Tekko32 F4 Mini 50A AM32**, about $69.99 inferred |
| Motors / props | EX1103 11000KV + Gemfan 2023-3 | Four **T-Motor A6-M + MF2311P-M** | **4 x GEPRC SPEEDX2 2105.5 2650KV + Gemfan D90-3** |
| Battery | GNB 2S 550 mAh 100C | Large 6S pack sized after industrial propulsion test | **6S 1050-1300 mAh high-rate LiPo**, final capacity bench-selected |
| Companion | Nicla Vision MCU | Jetson AGX Orin Industrial | **Pi Zero 2 W host**, $15 |
| Vision | Nicla onboard camera | **OAK 4 D Pro W**, $1,049 | **OAK-D Lite**, $169 |
| Flow / range | Matek 3901-L0X | ARK Flow + LightWare SF45/B | **ARK Flow DroneCAN**, $250 |
| Manual control | BetaFPV ELRS Lite | Herelink 1.1 | **RadioMaster RP3 V2 diversity ELRS**, $19.99 |
| Telemetry / logs | CRSF telemetry + onboard log | Herelink + Microhard P900 pair | **SiK V3 100 mW pair + onboard microSD**, $58.99 |
| Perception power | FC rail if measured safe | Custom high-power isolated DC/DC | **Separate 5 V regulator**, $20.99 allowance |
| Test equipment | DIY stand and cage | Instrumented industrial flight stand | **Calibrated <=5 kgf thrust stand + repeatable release rig** |

The approximate $1,030 optimal total includes $50 for mounts/wiring, $18 status hardware, a $45 battery allowance, and the catalog/inferred prices above. It excludes the optional $1,075 Tyto stand because that is support equipment, not flying hardware.

## Why the optimal tier wins

The weighted comparison uses recovery/control performance 30%, evidence and firmware support 20%, integration risk 20%, safety 15%, acquisition cost 10%, and extensibility 5%.

| Tier | Recovery | Evidence | Integration | Safety | Cost | Extensibility | Weighted score / 100 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Value | 6.0 | 7.0 | 7.0 | 7.0 | 10.0 | 5.0 | **69.0** |
| Capability ceiling | 9.5 | 8.0 | 3.0 | 2.0 | 1.0 | 10.0 | **59.5** |
| Mission-optimal | 9.0 | 9.0 | 8.0 | 8.0 | 6.0 | 8.0 | **83.0** |

These scores are an engineering decision aid, not measured performance. Propulsion, latency, and recovery success remain bench-gated.

## The order/no-order gate

Do not order the complete optimal architecture at once. First purchase or borrow only the propulsion-validation subset:

- one SPEEDX2 2105.5 2650KV motor;
- one D90-3 prop set and one spare geometry;
- one 50 A 6S-capable ESC;
- one representative 6S 1050-1300 mAh pack;
- one GEP-CL35 V2 guard/frame or a dimensionally representative duct fixture.

Freeze a provisional integrated mass of **700 g** for the first conservative screen. The pre-registered minimum is therefore:

\[
T_{motor,min} = \frac{2.0 \times 700}{4} = 350\ \mathrm{gf/motor}
\]

Acceptance at the minimum loaded pack voltage requires all of the following:

- uncertainty-adjusted static thrust **>=350 gf per motor** in the representative guard;
- no prop/guard contact and <=1.0 mm guard deflection at the proof load;
- battery sag <=10% during the acceptance step;
- 10-90% thrust rise <=100 ms;
- ESC/motor/connector temperature and current within their continuous ratings with >=20% planning margin.

If this passes, buy the optimal avionics. If it fails, first freeze the real mass and recompute `T_motor,min = mass/2`; then move to a larger guarded prop diameter. Do not compensate for a structural thrust miss by buying a more powerful companion computer.

## Avionics gates after propulsion passes

- OAK global-shutter pipeline: >=40 effective FPS, p95 exposure-to-classification <=40 ms.
- Complete event path: p95 sensor-event-to-accepted-MAVLink <=50 ms, p99 <=75 ms.
- Flow/range: <=0.25 m/s RMS velocity error and <=5% or 5 cm range error in the cage envelope.
- Timing: FC and companion event timestamps within 5 ms.
- Fault containment: FC remains stable and accepts manual kill when companion, OAK, CAN sensor, RC link, or telemetry link is removed independently.
- Power: no FC or companion brownout during simultaneous inference and full motor-step tests.

## Evidence boundary

Catalog evidence establishes component identity, interfaces, geometry, and nominal ratings. It does **not** establish guarded thrust, 6S current for the exact prop, recovery latency, classifier accuracy, estimator survival during release, or safe free-flight behavior. Those remain `BENCH_REQUIRED`; the detailed source trace is in [report.md](report.md) and the validated records in [results](results/).
