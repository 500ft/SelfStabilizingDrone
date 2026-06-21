# Stage 1 Locked BOM — Guarded Micro-UAV (SelfStabilizingDrone)

**Date:** 2026-06-20 · **Status:** LOCKED for Stage 1 (buy / build / test) · **Source:** `Component_Selection_2026.xlsx` (deep-research, 2026-06-19) · **Amended:** 2026-06-21 after interface verification

This is the single recommended build. It exists to stop decision drift: one part per
subsystem, with the reason it was chosen and the main option it beat. Full ranked
candidate lists (top 5–10 per category, with sources and confirmed-vs-inferred tags)
live in `Component_Selection_2026.xlsx`.

## The one decision that mattered: autonomy fork → H7/F7 research path

Two viable architectures:

- **Mass-minimal:** whoop-style AIO (Happymodel X12, ~5 g, ESC+VTX+RX onboard, Betaflight). Lightest, fewest parts.
- **Research/control-heavy (CHOSEN):** ArduPilot/PX4-capable H7 flight controller + companion vision board. Heavier and more wiring, but real logging, estimator access, failsafes, and clean MAVLink integration.

**Decision: H7 research path.** The recovery problem is a *state-estimation and control-authority* problem; it needs flight logs, estimator visibility, and failsafes far more than it needs the absolute lightest FC. The mass budget makes this free: the locked build is **~130 g vs the 200 g target**, so there is no reason to trade away research capability for grams. The mass-minimal AIO is recorded as the rejected alternative, not deleted — if a future mass crisis appears, it's the fallback.

## Locked BOM (flying hardware)

| Subsystem | Locked part | Mass (g) | ~USD | Why this / rejected |
|---|---|---:|---:|---|
| Flight controller | Holybro Kakute H7 Mini | 5.5 | 65 | ArduPilot/PX4, 6 UART (MAVLink companion), baro, blackbox. Rejected: Happymodel X12 AIO (Betaflight-only — no estimator/failsafe depth). |
| ESC 4-in-1 | HGLRC 13A 2-3S BB2 (20×20) | 3.0 | 18 | 20×20 matches the FC mount; 13 A/ch ≫ 9.2 A/motor; lightest. Rejected: FD13A (16×16, won't stack); Tekko32 45–50 A (over-spec, ≤15.6 g). |
| Motors ×4 | Happymodel EX1103 11000KV | 15.2 | 36 | Only motor with a published 2S+2023 thrust curve (121.9 g/motor). Rejected: <10000KV (fails T/W); T-Motor F1103 (+~5 g). |
| Propellers (+spares) | Gemfan Hurricane 2023-3 | 3.5 | 6 | The exact prop behind the validated thrust figure. Rejected: 2.5″ pitch (more current); sub-2″ (less thrust). |
| Battery | GNB 2S 550 mAh 100C (XT30) | 29.0 | 14 | 55 A cont ≫ 36.8 A peak. Rejected: 450 mAh 75C (33.75 A — FAILS current screen); BT2.0 (connector-limited). Budget alt: BetaFPV LAVA 550 75C. |
| Vision / compute | Arduino Nicla Vision | 19.8 | 90 | Camera + IMU + ToF in 20 g — release detection is motion fusion. Rejected for Stage 1: Coral Micro (NPU, mass unpublished); OAK-D-Lite (61 g/5 W). |
| Positioning | Matek 3901-L0X (flow + lidar) | 2.0 | 26 | Flow + height in 2 g, native ArduPilot. GPS deferred (outdoor only). |
| Control link RX | BetaFPV ELRS Lite (+ antenna) | 0.46 | 12 | Lightest; FC has no onboard RX. Upgrade: RadioMaster RP3 diversity if the guard shadows the antenna. |
| Buzzer + LED | VIFLY Finder Mini + WS2812 | 3.3 | 18 | Self-powered finder survives LiPo ejection; LED status/orientation. |
| Wiring / connectors | XT30 + 22/26 AWG + JST-SH | 5.5 | 8 | XT30 for 36.8 A peak headroom. Weigh finished harness. |
| Frame + guards + fasteners | Printed nylon frame + stiff guards + steel M2 | 42.5 | 40 | **Design work** (items 10/16/18). Guard ring must meet ≤1.0 mm deflection (SF ≥ 2.0) — verify by FEA + push test. |
| Vision logging | **Removed from Stage 1** | 0 | 0 | Nicla has no microSD socket. Send numeric event data to the FC over MAVLink; add an SPI reader only if image logging becomes required. |
| FPV video | **Deferred to Stage 2** | 0 | 0 | Not needed for manual cage hover (REQ-FLIGHT-001, LOS). If added: analog Caddx Ant Lite + Reaper Nano (~3.6 g, needs 5 V BEC). |
| GPS | **Deferred (outdoor only)** | 0 | 0 | Indoor recovery uses optical flow. Outdoor add-on: Matek M10Q-5883 (8 g). |

**Nominal flying total: ~129.8 g · ~$333.**
Margin vs 200 g target: **+70 g** · vs 225 g abort ceiling: **+95 g** · **T/W ≈ 3.75** (≥ 2.0 required).
Even worst-case (frame 50 g, vision 25 g) + Stage-2 FPV (~3.6 g) stays well under 225 g.

**Support gear (non-flying, not in total):** ToolkitRC M6AC charger ~$60 · thrust stand (DIY 1–2 kg load cell ~$30, or used RCbenchmark 1520 ~$165) · PVC+net test cage ~$40 · tethered release fixture ~$20.

## Engineering screens (both pass)

- **Thrust-to-weight:** 4 × EX1103 11000KV on Gemfan 2023R = 4 × 121.9 g = **487.6 g** static thrust ⇒ T/W ≈ **3.75** at 130 g (2.44 even at a full 200 g). Requirement ≥ 2.0. ✅
- **Battery current:** 4-motor peak = 4 × 9.2 A = **36.8 A**. GNB 550 mAh 100C = 55 A continuous ⇒ pass with margin. (450 mAh 75C = 33.75 A would **fail** — this is the prior screening failure, now resolved by moving to 550 mAh.) ✅

## Must verify before / during purchase (don't treat as proven)

1. **EX1103 + Gemfan 2023 thrust on 2S** — 121.9 g is Happymodel's own figure; no independent 2S bench exists. **Confirm on the thrust stand** before freezing the design.
2. **Real 2S peak current** — bench-measure; it validates both the ESC sizing and the battery C-rating choice.
3. **Prop-guard deflection** — the ≤1.0 mm / SF ≥ 2.0 requirement is not a vendor spec. Verify the chosen nylon (or nylon+TPU) guard by FEA + static lateral push test.
4. **Arduino Nicla Vision release-detection FPS** — confirm the onboard TFLite/Edge Impulse model runs fast enough; rolling-shutter (GC2145) may push you to a global-shutter camera (OV9281 + Pi Zero 2 W) as a Stage-2 option.
5. **FC mounting pitch** — confirm M2 vs M2.5 before ordering standoffs.

## Deferred to Stage 2 (explicitly out of scope now)
FPV video · GPS · global-shutter vision path · ESC telemetry (BLHeli_32/AM32) · digital video (HDZero Whoop Lite if HD ever needed). None block Stage 1.
