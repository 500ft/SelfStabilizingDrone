# Open Questions

Track unresolved design decisions here. Close each item with evidence rather than removing it silently.

| ID | Question | Decision Needed From | Required Evidence | Status |
|---|---|---|---|---|
| OQ-001 | What selected motor, propeller, and battery combination closes the recovery requirement? | Propulsion bench testing | Thrust/current/RPM curves across battery voltage | OPEN |
| OQ-002 | What is the frozen maximum flying mass? | CAD and BOM rollup | `roundup_to_5g(Sigma worst + 5 g)` and result `<=225 g` | OPEN |
| OQ-003 | Can batteries eventually be integrated into hollow frame members? | Later packaging study | Crash protection, thermal, serviceability, and abuse testing | DEFERRED |
| OQ-004 | Which NYU facility can provide motion-capture or high-speed video access? | Faculty/lab outreach | Confirmed equipment access and supervision | OPEN |
| OQ-005 | What gyro range and estimator envelope are reliable on the selected flight controller? | Flight-controller selection and test | Datasheet, firmware configuration, and external-truth comparison | OPEN |
| OQ-006 | What release heights are testable in the available enclosure? | Test-facility design | Cage dimensions and recovery simulation | OPEN |
