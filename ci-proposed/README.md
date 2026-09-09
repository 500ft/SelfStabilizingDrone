# Proposed CI change — not active

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
