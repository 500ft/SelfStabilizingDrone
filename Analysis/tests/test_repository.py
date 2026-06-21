import csv
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]

BOM = ROOT / "Design Report" / "BOM.csv"
MASS_BUDGET = ROOT / "Engineering Data" / "mass_budget.csv"
EVIDENCE_STATES = {"CONFIRMED", "INFERRED", "ASSUMED", "BENCH_REQUIRED", "BLOCKER"}
# Tokens that meant "not yet selected" before the 2026-06-20 Stage 1 lock.
# They must not reappear as a current selection in the canonical sources.
STALE_SELECTION_TOKENS = (
    "OpenMV",
    "ESP32",
    "Architecture not selected",
    "1103-class candidate",
    "H743 Mini",
)
NOMINAL_MASS_CEILING_G = 200.0


def _flying_bom_rows():
    with BOM.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if (row.get("Mass Nominal g") or "").strip():
                yield row


def _mass_budget_rows():
    with MASS_BUDGET.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class RepositoryTests(unittest.TestCase):
    def test_bom_and_mass_budget_nominal_totals_agree(self):
        bom_total = sum(float(row["Mass Nominal g"]) for row in _flying_bom_rows())
        budget_total = sum(float(row["nominal_g"]) for row in _mass_budget_rows())
        self.assertAlmostEqual(
            bom_total,
            budget_total,
            places=1,
            msg=f"BOM flying nominal {bom_total} g != mass budget nominal {budget_total} g",
        )

    def test_nominal_mass_below_planning_ceiling(self):
        budget_total = sum(float(row["nominal_g"]) for row in _mass_budget_rows())
        self.assertLess(budget_total, NOMINAL_MASS_CEILING_G, f"nominal mass {budget_total} g")

    def test_no_stale_selections_in_canonical_sources(self):
        offenders = []
        for path in (BOM, MASS_BUDGET):
            text = path.read_text(encoding="utf-8")
            for token in STALE_SELECTION_TOKENS:
                if token in text:
                    offenders.append(f"{path.relative_to(ROOT)} contains stale token '{token}'")
        self.assertEqual(offenders, [])

    def test_flying_bom_rows_have_locked_part_and_evidence_state(self):
        problems = []
        for row in _flying_bom_rows():
            if not (row.get("Locked Part") or "").strip():
                problems.append(f"{row.get('Item')}: missing Locked Part")
            state = (row.get("Evidence State") or "").strip()
            if state not in EVIDENCE_STATES:
                problems.append(f"{row.get('Item')}: invalid Evidence State '{state}'")
        self.assertEqual(problems, [])

    def test_local_markdown_links_exist(self):
        missing = []
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for document in ROOT.rglob("*.md"):
            for target in link_pattern.findall(document.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                clean_target = unquote(target.split("#", 1)[0])
                if not (document.parent / clean_target).resolve().exists():
                    missing.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual(missing, [])

    def test_engineering_register_headers(self):
        expected = {
            "requirements.csv": {"id", "requirement", "operator", "fixed_value", "units"},
            "estimates.csv": {"id", "parameter", "best", "nominal", "worst", "basis", "source"},
            "instrumentation.csv": {
                "measurement",
                "truth_source",
                "sample_rate",
                "resolution",
                "uncertainty",
                "synchronization",
                "calibration_method",
            },
            "fmea.csv": {
                "id",
                "failure_mode",
                "effect",
                "severity_1_5",
                "likelihood_1_5",
                "mitigation",
                "residual_risk",
            },
        }
        for filename, required in expected.items():
            path = ROOT / "Engineering Data" / filename
            with path.open(newline="", encoding="utf-8") as handle:
                headers = set(next(csv.reader(handle)))
            self.assertTrue(required.issubset(headers), f"{filename} missing {required - headers}")


if __name__ == "__main__":
    unittest.main()
