# Candidate evaluation — developer scenarios, not physical validation

Selection frozen before running the additional CLI scenario script on 2026-09-05.
Candidate gate SHA256: `d8de05fc5c239190f648323a681f934d5b286f9cc4fce3090b2822e3ecf0068e`.
Focused test SHA256: `38ebd73ada2a5a842b5adbcb7aea76c732f36653d8d5f7651b9f66730d05ba8e`.
Source base: `45da9be1a9647ce39ae18e3ea2494d965ee827e8`; changes uncommitted.

This is a bounded developer check. The audit, regression cases and helper generator informed development. No checksum or extra process makes these independent human/hardware data. Some stress cases are additional input combinations not previously executed against this candidate; none establish general accuracy or authenticity.

## Predeclared judgments

All records are generated synthetic fixtures, including the deliberately measured-labeled branch-coverage case.

| Case | Expected classification | Exit | Numerical result |
|---|---|---:|---|
| nominal synthetic | DEVELOPMENT_ONLY | 3 | PASS |
| below-threshold synthetic | DEVELOPMENT_ONLY | 3 | FAIL |
| missing calibration file | INCONCLUSIVE | 2 | null |
| reused raw observation | INCONCLUSIVE | 2 | null |
| missing uncertainty | INCONCLUSIVE | 2 | null |
| raw operating-point mismatch with updated hash | INCONCLUSIVE | 2 | null |
| malformed manifest array | INCONCLUSIVE | 2 | null |
| measured-label branch on synthetic records | PASS | 0 | PASS |
| empty derived file with matching hash | INCONCLUSIVE | 2 | null |
| 8.4 V reference rows only | INCONCLUSIVE | 2 | null |

The measured-label case documents a boundary, not a security success: humans can falsely label inputs measured. Metadata is not authentication, and the checker does not infer truth from hashes. Actual measured classification must be reviewed against physical source data.

Reproduce from repository root:
```bash
python evidence/sprint-2026-09-05/evaluate_candidate.py --output evidence/sprint-2026-09-05/cli-evaluation.json
```

The script uses a temporary directory per case, materializes complete input CSV/manifests via the committed test helper, invokes the actual module CLI, checks strict JSON, and retains classifications/exits/stdout plus source identities. Inputs are deterministic software fixtures. No personal/raw measurement data is included.

## Outcome

Initial execution exited 0: all **10/10** classifications, numerical results, and CLI exit codes matched the predeclared judgments. Full JSON outputs are in [cli-evaluation.json](cli-evaluation.json). No candidate change was made after this scenario run.

Earlier development found an inclusive collective-tolerance endpoint rejected
by floating-point roundoff. A failing endpoint regression preceded the fix;
only up to four floating-point ULPs were allowed at acquisition tolerances.
The authority threshold and statistical recovery gates were unchanged. That
observed case is development material, not held-out evidence.
