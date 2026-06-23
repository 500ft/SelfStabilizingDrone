# Roadmap — Guarded Micro-UAV (SelfStabilizingDrone)

_Last updated: 2026-06-23 · Horizon: 8 weeks (through ~2026-08-23)_

## Honest starting point

This repository is currently **thorough planning with zero demonstrated
results** — locked BOM, component study, gates, FMEA, safety plan, and some
analysis scripts, but (per the README) no purchased-and-weighed hardware, no
completed CAD, no measured bench data, and no flight evidence. "Drone project"
is also the most common ME-portfolio entry, so without a result it does not yet
differentiate.

**The marginal planning document now has near-zero resume value. Stop writing
them.** This cycle is about producing one demonstrable result.

## Decision required: pick ONE demonstrable deliverable

There are now **three** ways to produce a real result this cycle. Two cost no
money and are fully in your control (Lane A, Lane A+); one is gated (Lane B).
**Lane A+ is new and changes the calculus:** the "no completed CAD" gap is an
opportunity, not just a weakness — you can do CAD and FEA, so a parametric
airframe with structural/modal analysis is itself a demonstrable engineering
deliverable, and it feeds Lane A real mass and inertia instead of a BOM
estimate. The strongest cycle is **Lane A+ → Lane A** (CAD/FEA first, then drop
its mass/inertia tensor into the 6-DoF sim). Lane B stays gated exactly as
before.

This is still about results, not more planning docs: each lane below must end in
artifacts (CAD files, stress/modal plots with numbers, sim figures + video), not
prose.

### Lane A — Simulation deliverable (recommended)

Cheap, reliable, fully in your control. Build a 6-DoF dynamics + control
simulation of the release-to-stabilization maneuver and produce a demonstrable
result (plots + a short video).

- [ ] 6-DoF rigid-body model. Mass/inertia: start from the locked-BOM estimate,
      but **replace it with the CAD-extracted inertia tensor from Lane A+** as
      soon as that exists (CAD feeds the sim — see Lane A+).
- [ ] Toss/drop/release detection from simulated IMU.
- [ ] Stabilization controller that arrests tumble and recovers to hover.
- [ ] Characterize: recovery time, control-authority margin, max recoverable
      release rate.
- [ ] One figure set + a screen-recorded sim run.

Outcome: converts the project from "plan" to "demonstrated control result"
without spending money or risking an 8-week hardware slip.

### Lane A+ — Mechanical CAD/FEA package (demonstrable, no hardware purchase)

You can do CAD and FEA. The README's "no completed CAD" is therefore an
**opportunity** — a parametric airframe plus a structural/modal analysis package
is a standalone, money-free engineering result, and it produces the real
mass/inertia that Lane A needs. This is also where the project stops being a
generic quad: the **prop guard and the payload/release-recovery mechanism** are
the genuine differentiators, and they get designed and analyzed here.

This is a deliverable, not a planning doc. "Done" means CAD files plus
stress/deflection/safety-factor numbers and a modal table — not a description of
intent.

**Parametric airframe CAD** — model as a parametric assembly so geometry can be
re-driven from a few key dimensions:

- [ ] Frame / center plate, arms, motor mounts.
- [ ] Prop guard (full-perimeter, sub-250g-conscious).
- [ ] Payload + release-recovery mechanism (the differentiator vs a generic
      quad).
- [ ] Pull **total mass and the full 3×3 inertia tensor** (about the CG, with
      stated material densities and component masses) directly from the CAD.

**CAD → sim coupling (make this explicit):**

- [ ] The CAD-extracted mass and inertia tensor **replace** the locked-BOM
      mass/inertia in the Lane A 6-DoF model. CAD is the source of truth for the
      sim's rigid-body properties; re-export whenever the geometry changes.

**Structural FEA** — report stress, deflection, and safety factor for each case,
with the load path and boundary conditions stated:

- [ ] Arm/frame under **max-thrust** load (all motors at peak thrust; static).
- [ ] **Hard-landing / crash** load case (defined drop or g-load into the frame).
- [ ] **Guard impact** (lateral strike into the prop guard).
- [ ] **Mesh-convergence check**: refine and show the gauge-region result has
      converged to **< 5%** change between the last two refinements (don't trust
      a single un-converged mesh).

**Modal analysis** — frame natural frequencies vs the motor/prop excitation band:

- [ ] Compute the first several structural natural frequencies of the airframe.
- [ ] Lay them against the operating **rev frequency and prop-pass (blade-pass)
      frequency** band across the throttle range.
- [ ] **Acceptance criterion:** first structural mode sits clear of the operating
      rev/prop-pass frequencies, so resonance doesn't corrupt the IMU signal or
      the control loop. If it doesn't clear, stiffen/redesign and re-run.

Outcome: a parametric airframe + a structural/modal analysis package that (a) is
a demonstrable mechanical result on its own and (b) hands Lane A real,
CAD-derived mass and inertia — strengthening the sim instead of leaving it on a
BOM estimate.

### Lane B — Hardware bench test (only if budget + time are real)

Buy the locked BOM, build, and capture **one** tethered stabilization bench test
on video. Higher ceiling, but real risk of nothing-to-show by late August.
Pursue only if hardware budget is committed and the build path is de-risked.

## Default recommendation

**Run Lane A+ → Lane A now.** Both are money-free and fully in your control, and
together they give two demonstrable results that reinforce each other: the
CAD/FEA package produces the real mass/inertia, and the sim consumes it. Start
the CAD so the inertia tensor exists before the sim hardens its rigid-body
properties. Treat Lane B as a fall/winter extension if these succeed and
hardware funding lands.

## Portfolio statement (Lane A+ / Lane A)

> Designed a parametric sub-250g guarded-UAV airframe (frame, arms, prop guard,
> payload/release mechanism) in CAD; verified it with structural FEA
> (max-thrust, hard-landing, and guard-impact load cases, mesh-converged
> < 5%) and a modal analysis clearing the first structural mode of the
> motor/prop excitation band; then drove a 6-DoF release-to-stabilization
> control simulation with the CAD-extracted mass and inertia tensor,
> characterizing recovery time and control-authority margins under toss/drop
> initial conditions.

_No hardware has been built, weighed, or flown; all results above are CAD, FEA,
and simulation._
