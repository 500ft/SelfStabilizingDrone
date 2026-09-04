# SelfStabilizingDrone — tasks to completion

> **Objective.** Produce the strongest, most honestly-packaged evidence — not a completed
> project. Priority flows from leverage (does it unblock other work, or add decisive evidence)
> and from executability. Never from a calendar, and never from this project's ceiling.

Generated from an audit of the committed state of this repository. Every task is anchored to a
checked fact; no dates or estimates appear anywhere, by design.

## Two finish lines

**Ceiling.** A preregistered bench torque, then a drop-test video matching the prediction, plus the release classifier as a second citable artifact.

**Floor.** Preregistered gates with **measurement pending** stated plainly. The 8.4% reserve is arithmetically correct and already marked `BENCH_REQUIRED`; the floor is that package with the gate honest and unfilled.

The floor is the realistic finish line for anything gated on a measurement, and its tasks are
listed alongside the ceiling's — so the project is presentable even if the measurement never
happens.

_11 tasks · 4 Tier 0 · 5 executable now._

**Gate types.** `preregister` — write the threshold down *before* the thing it judges;
`external` — needs a resource or a person outside this repo; `build` — new work;
`hygiene` — reproducibility debt.

**Tiers.** 0 finish · 1 package · 2 park. A task whose blocker is not secured cannot be Tier 0
however decisive it is, which is why several measurements sit in Tier 2 with their
preregistration in Tier 0 ahead of them.

---

## Tier 0 — finish

### SSD-01 · Merge PR #1 (audit/mass-rollup-drift)

`hygiene` · executable now

**Why it matters.** Two documents state a mass rollup the committed script no longer produces (117.96/129.76/149.5 g against 123.86/135.66/156.00 g).

**What it adds.** Documents that agree with the committed CSV.

**Done when.** main states the committed rollup and analysis-tests stays green.

### SSD-02 · Merge PR #2 (audit/gate-mass-numbers)

`hygiene` · executable now · after SSD-01

**Why it matters.** PR #1 fixed the tables but left three references to the superseded 155 g frozen maximum, two of them load-bearing: the static thrust requirement understated total thrust by 20 gf.

**What it adds.** A test that fails whenever a document drifts from budget.py, so this class of error cannot recur.

**Done when.** main carries 330 g / 82.5 gf per motor and the 73-test suite passes.

### SSD-03 · Commit the bench acceptance criterion before the propulsion test

`preregister` · executable now

**Why it matters.** Every recovery claim rests on a torque number that does not exist. Writing the threshold after seeing the torque makes the 8.4% reserve unfalsifiable.

**What it adds.** Turns the bench run into a real PASS/FAIL rather than a description.

**Done when.** Acceptance criterion committed - the fifth-percentile differential torque required at each collective point - with no bench data taken.

### SSD-04 · Restate the Monte Carlo recovery gate with measured authority as the unknown

`preregister` · executable now · after SSD-03

**Why it matters.** Scenario C reports 100% recovery on an ASSUMED 60 mm arm. Stated as-is it reads as a result rather than a conditional prediction.

**What it adds.** A gate that the measurement can actually decide.

**Done when.** The >=962/1000 gate restated against measured authority and committed, before any measurement.

## Tier 1 — package

### SSD-07 · Write the floor package: preregistered gates with measurement pending stated plainly

`build` · executable now · after SSD-04

**Why it matters.** If the bench never happens the project still has to be presentable, and a reader must not have to infer which numbers are measured.

**What it adds.** A defensible package in registered-design mode - the honest finish line if the bench never runs.

**Done when.** One document committed that states each gate, its threshold, and its measurement-pending status.

### SSD-08 · Build the drop rig and instrument it

`build` · **blocked-on-hardware**

**Why it matters.** The drop test needs a repeatable release; without a rig the video is anecdote.

**What it adds.** A repeatable release condition.

**Done when.** Rig built and one instrumented release logged.

### SSD-09 · Collect the release-detection dataset on the Nicla

`build` · **blocked-on-hardware** · after SSD-08

**Why it matters.** The classifier cannot be trained or frozen without labelled release events.

**What it adds.** The dataset the TinyML artifact depends on.

**Done when.** Labelled dataset committed with the collection protocol.

## Tier 2 — park

### SSD-05 · Measure differential roll/pitch torque at 7.0 V, 6 repeats, and record the fifth percentile

`external` · **blocked-on-bench** · after SSD-03

**Why it matters.** This single measurement is the entire distance between the project and its ceiling; nothing downstream can exist without it.

**What it adds.** Converts the drone from a simulation study into a measured one.

**Done when.** Committed CSV of torque against collective at 7.0 V with the fifth percentile computed.

### SSD-06 · Re-run the Monte Carlo with the measured authority

`build` · **blocked-on-bench** · after SSD-05

**Why it matters.** The 100% scenario-C figure is conditional on an assumed arm length and must be re-derived once the arm is real.

**What it adds.** A recovery-robustness number that no longer rests on an assumption.

**Done when.** Re-run committed, scored against SSD-04 without adjusting the gate.

### SSD-10 · Train and freeze the TinyML release classifier

`build` · **blocked-on-hardware** · after SSD-09

**Why it matters.** An unfrozen model cannot be cited or evaluated on a held-out split.

**What it adds.** A second citable artifact independent of the recovery claim.

**Done when.** Frozen weights, a leakage-aware split and held-out metrics committed.

### SSD-11 · Drop test with video, scored against the prediction

`external` · **blocked-on-hardware** · after SSD-06,SSD-08

**Why it matters.** The prediction is only evidence once something outside the simulation agrees with it.

**What it adds.** The ceiling: a demonstrated recovery matching a preregistered prediction.

**Done when.** Video and telemetry committed with the scored comparison.

---

## Cross-cutting

These span repositories and are tracked identically in the others they touch.

### XC-01 · Reconcile the repo, portfolio and resume headline numbers

`hygiene` · executable now

**Why it matters.** A reviewer clicks between the three, and a disagreement there is more damaging than any single wrong number because it looks like carelessness rather than a stale file. Checked so far: the portfolio quotes 174.7 Hz (matches the repo - 163.8 Hz was the 0.20 kg placeholder tip mass, not drift) and r = 0.885 (matches), and makes no drone-mass claim. The resume was not available to check.

**Done when.** Every headline number in the portfolio and resume traced to a committed artifact, with any disagreement fixed at the source.

