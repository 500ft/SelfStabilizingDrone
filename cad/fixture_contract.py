#!/usr/bin/env python3
"""Bench-fixture geometry contract for the propulsion thrust stand, derived from the register.

usage: python cad/fixture_contract.py --refresh   # (re)write cad/bench/fixture-contract.json
       python cad/fixture_contract.py --check     # exit 1 if the committed contract is stale
       python cad/fixture_contract.py --release   # exit 2 REFUSED while any clause is pending

This is the contract cad/bench/fixture-preparation.md ("Geometry contract before a model")
requires BEFORE any fixture model exists. It names every interface, clearance and load-path
quantity a fixture model must be compared against, derives the few the register can support
(prop swept envelope from vendor nominal, envelope-only motor volume), and carries every
unmeasured interface as a PENDING clause with its release requirement copied from the
register. It models nothing and measures nothing: a clause becomes evaluable only when its
register row is filled by inspection, a drawing, or an owner decision -- never by this script.
Vendor-nominal rows are evaluable for geometry planning but are labelled so; they are not
inspected values and do not satisfy the "Confirm delivered ..." release requirements.
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "cad/bench/parameters.csv"
OUTPUT = ROOT / "cad/bench/fixture-contract.json"
CONTRACT_VERSION = "2026-09-12"
UNITS = {
    "motor_body_diameter": "mm", "motor_body_length": "mm", "motor_shaft_diameter": "mm",
    "prop_diameter": "mm", "prop_hub_bore": "mm",
    "motor_mount_pitch_circle": "mm", "motor_mount_hole_diameter": "mm", "motor_mount_thread_engagement": "mm",
    "prop_mount_screw_spacing": "mm", "load_cell_mount_spacing": "mm", "load_cell_capacity": "N",
    "stand_anchor_spacing": "mm", "stand_calibration_lever": "m", "authority_arm_measured": "m",
    "total_thrust_model": "N", "thrust_expanded_uncertainty": "N",
}
STATE_RANK = ["pending", "model_assumption", "vendor_nominal", "reported_vendor_nominal", "design_choice", "inspection", "protocol"]


class ContractInputError(ValueError):
    """The register cannot support the contract as written. Fail closed."""


def load_register(path: Path = REGISTER) -> dict:
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8", newline="")))
    have: dict = {}
    for row in rows:
        if row["parameter"] in have:
            raise ContractInputError("duplicate parameter in register: " + row["parameter"])
        have[row["parameter"]] = row
    out = {}
    for name, unit in UNITS.items():
        if name not in have:
            raise ContractInputError("required parameter missing from register: " + name)
        r = have[name]
        if r["unit"].strip() != unit:
            raise ContractInputError(f"unit mismatch for {name}: register {r['unit']!r}, contract expects {unit!r}")
        state = r["evidence_state"].strip(); raw = r["value"].strip()
        if state == "pending":
            if raw:
                raise ContractInputError("pending parameter carries a value; refuse to treat it as measured: " + name)
            out[name] = dict(value=None, state="pending", source=r["source"], release=r["release_requirement"]); continue
        try:
            value = float(raw)
        except ValueError:
            raise ContractInputError(f"non-numeric value for {name}: {raw!r}")
        if not math.isfinite(value) or value <= 0:
            raise ContractInputError(f"value must be finite and positive: {name}={raw}")
        out[name] = dict(value=value, state=state, source=r["source"], release=r["release_requirement"])
    return out


def _state(*names, reg):
    states = [reg[n]["state"] for n in names]
    return min(states, key=lambda s: STATE_RANK.index(s) if s in STATE_RANK else len(STATE_RANK))


def _clause(cid, group, requirement, inputs, reg, *, value=None, unit=None, formula=None, verification=None, note=None):
    pending = [n for n in inputs if reg[n]["state"] == "pending"]
    c = {"id": cid, "group": group, "requirement": requirement, "inputs": list(inputs),
         "status": "pending" if pending else "evaluable",
         "evidence_state": _state(*inputs, reg=reg) if inputs else "protocol"}
    if pending:
        c["pending_inputs"] = pending
        c["release_requirement"] = {n: reg[n]["release"] for n in pending}
    if formula: c["formula"] = formula
    if value is not None: c["value"] = value
    if unit: c["unit"] = unit
    if verification: c["verification"] = verification
    if note: c["note"] = note
    return c


def build(reg: dict) -> dict:
    D, L, ds = (reg[k]["value"] for k in ("motor_body_diameter", "motor_body_length", "motor_shaft_diameter"))
    Dp, bore = reg["prop_diameter"]["value"], reg["prop_hub_bore"]["value"]
    if Dp <= D:
        raise ContractInputError(f"prop diameter {Dp} mm does not clear the motor body {D} mm")
    if ds > bore * 1.5 or ds <= 0:
        raise ContractInputError(f"shaft {ds} mm and hub bore {bore} mm are not a plausible pair")
    Tm = reg["total_thrust_model"]["value"]
    clauses = [
        # ── interfaces ──
        _clause("motor_mount_pattern", "interface", "Fixture motor plate hole coordinates equal the measured EX1103 pattern (pitch circle, hole diameter) within the drawing tolerance",
                ["motor_mount_pitch_circle", "motor_mount_hole_diameter"], reg, unit="mm", verification="Dimensioned drawing or measured hole coordinates with uncertainty"),
        _clause("motor_mount_thread_engagement", "interface", "Screw penetration into the motor bell is at or below the safe depth and at or above the minimum engagement, across the plate + adapter stack",
                ["motor_mount_thread_engagement"], reg, unit="mm", verification="Owner confirms safe penetration; stack drawing lists every plate/washer thickness"),
        _clause("prop_hub_interface", "interface", "Prop hub bore and T-mount screw spacing match the delivered bell; hub bore equals shaft nominal until the delivered shaft is measured",
                ["prop_hub_bore", "motor_shaft_diameter", "prop_mount_screw_spacing"], reg, value={"hub_bore_mm": bore, "shaft_nominal_mm": ds}, unit="mm",
                note="Vendor-nominal bore/shaft are planning values; the mating fit is confirmed only by measuring the delivered shaft and hub."),
        _clause("load_cell_end_interfaces", "interface", "Both load-cell end interfaces (mount spacing, thread, orientation) match the identified, calibrated cell revision",
                ["load_cell_mount_spacing", "load_cell_capacity"], reg, unit="mm", verification="Engineering Data/instrumentation.csv names the cell; its drawing is the source"),
        _clause("stand_anchor_pattern", "interface", "Fixture base anchor pattern equals the measured bench mounting and the documented stability/load path",
                ["stand_anchor_spacing"], reg, unit="mm", verification="Instrumentation/propulsion-bench-safety-checklist.md"),
        # ── clearances ──
        _clause("prop_static_swept_envelope", "clearance", "No fixture, cable or guard element lies inside the static prop swept disc of diameter prop_diameter about the motor axis",
                ["prop_diameter"], reg, value=Dp, unit="mm", formula="static swept diameter = prop_diameter",
                note="STATIC envelope only. Dynamic clearance (blade flap, whirl) and containment envelope are a separately approved addition per the register's release requirement, NOT derived here."),
        _clause("motor_envelope_volume", "clearance", "Motor keep-out cylinder D x L; the only solid cad/generate.py produces today",
                ["motor_body_diameter", "motor_body_length"], reg, value=math.pi / 4 * D**2 * L, unit="mm^3", formula="pi/4 * D^2 * L",
                note="Envelope only (vendor nominal); no mount features are modelled until the pattern is measured."),
        _clause("sensor_deflection_clearance", "clearance", "Load-cell deflection at predicted peak load plus dead load does not close any clearance to a hard stop or preload path",
                ["load_cell_capacity", "total_thrust_model"], reg, unit="mm",
                note=f"Model peak thrust {Tm} N is a planning value (model_assumption); the cell's stiffness comes from its drawing once identified."),
        # ── load path ──
        _clause("force_axis_datum", "load_path", "Thrust axis passes through the load-cell sensitive axis; offset recorded, off-axis moment bounded, never bypassing the cell",
                ["load_cell_mount_spacing"], reg, unit="mm", verification="Interface coordinates in the machine-readable report; cable and containment attachments traced"),
        _clause("load_cell_capacity_margin", "load_path", "Cell capacity exceeds dead load + predicted peak thrust + reaction transients with the owner-selected overload margin",
                ["load_cell_capacity", "total_thrust_model"], reg, unit="N", formula="capacity >= margin * (dead_load + peak_thrust); margin is an owner decision",
                note=f"Planning peak thrust {Tm} N total (model_assumption, per-motor share is a design decision). Dead load and predicted peak are to be recorded separately."),
        _clause("stand_calibration_lever", "load_path", "If a lever-type calibration is used, the perpendicular pivot-to-force-line distance is calibrated and distinct from the vehicle authority arm",
                ["stand_calibration_lever", "authority_arm_measured"], reg, unit="m", verification="docs/specs/measured-authority-gate/evidence-contract.md: arm_m is measured separately from stand calibration"),
        _clause("thrust_uncertainty_budget", "load_path", "The expanded thrust uncertainty artifact exists and covers calibration, alignment and dead-load subtraction before any authority number is computed",
                ["thrust_expanded_uncertainty"], reg, unit="N", verification="Reviewed calibration and uncertainty artifact"),
    ]
    return {
        "family": "propulsion_bench_fixture",
        "contract_version": CONTRACT_VERSION,
        "status": "pending_inputs",
        "source_parameters": "cad/bench/parameters.csv",
        "governing_documents": ["cad/bench/fixture-preparation.md", "cad/bench/design-inputs.md",
                                 "docs/specs/measured-authority-gate/evidence-contract.md", "Instrumentation/propulsion-bench-safety-checklist.md"],
        "release_gate": "Every clause evaluable AND its inputs at inspection/drawing evidence state; vendor_nominal rows satisfy geometry planning only. A CAD collision check does not prove structural stability or prop containment.",
        "clauses": clauses,
        "evaluable_clauses": [c["id"] for c in clauses if c["status"] == "evaluable"],
        "pending_clauses": [c["id"] for c in clauses if c["status"] == "pending"],
        "not_generated_pending_owner_inputs": sorted({n for c in clauses for n in c.get("pending_inputs", [])}),
        "vendor_nominal_inputs_awaiting_confirmation": sorted(n for n, v in reg.items() if v["state"] in ("vendor_nominal", "reported_vendor_nominal")),
        "evidence_note": "Derived from the register on the stated version; no fixture STEP exists; nothing here authorises fabrication, spending, pressurisation or rotor operation.",
    }


def render(contract: dict) -> str:
    return json.dumps(contract, indent=2) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if the committed contract is stale")
    mode.add_argument("--release", action="store_true", help="exit 2 REFUSED while any clause is pending")
    mode.add_argument("--refresh", action="store_true", help="rewrite the committed contract from the register")
    parser.add_argument("--parameters", type=Path, default=REGISTER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    a = parser.parse_args(argv)
    try:
        contract = build(load_register(a.parameters))
    except ContractInputError as e:
        print("REFUSED:", e, file=sys.stderr); return 2
    if a.check:
        if not a.output.exists() or a.output.read_text() != render(contract):
            print("STALE: committed fixture contract does not match the register; run --refresh", file=sys.stderr); return 1
        print(f"fixture contract current: {len(contract['evaluable_clauses'])} evaluable, {len(contract['pending_clauses'])} pending"); return 0
    if a.release:
        if contract["pending_clauses"]:
            print("REFUSED: fixture contract cannot release; pending clauses:\n  - " + "\n  - ".join(contract["pending_clauses"]), file=sys.stderr)
            print("  pending register rows: " + ", ".join(contract["not_generated_pending_owner_inputs"]), file=sys.stderr); return 2
        if contract["vendor_nominal_inputs_awaiting_confirmation"]:
            print("REFUSED: all clauses evaluable but vendor-nominal inputs are unconfirmed: " + ", ".join(contract["vendor_nominal_inputs_awaiting_confirmation"]), file=sys.stderr); return 2
        print("RELEASABLE: every clause evaluable on inspected inputs (geometry comparison still required)"); return 0
    a.output.write_text(render(contract))
    print(f"wrote {a.output.relative_to(ROOT) if a.output.is_relative_to(ROOT) else a.output}: {len(contract['evaluable_clauses'])} evaluable, {len(contract['pending_clauses'])} pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
