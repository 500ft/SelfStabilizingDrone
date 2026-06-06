# Current Preliminary Results

Generated from planning estimates on June 6, 2026. These are not validated design results.

## Mass Budget

| Result | Value |
|---|---:|
| Best-case mass | 106.5 g |
| Nominal mass | 140.75 g |
| Worst-case mass | 175.0 g |
| Unmodeled-hardware allowance | 5.0 g |
| Proposed frozen maximum | 180.0 g |
| Nominal margin to proposed maximum | 39.25 g |
| Below 225 g abort threshold | PASS |

The `180 g` value is a proposal only. It cannot become the fixed maximum until real component choices and the complete CAD mass model exist.

## Preliminary Recovery Envelope

| Case | Minimum Height | Available Height | Testable Now |
|---|---:|---:|---|
| Best placeholder case | 0.86 m | 3.0 m | yes |
| Nominal placeholder case | 9.02 m | 3.0 m | no |
| Worst placeholder case | 66.04 m | 3.0 m | no |
| Nominal no-drag bound | 11.66 m | 3.0 m | no |

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
