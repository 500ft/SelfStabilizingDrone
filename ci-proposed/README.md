# Proposed CI change — not active

## Review amendment — 2026-09-09

The CAD proposal is now installed as
[`.github/workflows/cad-geometry.yml`](../.github/workflows/cad-geometry.yml).
Current-session authentication was verified by the parent reviewer to include
workflow permission; the earlier token restriction below is historical, not a
current blocker. Do not reapply the CAD patch: it is retained only as the original
proposal. Hosted CAD verification is pending until the amended PR runs green.
The installed job reads version constraints directly from `cad/requirements.lock`
and accepts PRs to main or a day-1 stack base. Those constraints pin five direct
packages; they are not a platform/build/transitive dependency lock.

`cad-geometry-workflow.patch` adds `.github/workflows/cad-geometry.yml`, the geometry CI that
DR-CAD-10 requires. It is **not installed**: the token that opened this PR has no `workflow`
scope, and that restriction exists to stop an automated token from silently changing what
CI executes. `git apply --check` passes against this branch.

```bash
git apply ci-proposed/cad-geometry-workflow.patch
git add .github/workflows/cad-geometry.yml && git commit -m "ci: add CAD geometry job (DR-CAD-10)"
rm -rf ci-proposed
```

Until it is applied, the geometry tests run only when invoked by hand:
`python -m pytest cad/tests -q` in an environment matching `cad/requirements.lock`.
