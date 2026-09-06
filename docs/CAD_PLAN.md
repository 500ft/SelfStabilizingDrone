# SelfStabilizingDrone — individual CAD tasks

Prepared 2026-09-06. **Planning only: no CAD model, drawing, fabrication, calibration or physical result was produced by this amendment.**

[CAD_TASKS.csv](CAD_TASKS.csv) is the sole status ledger for this new CAD phase. The earlier [SPRINT_TASKS.csv](SPRINT_TASKS.csv) remains the authority for the separate 30-hour evidence-integrity sprint; its estimates and achieved software evidence are unchanged. This plan expands mechanical work orders, not publication or test permission. Scope tiers are in [scope.md](specs/cad-development/scope.md).

## Verified reason for the work

The mass-property export is explicitly PENDING and the instrument plan requires pendulum validation. Bench safety names a stand, torque arm and guard but these lack individual design/release tasks.

Inspected source documents:

- [Engineering Data/cad_mass_properties_template.csv](../Engineering%20Data/cad_mass_properties_template.csv)
- [Engineering Data/hardware_interfaces.csv](../Engineering%20Data/hardware_interfaces.csv)
- [Instrumentation/README.md](../Instrumentation/README.md)
- [Instrumentation/propulsion-bench-safety-checklist.md](../Instrumentation/propulsion-bench-safety-checklist.md)

## Outcome and boundaries

A reviewer can reopen editable, version-pinned geometry; regenerate neutral STEP exports; understand the assembly, critical fits and measurement datums; and distinguish design assumptions from inspected hardware. STL is only a manufacturing derivative where appropriate, not the sole editable master. For hosted CAD retain a version-specific share reference and authorized portable source/export archive; record tool/version and export settings. Do not require a particular commercial tool before checking access.

**Entry decision:** Owner confirms the actual four-motor vehicle, component interfaces, fabrication capability and bench/instrument envelope; later drop-fixture work requires separate readiness approval.

**Excluded:** No motor operation, drop tests, purchases or flight release. Six test motors are a sampling requirement, not a six-motor airframe. Do not import the original checkout's untracked Onshape export without owner reconciliation.

Agent owns document preparation and modeling once inputs exist; Owner owns actual component/access choices and review authority; External fabricators/operators own quotes, manufacture and facility approval. No approval, purchase, fabrication booking, IP disclosure of third-party drawings, or test run is completed by checking in this plan. Unknown critical dimensions block fabrication; conceptual placeholders must be visible and cannot become as-built evidence.

## Focused-hour allocation

The initial CAD phase is **28 estimated focused hours**, additional to the earlier software sprint. A further **5 hours** is deferred behind explicit triggers. These are estimates, not recorded work. Each day is a workload bucket after its prerequisites, not a calendar promise; quotes, calibration and facility lead times are not compressed into CAD hours.

| Workload day | Hours | Ordered tasks |
| --- | ---: | --- |
| 1 | 4 | DR-CAD-01 → DR-CAD-02 |
| 2 | 6 | DR-CAD-03 |
| 3 | 4 | DR-CAD-04 |
| 4 | 3 | DR-CAD-05 |
| 5 | 5 | DR-CAD-06 |
| 6 | 6 | DR-CAD-07 → DR-CAD-08 |

Critical path follows the explicit task dependencies below: input register → owner decisions → parts/fixtures → release review. Independent branches may proceed after their shared inputs close.

## Individual work orders

All output paths below are **proposed NEW deliverables**, not existing artifacts. Current task state appears only in the CSV; the headings below define acceptance, not completion.

### DR-CAD-01 — Create mechanical interface and coordinate-frame register

- Owner: Agent; priority: P1; estimate: 2 h; workload day: 1.
- Dependencies: none; source inspection is available now.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/vehicle/interfaces.csv; cad/vehicle/design-inputs.md`.
- Done when: Trace selected components to hardware_interfaces.csv and requirements; list mounting patterns, motor centers, prop sweep, battery restraint and common body axes. Unknown dimensions and masses remain pending, not guessed release inputs.
- Verification and evidence to retain: Cross-check every component against the existing engineering tables and mass-property template; retain source and units per input.

### DR-CAD-02 — Approve actual component and bench geometry inputs

- Owner: Owner; priority: P1; estimate: 2 h; workload day: 1.
- Dependencies: DR-CAD-01.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/vehicle/owner-inputs.md`.
- Done when: Supply fit-critical drawings or measurements for motor, props, electronics, battery, load cell and stand, fabrication method and limits. Reconcile any existing Onshape model and define reuse authority; identify qualified bench reviewer.
- Verification and evidence to retain: Record actual part revisions, reviewed envelope and access decisions. Missing dimensions keep downstream fabrication blocked.

### DR-CAD-03 — Model the full vehicle packaging assembly

- Owner: Agent; priority: P1; estimate: 6 h; workload day: 2.
- Dependencies: DR-CAD-02.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/vehicle/assembly/ (editable source, STEP, layout drawing)`.
- Done when: Model motor mounts, frame, electronics/battery retention, connector service space and wire routing using sourced envelopes. Assign mass basis per part; model all four rotor swept envelopes and retained fasteners.
- Verification and evidence to retain: Retain interference report, top/side/section views and service-access checks at the documented configuration.

### DR-CAD-04 — Model guard attachments and analyze geometric load paths

- Owner: Agent; priority: P1; estimate: 4 h; workload day: 3.
- Dependencies: DR-CAD-03.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/vehicle/guard/ (source, STEP, load-path drawing)`.
- Done when: Detail attachment interfaces, joints and minimum prop clearance over declared tolerance/deflection assumptions; distinguish contact guard from blade-fragment containment. Do not claim a CAD guard is impact-qualified.
- Verification and evidence to retain: Inspect worst-case fit and removal/access; link load paths to Analysis/guard.py assumptions and log mismatches for later analysis.

### DR-CAD-05 — Export CAD mass, CG and inertia with source provenance

- Owner: Agent; priority: P1; estimate: 3 h; workload day: 4.
- Dependencies: DR-CAD-03, DR-CAD-04.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/vehicle/mass-properties.csv; cad/vehicle/mass-reconciliation.md`.
- Done when: Use the existing Engineering Data/cad_mass_properties_template.csv columns; document inertia frame, origin, units, products-of-inertia convention, density/source and uncertain bought-part masses. Keep modeled values separate from measured values.
- Verification and evidence to retain: Reconcile component sums with assembly mass; verify frame translations and symmetric/positive inertia; compare current mass budget without silently overwriting assumed inputs.

### DR-CAD-06 — Model propulsion metrology stand and protective interfaces

- Owner: Agent; priority: P1; estimate: 5 h; workload day: 5.
- Dependencies: DR-CAD-02.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/bench/propulsion/ (source, STEP, drawings)`.
- Done when: Specify load-cell mounts, thrust axis, calibrated torque-arm lever, hard mounting/ballast, cable restraint, remote stop access and independent containment interface. Document nominal applied loads and stability calculations; qualified containment is an external input, not a printed-shell claim.
- Verification and evidence to retain: Review calibration-load path, tip-over/sliding/fastener assumptions and prop exclusion envelope against the existing safety checklist. Retain review issues; no energized approval implied.

### DR-CAD-07 — Model mass-property verification fixture

- Owner: Agent; priority: P1; estimate: 3 h; workload day: 6.
- Dependencies: DR-CAD-02, DR-CAD-05.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/bench/pendulum/ (source, STEP, datums)`.
- Done when: Define bifilar or trifilar suspension attachment, spacing, suspension-length measurement, body-frame alignment and securing points for a props-off vehicle. Include fixture inertia/tare identification in the measurement plan.
- Verification and evidence to retain: Check support loads and unobstructed small-angle motion; retain dimensioned datums and fixture contribution calculation before an approved calibration run.

### DR-CAD-08 — Release vehicle and bench manufacturing-review pack

- Owner: Agent; priority: P1; estimate: 3 h; workload day: 6.
- Dependencies: DR-CAD-04, DR-CAD-05, DR-CAD-06, DR-CAD-07.
- Scope: initial CAD phase, subject to its input/owner gate.
- Proposed deliverables: `cad/release/ (BOM, drawings, source/export manifest, inspection plan)`.
- Done when: Include vehicle/bench revisions, material/process and critical fits, assembly/exploded views and inspection checks. List mass-property physical validation and safety approval as unresolved until observed; preserve 0.020 N m and 962/1000 gates.
- Verification and evidence to retain: Reopen neutral exports, compare selected dimensions and mass against native source; review every critical interface and hardware-data dependency.

### DR-CAD-09 — Design a restrained release/synchronization fixture

- Owner: Agent; priority: P2; estimate: 5 h; workload day: conditional.
- Dependencies: DR-CAD-08.
- Scope: trigger-gated extension; not required for initial CAD release.
- Proposed deliverables: `cad/bench/release-fixture/ (source and reviewed concept drawing)`.
- Done when: Only after qualified operator approves a bounded recovery campaign and measured propulsion readiness exists: define restraint, release clearance and common trigger/visible-LED mounts. No free-flight claim or test authorization from CAD.
- Verification and evidence to retain: Review prop/vehicle trajectory envelope and release-failure modes with the facility; record approval separately from geometry.

## Release review and overrun rule

Every release includes an assembly/exploded view, a critical section/detail view and a measurement/inspection setup view. Captions identify the question illustrated, source revision, dimensions/units and **CAD prediction—not measured** state; cite vendor/hand-calculation references actually used. Render quality is not evidence of fit or performance.

Before marking a CAD task done, attach real source/export identities, regeneration instructions and the corresponding acceptance evidence in CAD_TASKS.csv. A second AI pass is a development check, not independent human or laboratory validation. Retain failed fits and unresolved assumptions; do not silently tune experimental geometry after observing confirmation data.

If the phase overruns, postpone decorative renders, optional variants and mechanism extensions first. Do not remove required fits, safety interfaces, reference controls, source traceability or measurement access. Fabrication-release review, apparatus commissioning and physical evaluation remain separate future actions; updated geometry may require a new prospective analysis/reference freeze. Preparing drawings does not close an existing physical-readiness or publication blocker.

## PR review scope

This amendment changes task planning and navigation only. It is stacked on the open evidence-integrity PR so its diff excludes earlier fixes. No software behavior or frozen scientific threshold is changed. Review task dependencies and claim boundaries now; actual CAD acceptance is assessed when those artifacts exist.
