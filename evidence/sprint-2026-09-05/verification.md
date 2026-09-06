# Verification record — 2026-09-05

Working directory: repository root of the isolated sprint checkout. Python
3.11.8, NumPy 2.1.1, Matplotlib 3.10.1; base
`45da9be1a9647ce39ae18e3ea2494d965ee827e8`. No hardware, publication, push, or
external service was exercised.

## Baseline

`python -m unittest discover -s Analysis/tests -v`: exit 0, 69 tests in
119.355s. Complete invalid input and selected output: [baseline.md](baseline.md).

## Test-first changes

1. Added nonfinite/unphysical assertions before correction.
   Command: `python -m unittest Analysis.tests.test_measured_authority_gate -v`.
   Original behavior: exit 1, 6 tests, five failing subcases.
   NaN voltage/+Infinity torque yielded PASS; negative/-Infinity/NaN torque
   yielded FAIL instead of INCONCLUSIVE. Small finite/sign correction: exit 0,
   6 tests, 0.001s.
2. Added evidence-contract/API/CLI regressions before adding the interface.
   Command: `python -m unittest Analysis.tests.test_measured_authority_gate.EvidenceContractTests -v`.
   Red: exit 1, 11 tests, two assertion failures and 19 subcase errors
   (`evaluate_rows() got an unexpected keyword argument 'evidence_path'`).
   Assertions caught three-column PASS and missing-evidence CLI exit 0.
   Green after implementation: exit 0, 11 tests, 0.105s.
3. Added exact acquisition-tolerance endpoint regression before correction.
   Command: `python -m unittest Analysis.tests.test_measured_authority_gate.EvidenceContractTests.test_exact_registered_threshold_and_tolerance_endpoints -v`.
   Red: exit 1, one failure: INCONCLUSIVE rather than PASS at collective
   `registered_point + 0.002`. Binary roundoff fix: inclusive acquisition
   tolerances allow up to four ULPs; no authority/statistical threshold changed.
4. Final focused suite: `python -m unittest Analysis.tests.test_measured_authority_gate -v`.
   Exit 0, **21 tests in 0.140s**. The original numerical PASS/FAIL assertions
   remain and now supply an explicit synthetic fixture of the required evidence
   bundle; requirements were strengthened, not weakened to satisfy tests.

These are selected observed console summaries, not fabricated full transcripts.
Reviewers can rerun all current regression inputs from the test source. To
reproduce the original defect use the complete input against the base in a
separate checkout; do not overwrite this candidate.

## Delivery and final gates

- `python -m Analysis.measured_authority_gate --help`: exit 0; exposes CSV,
  `--manifest`, and `--output` arguments.
- `python evidence/sprint-2026-09-05/evaluate_candidate.py --output evidence/sprint-2026-09-05/cli-evaluation.json`:
  exit 0, all 10 predeclared developer scenarios matched; actual subprocess
  CLI responses retained. Inputs are synthetic, including measured-label
  branch coverage. This is not independent evaluation or physical validation.
- `python -m compileall -q Analysis`: exit 0.
- `git diff --check`: exit 0.
- Repository Markdown-link check: exit 0, one test in 0.008s before final docs.
- Full final CI suite: `python -m unittest discover -s Analysis/tests -v`;
  exit 0, **86 tests in 128.281s**, outcome collected on 2026-09-06.
  This includes the unchanged exact-binomial/962-of-1000 and descent tests.

No typecheck, lint, distributable build, registry route, or flight-test gate is
configured/exercised by this software change. CLI execution is the actual
consumer route; it does not establish installation/publication/deployment.
