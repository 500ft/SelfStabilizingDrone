# SelfStabilizingDrone — CAD item list

Prepared 2026-09-06 (America/New_York). **A list of planned parts and assemblies—not completed CAD, hardware or approval to fabricate/test.**

Design the propulsion measurement bench first, after bench-only input confirmation. Vehicle packaging is a separate later branch; it must not delay the 7.0 V torque/authority measurement.

## How to use this list

This is a parts inventory, not another task-status ledger or additional scope/budget. Each row maps to the [existing work-order definitions](https://github.com/500ft/SelfStabilizingDrone/blob/7e36971b67c9a3c47b203ebe7d9c0d33c94947f8/docs/CAD_PLAN.md) and [their task ledger](https://github.com/500ft/SelfStabilizingDrone/blob/7e36971b67c9a3c47b203ebe7d9c0d33c94947f8/docs/CAD_TASKS.csv); several parts can belong to one work order. Bought parts and existing models should be reused/imported when authorized, not redesigned merely to fill a CAD folder. One part may serve multiple listed interfaces; avoid duplicating it.

## First modeling package: propulsion bench

| Item to model or import | Existing work order | Purpose / boundary |
| --- | --- | --- |
| Motor test mount / interchangeable adapter | `DR-CAD-06` | Fit the selected motor and its actual mounting pattern; establish the thrust axis. |
| Load-cell bracket and load-transfer connection | `DR-CAD-06` | Define the measured force path and alignment to the calibrated load cell. |
| Stand base, anchoring and calibration-arm interface | `DR-CAD-06` | Show bench attachment, stability/load path and lever datums. The stand calibration lever is not automatically the effective vehicle arm_m. |
| Cable restraints and containment/stop-access interfaces | `DR-CAD-06` | Show safe routing, approved containment attachment and remote-stop access. This is an interface to qualified containment, not a claim that a CAD shell contains blade fragments. |
| Complete thrust/torque stand assembly | `DR-CAD-08` | Provide an assembled view, fit-critical drawings and the mapping to thrust_n/arm_m measurements. |

## Later: only after the authority decision supports the vehicle branch

| Item to model or import | Existing work order | Purpose / boundary |
| --- | --- | --- |
| Vehicle frame and motor mounts | `DR-CAD-03` | Create the four-motor assembly and rotor swept envelopes using sourced component dimensions. |
| Battery restraint and electronics mounts | `DR-CAD-03` | Model retention, wiring/connector clearance and service access. |
| Propeller guard and frame attachments | `DR-CAD-04` | Model joints, load paths and clearances; impact/containment capability remains untested. |
| Full vehicle assembly for mass/CG/inertia export | `DR-CAD-05` | Assign sourced masses/materials and record body axes; this is an assembled configuration, not a separate fabricated part. |
| Bifilar/trifilar pendulum mounting fixture | `DR-CAD-07` | Provide props-off suspension attachment, measured spacing and fixture-tare datums. |
| Restrained release and synchronization fixture | `DR-CAD-09` | Only for a separately approved recovery campaign: show restraint/release and visible-trigger mounting interfaces. |

## What to deliver for each applicable part or assembly

- Editable/source CAD or an authorized immutable CAD-document version; identify reused vendor geometry and its source.
- STEP export, with dimensions/units checked after reimport. Parameter-driven families also need the planned numerical geometry tests before model acceptance.
- A dimensioned drawing for custom fabricated parts, with material/process, critical fits and inspection datums; vendor hardware can use its sourced drawing.
- An assembly/section view showing how the part fits and which problem it addresses. Label all visuals CAD/design-only until corresponding evidence exists.

Use actual vendor drawings or measurements for mounting patterns; the electrical UART/pad map is not mechanical geometry. Unknown dimensions block release. These parts do not authorize motor operation or flight.

## Policy and scope

This checklist-only PR does not copy the pending CAD planning ledgers onto main. The cited work orders live at their existing public commit; linking them does not turn a public branch into private storage. No withheld details are restored, no model task is marked done and no hardware/fabrication/disclosure gate is closed by adding this list.
