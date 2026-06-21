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
