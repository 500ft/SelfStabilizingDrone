# EST-REC-007 — Automated Gate Test Report

Status: **protocol and automated gates verified; physical measurement pending**.

Automated checks cover the 0.020 N·m band threshold, complete collective grid,
minimum repeat count, 4.2 N/60 mm mixer prediction, numerically stable exact
Clopper–Pearson bounds at n=1,000, the 962/1,000 success threshold, and the
3.0 m maximum-descent condition.

Run:

```bash
python3 -m unittest discover -s Analysis/tests -v
```

Measured results will be added without changing the registered thresholds.
