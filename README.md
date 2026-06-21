# Guarded Micro-UAV Project

This repository documents a staged learning project for a protected micro-UAV that can eventually detect a toss/drop/release event, stabilize in midair, and follow a designated target.

## Current Documents

- [Executable Engineering Plan](Engineering%20Plan/README.md)
- [Design Report](Design%20Report/README.md)
- [Bill of Materials](Design%20Report/BOM.md)
- [BOM CSV](Design%20Report/BOM.csv)
- [Preliminary Calculations](Design%20Report/calculations.md)
- [Executable Analysis](Analysis/README.md)
- [Current Preliminary Results](Analysis/current-results.md)
- [Instrumentation Plan](Instrumentation/README.md)
- [Safety and Release-Rig Plan](Safety/README.md)
- [Control Architecture and State Machine](Controls/README.md)
- [Open Questions](OPEN_QUESTIONS.md)
- [Project Evaluation: Hiring and Graduate-School Value](Project%20Evaluation/README.md)
- [Stage 1 - No "Throw"](Stage%201%20-%20No%20%22Throw%22/README.md)
- [Challenges](Challenges/README.md)
- [Component and Propulsion Research](Research/Component%20Study/README.md)
- [Stage 1 Verification Gates and Resource Map](Engineering%20Plan/stage1-verification-gates.md)
- [Pre-Purchase Verification Report](Research/Component%20Study/component-selection-2026/PREPURCHASE_VERIFICATION.md)

## Current Status

The Stage 1 catalog hardware selection is locked and consolidated into the
authoritative BOM. The repository also contains executable preliminary
analyses, pre-registered propulsion/vision gates, a verified Kakute H7 Mini
resource map, structured requirements, and a safety/FMEA baseline. It does
**not** yet contain purchased-and-weighed hardware, completed CAD, measured
bench data, or flight-test evidence.

Run the repository checks with:

```bash
python3 -m unittest discover -s Analysis/tests -v
```
