# Guarded Micro-UAV Project

This repository documents a staged learning project for a protected micro-UAV that can eventually detect a toss/drop/release event, stabilize in midair, and follow a designated target.

The strongest current result is an honest hinge: the preregistered recovery
sweep **fails** with the 0.004 N·m placeholder authority but is predicted to
pass with a physically derived mixer. The deciding EST-REC-007 bench experiment
is frozen, executable, and **measurement pending**—not yet a validated flight or
recovery claim.

## Parts Reference for CAD / FEA

- **[Three-Tier Drone Parts PDF (cheapest / most expensive / most efficient)](Drone_Parts_Three_Tiers.pdf)** — single-file parts reference with masses, mounting geometry, and structural load cases to start CAD and FEA. Regenerate with `python3 "Research/Component Study/unrestricted-tier-study-2026/generate_parts_pdf.py"`.

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
- [Frozen Measured-Authority Gate](docs/specs/measured-authority-gate/design.md)
- [Propulsion-Bench Safety Checklist](Instrumentation/propulsion-bench-safety-checklist.md)
- [Pre-Purchase Verification Report](Research/Component%20Study/component-selection-2026/PREPURCHASE_VERIFICATION.md)
- [Three-Tier Architecture Decision (cheapest / capability ceiling / mission-optimal)](Research/Component%20Study/unrestricted-tier-study-2026/DECISION.md)
- [Weight-Unrestricted Component Research](Research/Component%20Study/unrestricted-tier-study-2026/report.md)

## Current Status

The Stage 1 catalog hardware selection is locked and consolidated into the
authoritative BOM. The repository also contains executable preliminary
analyses, pre-registered propulsion/vision gates, a verified Kakute H7 Mini
resource map, structured requirements, and a safety/FMEA baseline. It does
**not** yet contain purchased-and-weighed hardware, completed CAD, measured
bench data, or flight-test evidence.

Wave 2 remains blocked until the 7.0 V fifth-percentile authority is at least
0.020 N·m throughout 25–75% collective and the fixed 2 rad/s primary simulation
records at least 962/1,000 recoveries with an exact one-sided 95% lower bound
of at least 0.95 and maximum descent no greater than 3.0 m.

Run the repository checks with:

```bash
python3 -m unittest discover -s Analysis/tests -v
```

## License

This project is licensed under the [MIT License](LICENSE).
