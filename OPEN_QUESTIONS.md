# Open Questions

Track unresolved design decisions here. Close each item with evidence rather than removing it silently.

| ID | Question | Decision Needed From | Required Evidence | Status |
|---|---|---|---|---|
| OQ-001 | Does the locked propulsion set (EX1103 11000KV / Gemfan 2023-3 / GNB 2S 550 mAh) meet thrust reserve on the bench? | Propulsion bench testing | Thrust/current/RPM curves at 8.4/7.6/7.0 V; >=112.5 gf/motor at 7.0 V for full 225 g reserve | OPEN (catalog selection LOCKED 2026-06-20; performance bench-gated) |
| OQ-002 | What is the frozen maximum flying mass? | CAD and BOM rollup | `roundup_to_5g(Sigma worst + 5 g)` and result `<=225 g` | OPEN (primary response to a propulsion miss is mass freeze, not a prop change) |
| OQ-003 | Can batteries eventually be integrated into hollow frame members? | Later packaging study | Crash protection, thermal, serviceability, and abuse testing | DEFERRED |
| OQ-004 | Which NYU facility can provide motion-capture or high-speed video access? | Faculty/lab outreach | Confirmed equipment access and supervision | OPEN |
| OQ-005 | What gyro range and estimator envelope are reliable on the Holybro Kakute H7 Mini (ArduPilot)? | Bench + flight test on locked FC | Kakute IMU datasheet, ArduPilot EKF3 config, and external-truth comparison | OPEN (FC locked: Kakute H7 Mini) |
| OQ-006 | What release heights are testable in the available enclosure? | Test-facility design | Cage dimensions and recovery simulation | OPEN |

## Milestone Schedule

Target dates are placeholders until the student fills them in against their actual semester schedule.

| Milestone | Target Date | Status |
|---|---|---|
| Mass freeze | TBD | Not started |
| Manual hover test | TBD | Not started |
| Classifier dataset collection | TBD | Not started |
| Release-rig test | TBD | Not started |
| Powered recovery test | TBD | Not started |
