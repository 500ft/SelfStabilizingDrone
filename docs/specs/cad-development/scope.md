# SelfStabilizingDrone — CAD adaptive scope

Date: 2026-09-06. Task definitions: [CAD_PLAN.md](../../CAD_PLAN.md); authoritative CAD state: [CAD_TASKS.csv](../../CAD_TASKS.csv).

## Must-have for the initial CAD deliverable

- DR-CAD-01: Create mechanical interface and coordinate-frame register.
- DR-CAD-02: Approve actual component and bench geometry inputs.
- DR-CAD-03: Model the full vehicle packaging assembly.
- DR-CAD-04: Model guard attachments and analyze geometric load paths.
- DR-CAD-05: Export CAD mass, CG and inertia with source provenance.
- DR-CAD-06: Model propulsion metrology stand and protective interfaces.
- DR-CAD-07: Model mass-property verification fixture.
- DR-CAD-08: Release vehicle and bench manufacturing-review pack.

“Must-have” applies only to this CAD package, not every paper or software milestone. Entry decision: Owner confirms the actual four-motor vehicle, component interfaces, fabrication capability and bench/instrument envelope; later drop-fixture work requires separate readiness approval.

## Nice-to-have after the package

- Additional presentation renders or animation, only after source/STEP/drawing reproduction succeeds; they add explanation, not test evidence.

## Maybe-later

- DR-CAD-09: Design a restrained release/synchronization fixture. Trigger and acceptance: Only after qualified operator approves a bounded recovery campaign and measured propulsion readiness exists: define restraint, release clearance and common trigger/visible-LED mounts. No free-flight claim or test authorization from CAD. Why wait: avoid detailed hardware work before its scientific and resource gate closes.

## Out

- No motor operation, drop tests, purchases or flight release. Six test motors are a sampling requirement, not a six-motor airframe. Do not import the original checkout's untracked Onshape export without owner reconciliation.

## Milestone watch

- Check owner-input records before moving from a parameterized concept to released fits.
- Check the CAD_TASKS.csv predecessor IDs and linked acceptance evidence before starting dependent geometry.
- Check source/export regeneration and inspection drawings before a fabrication-review decision.
- Check qualified apparatus/measurement approval separately before any physical claim or energized run.
