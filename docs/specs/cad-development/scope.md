# SelfStabilizingDrone — amended CAD scope

2026-09-06. Owner placement decision pending: these ledgers are draft branch material, not approved for main. [Work orders](../../CAD_PLAN.md); [sole CAD status ledger](../../CAD_TASKS.csv).

## Must-have for the prioritized CAD package

- DR-CAD-01 — Prepare bench-first mechanical inputs and evidence mapping
- DR-CAD-02 — Approve bench-only geometry and access
- DR-CAD-10 — Establish code-CAD regeneration and CI geometry tests
- DR-CAD-06 — Model propulsion metrology stand and protective interfaces
- DR-CAD-08 — Release bench-only fabrication and calibration-review pack

## Nice-to-have

- Additional explanatory views only after numerical geometry verification and the release contract pass; not a parallel modeling lane.

## Maybe-later

- DR-CAD-02V — Approve vehicle-only mechanical interfaces. Trigger: Vehicle branch parked until bench decision and owner promotion.
- DR-CAD-03 — Model the full vehicle packaging assembly. Trigger: Vehicle work parked until measured authority supports proceeding and owner promotes this branch.
- DR-CAD-04 — Model guard attachments and analyze geometric load paths. Trigger: Vehicle work parked until measured authority supports proceeding and owner promotes this branch.
- DR-CAD-05 — Export CAD mass, CG and inertia with source provenance. Trigger: Vehicle work parked until measured authority supports proceeding and owner promotes this branch.
- DR-CAD-07 — Model mass-property verification fixture. Trigger: Vehicle work parked until measured authority supports proceeding and owner promotes this branch.
- DR-CAD-11 — Release vehicle and inertia-verification pack. Trigger: Vehicle branch parked until bench gate and owner promotion.
- DR-CAD-09 — Design a restrained release/synchronization fixture. Trigger: Vehicle work parked until measured authority supports proceeding and owner promotes this branch.

## Out

- Physical-test authorization, manufacture, certified performance and claims of independent validation from CAD alone.
- Main-branch planning-ledger publication without the owner placement decision.

## Milestone watch

- Bench torque at 7.0 V first. DR-CAD-01 → bench inputs DR-CAD-02 and tooling DR-CAD-10 → stand DR-CAD-06 → bench release DR-CAD-08. Vehicle inputs/packaging cannot gate that path.
- Check owner/research decision evidence before promotion; completion is not inferred from elapsed time.
- Check code-CAD environment/CI acceptance before closing parametric models.
- Check physical readiness and pre-load reference/uncertainty requirements independently of geometry export.
