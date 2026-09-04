# Guarded Micro-UAV

**An engineering study of a protected micro-UAV that detects release and
attempts attitude recovery within propulsion, descent, sensing, and guard-load
limits.**

[![CI](https://github.com/500ft/SelfStabilizingDrone/actions/workflows/ci.yml/badge.svg)](https://github.com/500ft/SelfStabilizingDrone/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-276c6b)](LICENSE)

**[Results](Analysis/current-results.md) · [Reproduce](#reproduce-the-analysis) · [Data and figures](docs/data-and-figures.md) · [Safety](#safety-boundary)**

![Simulated recovery envelope: altitude loss and recoverable tumble rate for three component tiers](Figures/release_recovery_envelope.png)

*Simulated altitude loss and recoverable tumble rate for three component tiers.
The [results](Analysis/current-results.md) explain the current gate state; the
[figure guide](docs/data-and-figures.md) records assumptions and generators.*

## Overview

Midair recovery requires the release classifier, controller, propulsion system,
battery, mass properties, guard, and test rig to close as one system. This
repository expresses those dependencies as executable models, structured data
tables, test contracts, and staged stop/go gates.

```mermaid
flowchart LR
    classDef input    fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#1f2933,font-weight:bold;
    classDef process  fill:#b2dfdb,stroke:#00796b,stroke-width:2px,color:#1f2933;
    classDef core     fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px,color:#1f2933,font-weight:bold;
    classDef decision fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#1f2933,font-weight:bold;
    classDef endpoint fill:#f8bbd0,stroke:#c2185b,stroke-width:2px,color:#1f2933,font-weight:bold;

    I[/Release cues/]:::input --> C[Classifier and state machine]:::process
    C --> R{{6-DoF recovery simulation}}:::core
    P[/Propulsion authority/]:::input --> R
    M[/Mass, inertia, and CG/]:::input --> R
    R --> G{Recovery and descent gates}:::decision
    S[Guard and rig checks]:::process --> F([Flight-test readiness]):::endpoint
    G --> F
```

*Shapes: parallelogram = input · rectangle = process · hexagon = core method · diamond = gate · pill = endpoint.*

The current plots use estimated or catalog-derived parameters. The Monte Carlo
study compares placeholder torque with an assumed mixer-authority model.
Hardware has not yet supplied the measured authority, mass properties, guard
response, or recovery-flight data needed to close the registered gates.

## Results and status

Every number below is simulation or vendor-spec — **no hardware has been
measured yet**. Full tables and lineage:
[`Analysis/current-results.md`](Analysis/current-results.md).

| Finding | Evidence state |
| --- | --- |
| The Monte Carlo dispersion gate **fails at the placeholder torque authority**: 4.0% recovery as-toleranced (CG ≤ 5 mm, 2 rad/s release). Root cause: thrust-line-offset torque consumes the placeholder 0.004 N·m budget at 0.95 mm offset under recovery thrust. | Simulation — registered gate result (FAIL) |
| Under the physically derived four-motor mixer authority, the same as-toleranced sweep recovers **300/300** (exact 95% lower bounds 96.1–98.0%), worst altitude loss 1.01 m of the 3.0 m budget. | Simulation — **prediction, not a validation**; conditional on an **assumed 60 mm arm** and datasheet thrust |
| Bench measurement **EST-REC-007** (per-motor thrust + arm length → measured differential-torque authority) decides between the two scenarios. | Pre-registered, **pending** — contract in [`docs/specs/measured-authority-gate/`](docs/specs/measured-authority-gate/) |

Phase status and remaining milestones: [`ROADMAP.md`](ROADMAP.md).

## Reproduce the analysis

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s Analysis/tests -v
python -m Analysis.run_release_recovery
python -m Analysis.monte_carlo_recovery
```

The first analysis command regenerates the recovery JSON and four plot files.
The second regenerates the deterministic Monte Carlo JSON. Other calculators
and their inputs are indexed in [`Analysis/README.md`](Analysis/README.md); the
complete data path is in [`docs/data-and-figures.md`](docs/data-and-figures.md).

## Documentation

| Document | Purpose |
| --- | --- |
| [`Analysis/current-results.md`](Analysis/current-results.md) | Current mass, guard, recovery, Monte Carlo, and gate results |
| [`docs/data-and-figures.md`](docs/data-and-figures.md) | Data sources, assumptions, plot generators, and reproduction limits |
| [`docs/figure-manifest.json`](docs/figure-manifest.json) | Machine-readable generator/input/output map |
| [`Engineering Plan/README.md`](Engineering%20Plan/README.md) | Test sequence, dependencies, and exit gates |
| [`Design Report/README.md`](Design%20Report/README.md) | Architecture, BOM, and preliminary calculations |
| [`Controls/README.md`](Controls/README.md) | State machine and control interfaces |
| [`Instrumentation/README.md`](Instrumentation/README.md) | Bench equipment and measurement procedures |
| [`Safety/README.md`](Safety/README.md) | Release-rig plan and operating controls |
| [`docs/specs/measured-authority-gate/`](docs/specs/measured-authority-gate/) | Registered propulsion and recovery acceptance contract |
| [`ROADMAP.md`](ROADMAP.md) | Project phases and remaining milestones |

The authoritative controller state names and guards are stored in
[`Controls/state_machine.json`](Controls/state_machine.json).

## Repository map

```text
Analysis/          executable models, gates, tests, and result summary
Controls/          recovery state machine and controller interfaces
Data/              generated JSON plus the structure for future test data
Design Report/     BOM, architecture, and calculations
Engineering Data/  requirements, budgets, interfaces, and FMEA tables
Engineering Plan/  staged execution and procurement plan
Instrumentation/   bench procedures and measurement requirements
Safety/            release-rig and operating controls
Figures/           generated plots and authored engineering diagrams
Research/          component, propulsion, and architecture studies
docs/              specifications and figure lineage
```

## Safety boundary

Do not attempt a recovery flight from the current project state. Propulsion
measurements, guard testing, release-rig checks, and the registered simulation
gates must be completed first. See the
[`propulsion-bench checklist`](Instrumentation/propulsion-bench-safety-checklist.md)
and [`Safety/README.md`](Safety/README.md).

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for analysis checks, generated-artifact
rules, and safety constraints. The project uses the [MIT License](LICENSE).
