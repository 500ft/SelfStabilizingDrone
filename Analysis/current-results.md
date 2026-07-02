# Current Preliminary Results

Generated from the locked Stage 1 catalog selection on June 21, 2026. These are
not validated design results.

## Mass Budget

| Result | Value |
|---|---:|
| Best-case mass | 117.96 g |
| Nominal mass | 129.76 g |
| Worst-case mass | 149.5 g |
| Unmodeled-hardware allowance | 5.0 g |
| Proposed frozen maximum | 155.0 g |
| Nominal margin to proposed maximum | 25.24 g |
| Below 225 g abort threshold | PASS |

The `155 g` value is a proposal only. It cannot become the fixed maximum until
delivered components are weighed and the complete CAD mass model exists.

## Pre-Registered Component Gates

| Gate | Threshold | Status |
|---|---:|---|
| Full-reserve thrust at 7.0 V | 112.5 gf/motor | BENCH_REQUIRED |
| ESC unconditional current | <=10.4 A/motor | BENCH_REQUIRED |
| Battery unconditional current | <=44 A pack | BENCH_REQUIRED |
| Stage 1 Nicla p95 latency | <=100 ms | BENCH_REQUIRED |
| Future recovery Nicla p95 latency | <=50 ms | DEFERRED |
| Duplicate hardware resources | 0 | PASS (catalog map) |

## Preliminary Recovery Envelope

| Case | Minimum Height | Available Height | Testable Now |
|---|---:|---:|---|
| Best placeholder case | 0.88 m | 3.0 m | yes |
| Nominal placeholder case | 8.64 m | 3.0 m | no |
| Worst placeholder case | 58.42 m | 3.0 m | no |
| Nominal no-drag bound | 11.16 m | 3.0 m | no |

The model is first-order and uses estimated inertia, torque, thrust, latency, and drag. These results demonstrate why recovery cannot be assumed to work at low height. They do not predict the final vehicle.

## Guard Functional Check

All current placeholder guard cases fail the required clearance-to-deflection safety factor of `>=2`.

| Case | Predicted Deflection | Clearance SF | Elastic Stress SF | Functional Result |
|---|---:|---:|---:|---|
| Best placeholder case | 5.35 mm | 0.56 | 17.82 | FAIL |
| Nominal placeholder case | 10.54 mm | 0.24 | 7.50 | FAIL |
| Worst placeholder case | 20.00 mm | 0.10 | 4.00 | FAIL |

This does not prove a real guard will fail. It proves that the assumed stiffness and energy values do not close and must be replaced by analysis and test data.

## Classifier Confidence Bounds

| Observation | Exact 95% Upper Bound |
|---|---:|
| 0 false positives in 300 trials | 0.994% |
| 0 false positives in 1,000 trials | 0.299% |

An observation of zero is not reported as a true false-positive rate of zero.

## Closed-Loop Recovery Envelope (6-DoF, corrected 2026-07-02)

From `Analysis/run_release_recovery.py` (`Data/release_recovery_results.json`). The
envelope scan is capped at the gyro measurement range (2000 °/s): a release faster than
the gyro can report cannot be claimed recoverable regardless of the dynamics. Each edge
is labeled by what it actually is.

| Tier | Max recoverable tumble (60° tilt, 3 m budget) | Envelope edge |
|---|---:|---|
| Best | 34.5 rad/s (1977 °/s) | **gyro limit** (never failed up to sensor range) |
| Nominal | 3.5 rad/s (201 °/s) | real dynamic failure |
| Worst | 1.0 rad/s (57 °/s) | real dynamic failure |

The previously reported "best ≥ 40 rad/s" was the scan cap of the search loop — an
artifact, not a physical boundary — and exceeded the gyro range. Corrected.

## Monte Carlo Dispersion Sweep — GATE RESULT: FAIL at placeholder authority

From `Analysis/monte_carlo_recovery.py` (`Data/monte_carlo_results.json`). The validation
gates require recovery to hold "across a Monte Carlo sweep, not only a single
cherry-picked run." Dispersions per trial: mass ×[0.95, 1.10], inertia ×[0.85, 1.25],
torque ×[0.85, 1.10], thrust ×[0.85, 1.05], latencies ×[0.8, 1.5], battery sag ×[0.90, 1.00],
motor-mismatch torque bias ≤ 10% of budget, gyro noise 0.02 rad/s, attitude-estimate noise
2°, thrust-line (CG) offset uniform over a disk. Release: 60° tilt, nominal BOM tier.

| Scenario | 1.0 rad/s | 2.0 rad/s | 3.0 rad/s |
|---|---:|---:|---:|
| As-toleranced (cg ≤ 5 mm) | 3/75 (4.0%) | 6/150 (4.0%) | 1/75 (1.3%) |
| Balance-controlled (cg ≤ 1 mm) | 45/75 (60.0%) | 115/150 (76.7%) | 32/75 (42.7%) |

Success rates carry exact Clopper–Pearson 95% lower bounds in the JSON (same
zero-inflation-proof convention as the classifier stats above).

**Root cause.** The thrust-line-offset disturbance torque is `cg × thrust`. Against the
placeholder 0.004 N·m per-axis budget (EST-REC-007 — explicitly a placeholder,
"replace with measured thrust and arm length"):

| Thrust condition | CG offset that consumes 100% of budget | 50%-margin offset |
|---|---:|---:|
| Hover (1.27 N) | 3.15 mm | 1.57 mm |
| Recovery peak (4.2 N) | **0.95 mm** | 0.48 mm |

A thrust cap during righting does not rescue it: protecting torque margin trades directly
against the 3 m altitude budget and the vehicle hits the ground instead.

**What this means (requirement, not despair).** A real 4-motor mixer at this scale can
plausibly produce ~10× the placeholder differential torque, so the FAIL is most likely an
artifact of the conservative placeholder — but that is exactly the point: the claim is
unverifiable until measured. Derived actions:

1. **EST-REC-007 is the highest-value bench measurement in the project.** Measure
   per-motor thrust + arm length; the recovery-robustness story lives or dies on it.
2. **New build requirement:** thrust-line offset ≤ 0.5 mm (50%-margin at recovery thrust
   under the placeholder budget), to be verified from the Lane A+ CAD mass model and at
   assembly. Relax only after (1) demonstrates margin.
3. Until one of those lands, the single-point Lane A demo may be cited only alongside
   this gate result.
