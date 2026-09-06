# Measured-authority evidence contract v1

Admission format added 2026-09-05 to enforce existing frozen requirements. No real bench bundle is committed. This document specifies inputs; it is not a populated measurement record.

## Bundle and derived CSV

Place the manifest and its artifacts together; artifact paths are relative to the manifest directory and cannot escape it. The CLI accepts:

```text
python -m Analysis.measured_authority_gate DERIVED_CSV --manifest MANIFEST_JSON --output VERDICT_JSON
```

Uppercase arguments are explicit placeholders: use real reviewed file paths. The runnable synthetic consumer check is:
```bash
python -m unittest Analysis.tests.test_measured_authority_gate.EvidenceContractTests.test_cli_is_strict_json_and_nonzero_for_missing_or_synthetic_evidence -v
```

Required derived columns:
`sample_id,raw_record_id,motor_id,voltage_v,collective_fraction,tau_rp_n_m,expanded_uncertainty_n_m`.

One unique sample and one unique raw observation per derived row. Reusing a raw observation under a new sample ID is rejected. Six distinct roster motors must occur at **each** accepted grid point. This is a traceability convention for the minimum symmetric four-motor authority derivation from per-motor bench curves, not a general mixed-motor combinatorial uncertainty pipeline. A different derived-sample construction needs an explicit reviewed format extension; do not relabel one observation as several motors.

The `tau_rp_n_m` column contains nominal derived authority, not an already uncertainty-reduced value. The checker subtracts supplied nonnegative expanded uncertainty **once**, clamps at zero, and evaluates the empirical fifth percentile. Missing or nonfinite values are never zero-filled.

Required raw CSV columns:
`record_id,motor_id,voltage_v,collective_fraction,thrust_n,current_a,temperature_c,rpm,time_s,arm_m,calibration_id`.

Raw IDs are unique. Motor, voltage, collective, and calibration identity must agree with the derived row/manifest; raw numeric telemetry must be finite and physically signed. The derivation artifact explains how raw curves, geometry, and motor variation produce authority. The code does **not** recompute the mixer derivation or prove thermal/transient representativeness.

## Manifest fields

| Field | Required value |
|---|---|
| `schema_version` | Integer 1 |
| `evidence_kind` | `measured` or `synthetic` |
| `motor_ids` | Six distinct nonempty identifiers |
| `calibration_id` | Identifier matching raw records |
| `calibration_quantities` | List covering thrust_n, voltage_v, current_a, temperature_c, rpm, time_s, arm_m |
| `review` | Object: status=`accepted`, nonempty reviewer, reviewed_on=`YYYY-MM-DD` |
| `artifacts` | Five objects keyed derived, raw, calibration, uncertainty, derivation |
| Each artifact | Relative `path` and exact lowercase `sha256` of nonempty file |

The reviewed calibration artifact must document instrument/reference/procedure/raw/fitted/residual/operator/date information from [Instrumentation](../../../Instrumentation/README.md). The uncertainty artifact must record coverage factor/assumptions, calibration and motor-variation contributions, correlations, and applicability. The derivation must state motor selection/repeats and operating envelope before evaluation. The software checks presence/hashes/declared coverage, not the truth or adequacy of these statements. Review strings are not signatures.

## Result and compatibility

CLI exit: PASS=0; completed numerical FAIL on measured-labeled evidence=1; invalid/incomplete evidence INCONCLUSIVE=2; synthetic DEVELOPMENT_ONLY=3. Verdict JSON disallows NaN/Infinity. For a valid synthetic bundle, `numerical_result` is PASS/FAIL but classification never authorizes hardware. API: `evaluate_rows(rows, evidence_path=Path(...))`; the rows must exactly correspond to the hashed derived artifact after CSV string serialization. The old three-column-only API now returns INCONCLUSIVE.

Output retains `conservative_minimum_n_m` for compatibility, meaning the minimum **empirical uncertainty-adjusted** grid quantile. It is not a population confidence bound. Each point records sampled motor IDs; output identifies the manifest hash and static-only scope.

Measured-labeled fixtures in unit tests exercise a software branch only. A malicious or mistaken person can assert a false review or evidence_kind; these checks are consistency checks, not a trust authority. A real reviewer must inspect underlying evidence. Flight remains blocked.
