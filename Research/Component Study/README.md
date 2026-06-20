# Component and Propulsion Research

> **Stage 1 selection is locked (2026-06-20).** See [`component-selection-2026/STAGE1_BOM.md`](component-selection-2026/STAGE1_BOM.md) for the single recommended build (one part per subsystem, with the reason each was chosen and the option it beat), and [`component-selection-2026/Component_Selection_2026.xlsx`](component-selection-2026/Component_Selection_2026.xlsx) for the full ranked candidate lists (top 5–10 per category, sourced, with confirmed-vs-inferred tags). The autonomy fork is resolved to the **H7/F7 ArduPilot/PX4 research path**; FPV and GPS are deferred to Stage 2. Nominal flying mass ~130 g (vs 200 g target), T/W ≈ 3.75.

The [Drone Component and Propulsion Study](Drone_Component_and_Propulsion_Study.xlsx) is the first hardware-selection research package for the guarded micro-UAV.

It contains:

- a source-linked register of flight controllers, motors, propellers, batteries, vision boards, positioning sensors, and receivers;
- comparable small-drone benchmarks;
- a formula-driven motor-propeller-battery estimate study;
- a dedicated comparison of removable, semi-integrated, split-arm, and structural/frame-integrated battery architectures;
- assumptions, limitations, recommendations, and workbook verification checks.

## Current Engineering Conclusion

The first propulsion bench configuration should use a documented `EX1103 11000KV + 2023-3 + removable central 2S 550-650 mAh` combination. The modeled `450 mAh 75C` pack clears the static thrust-to-weight screen but fails the catalog full-load discharge-current screen. A frame-integrated battery should remain a later research track because distributed cells can increase rotational inertia and complicate charging, balancing, cooling, impact protection, inspection, and replacement.

The workbook is a screening model. Estimated thrust/current cases must not be used as proof of compliance until the exact hardware combination is tested on a thrust stand.
