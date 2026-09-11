# Presentation migration verification

Date: September 10, 2026. Base commit: `7aae61f302f9a400118fb38d4b298d020aa0fc0e`.

The README, reading guide, conceptual overview and contribution templates now
use Multirotor Recovery Dynamics. Existing study inputs, results, protocols,
parameter registers and physical-gate states are unchanged. No new CAD or
physical observation is claimed. [Identity notes](../../docs/REPOSITORY_IDENTITY.md).

[checks.json](checks.json) records commands and local outputs: 29 CAD tests,
91 analysis tests, navigation checks and four presentation negative controls
pass. CAD dependency deprecation warnings are retained, not hidden.

From the root:

```sh
python tools/check_presentation.py . "Multirotor Recovery Dynamics" multirotor-recovery-dynamics
python tools/test_presentation.py
python -m unittest discover -s Analysis/tests -v
```

Use the [reading guide](../../docs/START_HERE.md) for analysis dependencies and the
separate CadQuery environment. Hosted checks and rendered presentation are
verified on the PR, not inferred from local success. No flight or bench readiness
is established by this documentation update.
