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

## Decision required: pick ONE lane

### Lane A — Simulation deliverable (recommended)

Cheap, reliable, fully in your control. Build a 6-DoF dynamics + control
simulation of the release-to-stabilization maneuver and produce a demonstrable
result (plots + a short video).

- [ ] 6-DoF rigid-body model with the locked-BOM mass/inertia.
- [ ] Toss/drop/release detection from simulated IMU.
- [ ] Stabilization controller that arrests tumble and recovers to hover.
- [ ] Characterize: recovery time, control-authority margin, max recoverable
      release rate.
- [ ] One figure set + a screen-recorded sim run.

Outcome: converts the project from "plan" to "demonstrated control result"
without spending money or risking an 8-week hardware slip.

### Lane B — Hardware bench test (only if budget + time are real)

Buy the locked BOM, build, and capture **one** tethered stabilization bench test
on video. Higher ceiling, but real risk of nothing-to-show by late August.
Pursue only if hardware budget is committed and the build path is de-risked.

## Default recommendation

**Take Lane A now.** It guarantees a result. Treat Lane B as a fall/winter
extension if Lane A succeeds and hardware funding lands.

## Portfolio statement (Lane A)

> Modeled and simulated a release-to-stabilization controller for a sub-250g UAV,
> characterizing recovery time and control-authority margins under toss/drop
> initial conditions.
