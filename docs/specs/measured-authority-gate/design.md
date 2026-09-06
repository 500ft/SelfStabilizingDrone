# EST-REC-007 Measured Authority Gate — Frozen Protocol

Protocol frozen: 2026-07-17
Status: measurement pending

## Decision claim

Wave 2 is authorized only if both the measured propulsion-authority gate and
the end-to-end recovery simulation gate pass. Static thrust times arm validates
available roll/pitch torque; it does not by itself validate dynamic recovery.

## Authority threshold

At 7.0 V under load, calculate roll/pitch mixer authority across collective
fractions 0.25, 0.375, 0.50, 0.625, and 0.75. Use all six motors and propagate
calibration and motor-to-motor variation. The conservative empirical fifth
percentile must be at least **0.020 N·m at every grid point**.

The value is frozen from the design physics, not the forthcoming data. The
225 g full-reserve propulsion requirement is 112.5 gf/motor, approximately
4.41 N total. At 75% collective that is about 3.31 N; a 5 mm thrust-line offset
creates roughly 0.0166 N·m disturbance. The 0.020 N·m threshold retains about
20% margin over that disturbance and is 5× the old 0.004 N·m placeholder. The
current 4.2 N, 60 mm assumed mixer predicts about 0.0445 N·m at both band edges.

The direct gate CSV has one row per derived authority sample:

```text
sample_id,raw_record_id,motor_id,voltage_v,collective_fraction,tau_rp_n_m,expanded_uncertainty_n_m
```

Raw thrust, current, temperature, RPM, arm measurement, calibration, and motor
identifier remain in the source dataset and must trace to each derived sample.

### Evidence-admission correction — 2026-09-05

The original three-column checker did not enforce this protocol and could
accept nonfinite torque. The [evidence contract](evidence-contract.md) adds
traceable records and a manifest without changing 0.020 N·m, the grid, voltage,
or the 962/1,000 recovery requirement. Six motors means six sampled motors
characterizing the four-motor aircraft, not a six-motor airframe.

Apply the supplied expanded torque uncertainty once to each nominal derived
sample: `max(0, tau_rp_n_m - expanded_uncertainty_n_m)`. The uncertainty artifact
must explain calibration and motor-variation propagation, coverage assumptions,
and dependencies; the checker does not invent an uncertainty value or validate
that derivation. Owner review is required before calling a bundle measured.

The fifth percentile is empirical over admitted observations. With six samples
it is the sample minimum, not a 95%-confidence population quantile. Repeated
observations are not additional independent motors; selection and repeat counts
must be documented in the reviewed derivation. The future sampling plan must
be fixed before data collection. No new population-confidence claim is made.

Missing/inconsistent evidence produces INCONCLUSIVE. A synthetic bundle returns
DEVELOPMENT_ONLY with a separate numerical result; it cannot close a physical
gate. Hash checks and review metadata establish supplied-bundle consistency,
not authenticity or scientific adequacy. PASS is static authority only and
still requires the independent end-to-end and safety gates below.

## End-to-end gate

Use the fixed controller, dispersions, and seeds with measured authority and
spool distributions. The primary case is 60° tilt, 2 rad/s initial tumble,
CG offset ≤5 mm, and 3.0 m available height. Run exactly 1,000 primary trials.
PASS requires:

- at least **962/1,000** recoveries;
- exact one-sided 95% Clopper–Pearson lower bound ≥0.95; and
- maximum descent across all trials ≤3.0 m.

Run 250 trials each at 1 and 3 rad/s for descriptive sensitivity only. Those
cases cannot rescue a failed primary gate. Controller tuning on evaluation
trials opens a separately labeled redesign round; it cannot rewrite this gate.

## Decision

- **PASS:** authority and end-to-end gates both pass; Wave 2 may be considered.
- **FAIL:** either completed gate fails; publish the negative design study and
  stop Wave-2 spending unless a separately costed redesign is preregistered.
- **INCONCLUSIVE:** calibration, required collective points, six-motor coverage,
  telemetry integrity, or uncertainty is inadequate; fix the measurement once
  and rerun without changing thresholds.
