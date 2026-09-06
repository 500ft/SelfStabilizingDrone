# Baseline — 2026-09-05

Working directory: `/Users/redhose/Developer/research-sprints/2026-09-05/SelfStabilizingDrone`.
Remote: https://github.com/500ft/SelfStabilizingDrone.git
Branch: `sprint/evidence-integrity-20260905`.
Commit: `45da9be1a9647ce39ae18e3ea2494d965ee827e8`.
Initial worktree: clean.
Runtime observed: `Python 3.11.8`.
Source configuration: `.github/workflows/ci.yml`, `requirements.txt`.

## Full suite

Command: `python -m unittest discover -s Analysis/tests -v`.
Exit 0. Actual final output:
```text
----------------------------------------------------------------------
Ran 69 tests in 119.355s

OK
```
All 69 named tests emitted `ok`; the selected retained output is the final summary.
Installed versions observed separately: NumPy 2.1.1; Matplotlib 3.10.1.

## Audit reproduction — complete input

Command (from repository root):

```bash
python -c 'from Analysis.measured_authority_gate import COLLECTIVE_GRID,evaluate_rows; data=[{"voltage_v":7.0,"collective_fraction":point,"tau_rp_n_m":float("inf")} for point in COLLECTIVE_GRID for _ in range(6)]; print(evaluate_rows(data))'
```

Exit 0. Actual verdict excerpt:
```text
AuthorityVerdict(classification='PASS', threshold_n_m=0.02, conservative_minimum_n_m=inf, voltage_v=7.0, ... reasons=['fifth-percentile authority clears 0.020 N m at every grid point'])
```
The omitted point list contains exactly five points, each samples=6 and fifth_percentile_tau_n_m=inf. No source data, motor identifier, calibration, or uncertainty was supplied. Input is synthetic and deliberately invalid; this result is not a propulsion observation.

## Gate coverage limits

CI uses unittest only. No configured typecheck, lint, or distributable package build was found. Dependencies were already available; no installation, hardware tests, flight, or external service invocation was needed.
