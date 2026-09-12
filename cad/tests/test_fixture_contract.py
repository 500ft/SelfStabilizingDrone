"""Bench-fixture geometry contract: pending inputs must prevent release; nothing is guessed."""
import csv, json, math, subprocess, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from cad import fixture_contract as FC  # noqa: E402


def _write_register(tmp_path, mutate):
    rows = list(csv.DictReader(FC.REGISTER.open(encoding="utf-8", newline="")))
    mutate(rows)
    p = tmp_path / "parameters.csv"
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return p


def test_committed_contract_is_current():
    assert FC.OUTPUT.read_text() == FC.render(FC.build(FC.load_register())), "run: python cad/fixture_contract.py --refresh"


def test_every_pending_register_row_used_by_the_contract_blocks_a_clause():
    reg = FC.load_register(); c = FC.build(reg)
    pending_rows = {n for n, v in reg.items() if v["state"] == "pending"}
    assert set(c["not_generated_pending_owner_inputs"]) == pending_rows
    assert len(c["pending_clauses"]) == 10 and len(c["evaluable_clauses"]) == 2


def test_groups_cover_interfaces_clearances_and_load_path():
    c = FC.build(FC.load_register())
    assert {cl["group"] for cl in c["clauses"]} == {"interface", "clearance", "load_path"}


def test_derived_values_match_register_arithmetic():
    c = FC.build(FC.load_register()); by = {cl["id"]: cl for cl in c["clauses"]}
    assert math.isclose(by["motor_envelope_volume"]["value"], math.pi / 4 * 13.5**2 * 15.5, rel_tol=1e-12)
    assert by["prop_static_swept_envelope"]["value"] == 52.17
    assert "STATIC" in by["prop_static_swept_envelope"]["note"]


def test_release_refuses_while_pending():
    p = subprocess.run([sys.executable, str(ROOT / "cad/fixture_contract.py"), "--release"], capture_output=True, text=True)
    assert p.returncode == 2 and "REFUSED" in p.stderr and "motor_mount_pattern" in p.stderr and "load_cell_mount_spacing" in p.stderr


def test_filling_a_pending_row_makes_its_clause_evaluable_positive_control(tmp_path):
    def fill(rows):
        for r in rows:
            if r["parameter"] == "stand_anchor_spacing":
                r["value"], r["evidence_state"], r["source"] = "120", "inspection", "synthetic bench measurement"
    c = FC.build(FC.load_register(_write_register(tmp_path, fill)))
    assert "stand_anchor_pattern" in c["evaluable_clauses"] and len(c["pending_clauses"]) == 9


def test_filling_every_pending_row_still_refuses_release_on_unconfirmed_vendor_nominals(tmp_path):
    # Positive control for the second gate: geometry can be complete while the delivered
    # parts are still unconfirmed. Vendor nominal is not inspection.
    def fill_all(rows):
        for r in rows:
            if r["evidence_state"] == "pending":
                r["value"], r["evidence_state"], r["source"] = "1", "inspection", "synthetic"
    reg_path = _write_register(tmp_path, fill_all)
    c = FC.build(FC.load_register(reg_path))
    assert not c["pending_clauses"]
    p = subprocess.run([sys.executable, str(ROOT / "cad/fixture_contract.py"), "--release", "--parameters", str(reg_path)], capture_output=True, text=True)
    assert p.returncode == 2 and "vendor-nominal" in p.stderr


def test_pending_row_carrying_a_value_is_refused(tmp_path):
    def poison(rows):
        for r in rows:
            if r["parameter"] == "load_cell_capacity": r["value"] = "50"
    with pytest.raises(FC.ContractInputError, match="pending parameter carries a value"):
        FC.load_register(_write_register(tmp_path, poison))


def test_unit_mismatch_missing_row_and_nonnumeric_are_refused(tmp_path):
    def bad_unit(rows):
        for r in rows:
            if r["parameter"] == "prop_diameter": r["unit"] = "in"
    with pytest.raises(FC.ContractInputError, match="unit mismatch"):
        FC.load_register(_write_register(tmp_path, bad_unit))
    def drop(rows): rows[:] = [r for r in rows if r["parameter"] != "motor_body_length"]
    with pytest.raises(FC.ContractInputError, match="missing from register"):
        FC.load_register(_write_register(tmp_path, drop))
    def text(rows):
        for r in rows:
            if r["parameter"] == "motor_body_diameter": r["value"] = "thirteen"
    with pytest.raises(FC.ContractInputError, match="non-numeric"):
        FC.load_register(_write_register(tmp_path, text))


def test_geometrically_impossible_inputs_are_refused(tmp_path):
    def shrink_prop(rows):
        for r in rows:
            if r["parameter"] == "prop_diameter": r["value"] = "10"
    with pytest.raises(FC.ContractInputError, match="does not clear"):
        FC.build(FC.load_register(_write_register(tmp_path, shrink_prop)))


def test_stale_committed_contract_is_detected(tmp_path):
    def bump(rows):
        for r in rows:
            if r["parameter"] == "motor_body_length": r["value"] = "16.0"
    reg_path = _write_register(tmp_path, bump)
    p = subprocess.run([sys.executable, str(ROOT / "cad/fixture_contract.py"), "--check", "--parameters", str(reg_path)], capture_output=True, text=True)
    assert p.returncode == 1 and "STALE" in p.stderr


def test_cli_check_passes_on_committed_state():
    p = subprocess.run([sys.executable, str(ROOT / "cad/fixture_contract.py"), "--check"], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
