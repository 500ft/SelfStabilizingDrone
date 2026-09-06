# SelfStabilizingDrone — evidence-integrity sprint

Prepared 2026-09-05. Budget: six workload days, 30 focused hours (27 Agent + 3 Owner); no unattended execution. This sprint repairs software admission of measurement evidence, not the vehicle.

## A. Outcome and baseline

Reviewer-reproducible measured-authority admission checks with conservative uncertainty handling, explicit six-motor source coverage, and honest simulation claims. No physical authority/recovery verdict is promised.

Publication-state update (2026-09-06): the owner authorized local commits, branch
pushes, and pull requests for this sprint. This does not authorize deployment,
research publication, outreach, spending, or any blocked physical/data action.

- Canonical implementation checkout: `/Users/redhose/Developer/research-sprints/2026-09-05/SelfStabilizingDrone`.
- Remote: `https://github.com/500ft/SelfStabilizingDrone.git`.
- Branch: `sprint/evidence-integrity-20260905`.
- Base: `45da9be1a9647ce39ae18e3ea2494d965ee827e8`; initially clean.
- Original owner checkout remains untouched. This isolated checkout is deliberate.
- Python 3.11.8; requirements are `numpy==2.1.1`, `matplotlib>=3.8`.
- CI command: `python -m unittest discover -s Analysis/tests -v`, from repository root.
- No configured typechecker, linter, or distributable build. Use compile checks, focused/full unittest, and real CLI invocations; do not imply the missing gates ran.
- Selected logs: [baseline](../evidence/sprint-2026-09-05/baseline.md). Task status lives only in [SPRINT_TASKS.csv](SPRINT_TASKS.csv).

## B. Evidence-backed starting gaps

**Reproduced failure:** 30 rows of positive-infinite torque return PASS at base. Full input and output are in baseline evidence. The same checker has no sample/motor identities, calibration artifact, or uncertainty field.

**Verified contract:** [frozen design](specs/measured-authority-gate/design.md) demands all six sampled motors, complete collective grid, calibration, uncertainty, and traceable raw telemetry. They characterize a four-motor craft; six is the sampled motor count, not airframe motor count.

**Verified mismatch:** [Scenario C](../Analysis/current-results.md) changes mixer authority AND control behavior; the 4%→100% contrast is not an isolated authority intervention.

**Reported, not measured:** no bench dataset or flight validation is supplied. Six-point empirical fifth percentile is the sample minimum, not a confidence-qualified population limit. Do not alter 0.020 N·m or the independent 962/1,000 recovery requirement.

Baseline checks are recorded with actual completion status in evidence; a running process is not a pass.

## C. Scope, ownership, and critical path

Must-haves: fail-closed numeric validation; unique sample/raw-source identities; six-motor coverage at each registered grid point; explicit calibrated uncertainty input and source artifact checks; synthetic-labeled fixtures unable to authorize hardware progression; regression/CLI evidence; accurate claim boundaries; review packet. Evidence labels and review metadata are supplied assertions, not proof of authenticity.

Authority reduction will remain a derived-data interface: the checker can validate provenance/coverage and apply supplied expanded uncertainty, but cannot certify calibration quality or recreate an unprovided thrust-to-mixer derivation. Missing evidence is INCONCLUSIVE, not FAIL or PASS.

Agent owns implementation/tests/docs. Owner supplies the six-motor roster, measured-data availability, calibration/uncertainty review, and facility/operator readiness. External facility/operator approval and actual measurements have unknown lead time and are outside 30 hours. Preparation does not imply outreach, purchases, reservations, or approval.

Critical path: baseline → failing regression → validated evidence contract + correction → CLI delivery → frozen software candidate / bounded developer verification → review packet. Owner confirmation runs in parallel; its absence blocks a physical verdict, not synthetic software verification.

Excluded: flight, purchases, propulsion operation, firmware/controller retuning, new Monte Carlo result claims, broad vehicle redesign, statistical population guarantees, publication/deployment/push.

## D. Six-day allocation

| Day | Hours | Primary deliverable |
|---|---:|---|
| 1 | 5 | Baseline/reproduction and owner evidence intake checklist |
| 2 | 5 | Finite, physical, unique measurement admission |
| 3 | 6 | Traceability/uncertainty integration and corrected claims |
| 4 | 4 | CLI consumer route and documentation |
| 5 | 6 | Frozen candidate and bounded adversarial verification |
| 6 | 4 | Reviewer packet and owner feedback or explicit pending state |
| Total | 30 | 27 Agent + 3 Owner hours |

Day numbers are workload groupings, not elapsed-time promises. Optional Day 7: up to 4 additional Agent hours for defect repair/review only; not preauthorized hardware work.

## E. Ordered work and acceptance

### Day 1 — DR-S01 (P0, Agent, 3h); DR-S02 (P0, Owner, 2h)
Prerequisites: accessible checkout and Python. Inspect `Analysis/measured_authority_gate.py`, `Analysis/tests/test_measured_authority_gate.py`, `.github/workflows/ci.yml`, `requirements.txt`, and `docs/specs/measured-authority-gate/{design,plan,test-report}.md`.

S01 deliverable: baseline identity, full-suite exit/output, and exact positive-infinity reproduction, plus **new** sprint records/evidence. Verify with CI command and reproduced 30-row input in baseline.md.
S02 deliverable: completed **new** `docs/specs/measured-authority-gate/evidence-intake.md` owner fields: motor roster, measurement availability, calibration/uncertainty reviewer, safety/facility state. No messages sent or equipment operated.
Done when software baseline is recorded and owner answers are received or explicitly pending. S01 does not depend on S02.

### Day 2 — DR-S03 (P0, Agent, 5h)
Depends S01. Change `Analysis/measured_authority_gate.py` and `Analysis/tests/test_measured_authority_gate.py`.
Regression first: nonfinite voltage/collective/torque, negative authority, empty/missing grid, duplicate samples and raw observations, single motor repeated six times. Deliverable: fail-closed admission, preserving thresholds and returning a non-successful evidence state for incomplete inputs.
Verify: `python -m unittest Analysis.tests.test_measured_authority_gate -v`; retain red and green outputs. Done when original defect is reproduced by the regression and corrected without accepting counterexamples.

### Day 3 — DR-S04 (P0, Agent, 4h); DR-S05 (P1, Agent, 2h)
S04 depends S03. Existing gate/test/design files; **new** evidence contract example/schema documentation under `docs/specs/measured-authority-gate/`. Establish required manifest/raw-record references, source hashes, motor identities, calibration/derivation/uncertainty artifacts, explicit evidence kind, and uncertainty-adjusted lower authority per grid.
Acceptance: omission, tampering, missing motor, duplicate observation, and uncertainty crossing 0.020 are tested; synthetic fixture is never a physical PASS. Label empirical quantile honestly.
S05 depends S01. Update `README.md`, `Analysis/current-results.md`, and spec/test-report wording: Scenario C includes controller changes; direct static measurement is not dynamic recovery validation.
Verify targeted unittest and source inspection. Done when evidence format and claims agree, with owner judgment clearly separated from software checks.

### Day 4 — DR-S06 (P0, Agent, 4h)
Depends S04/S05. Existing CLI/gate tests and `docs/data-and-figures.md`; **new** selected CLI evidence in sprint directory.
Deliverable: actual command-line CSV+manifest ingestion, strict JSON output, meaningful nonzero invalid/inconclusive status; traceable input hashes and command captures.
Verify `python -m Analysis.measured_authority_gate --help` and generated temporary synthetic CSV/manifest via subprocess regression. No real measured CSV exists; do not provide a fabricated measured command example. Done when consumer invocation reproduces software acceptance/rejection and documentation names prerequisites.

### Day 5 — DR-S07 (P0, Agent, 6h)
Depends S06. **New** `evidence/sprint-2026-09-05/evaluation.md`: record candidate file hashes and a predeclared boundary matrix before additional outputs. Cases: finite threshold boundaries, voltage/grid tolerance, six distinct motor coverage, uncertainty subtraction, missing/tampered evidence, synthetic versus measured labels.
This is developer adversarial testing, not independent held-out validation: audit inputs and synthetic fixtures informed development. Cases that trigger fixes stay development material; record any revised candidate.
Verify full CI suite and CLI counterexamples. Done when expected judgments, observed behavior, discrepancies, limits, and final hashes are retained. No accuracy or physical safety claim follows.

### Day 6 — DR-S08 (P0, Agent, 3h); DR-S09 (P1, Owner, 1h)
S08 depends S07; S09 depends S08 and Owner availability.
Deliverable: **new** `docs/REVIEW_READY.md` with base/candidate status, scope, evidence links, regressions, CLI changes, incomplete work, and at most three remaining problems. Final `git diff --check`, compile and unittest gates; no commit/push in this sprint without parent authorization.
Owner inspects contract/data feasibility and responds or remains explicitly pending. Done when another reviewer can reproduce all software claims and the handoff is explicitly partial if owner/physical requirements remain open.

## F. Overrun and review rules

Cut extra simulation studies and aesthetic changes first. Do not cut fail-closed input checks, traceability, the frozen numbers, or measured/synthetic separation. If the manifest derivation needs unresolved physical assumptions, keep the verdict INCONCLUSIVE and report the missing specification. External measurement/safety work is not compressed into remaining hours.

Success establishes software contract enforcement, not authentic data, population confidence, flight readiness, or vendor performance. An independent reviewer should try forged/missing metadata, inspect the source-to-derived mapping, and rerun the CLI from a clean checkout. Parent independently reruns tests before adopting changes.

## G. First action

Record the current full-suite outcome, then write the positive-infinity regression before changing behavior. Resume from [task ledger](SPRINT_TASKS.csv) and [progress log](SPRINT_PROGRESS.md).
