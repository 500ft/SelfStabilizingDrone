# EST-REC-007 — Automated Gate Test Report

Status: **software evidence-admission regression checked; physical measurement pending**.

Automated checks cover the 0.020 N·m band threshold, complete collective grid,
minimum repeat count, distinct six-motor coverage per grid, unique raw and
derived observations, finite/physical values, hashed source consistency,
declared calibration coverage, supplied uncertainty subtraction, synthetic
DEVELOPMENT_ONLY separation, 4.2 N/60 mm mixer prediction, numerically stable exact
Clopper–Pearson bounds at n=1,000, the 962/1,000 success threshold, and the
3.0 m maximum-descent condition.

Run:

```bash
python3 -m unittest discover -s Analysis/tests -v
```

Measured results will be added without changing the registered thresholds.

September 5 correction: the earlier tests did not establish the entire
measurement protocol. The original checker admitted infinite torque and lacked
calibration/identity/uncertainty evidence. The new checks validate supplied
bundle consistency, not calibration truth or authenticity. See the
[red/green record](../../../evidence/sprint-2026-09-05/verification.md),
[bounded developer evaluation](../../../evidence/sprint-2026-09-05/evaluation.md),
and [review index](../../REVIEW_READY.md).
