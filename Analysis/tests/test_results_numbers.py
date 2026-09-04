# Gate every hand-written mass number in the documents against Analysis/budget.py.
#
# Why this exists: the rollup drifted once already. Commit 52f4eaa updated
# Engineering Data/mass_budget.csv and Design Report/BOM.md together and left
# Analysis/current-results.md and Design Report/calculations.md stating the previous
# figures, so two documents disagreed with the committed script for weeks. A later edit
# to current-results.md did not touch its table, which is why edit recency is not a
# freshness signal and a test is.
#
# The derived numbers matter as much as the rollup: the static thrust requirement is
# 2.0 x the frozen maximum, so a stale maximum silently understates required thrust.

import re
import unittest
from pathlib import Path

from Analysis.budget import load_mass_budget, rollup

ROOT = Path(__file__).resolve().parents[2]

# Numbers each document is expected to state, and numbers that must NOT appear because
# they belong to a superseded rollup. Values are computed from budget.py, never typed.
DOCS = (
    "Analysis/current-results.md",
    "Design Report/calculations.md",
    "Design Report/BOM.md",
)

# Superseded rollup (worst = 149.5 g), kept explicit so a regression names itself.
STALE_VALUES = (117.96, 129.76, 149.5, 154.5, 155.0, 310.0, 77.5, 64.9)

TOL = 1e-9


# A superseded value may legitimately appear when the text explicitly frames it as
# history -- BOM.md says "vs the prior 129.76 g", which is a correct description of the
# change, not a stale claim. The rule being enforced is "no document ASSERTS a
# superseded value as current", not "no document may mention its own history".
HISTORICAL = re.compile(
    r"\b(prior|previous(ly)?|was|were|formerly|superseded|corrected|used to|earlier|"
    r"before the|old)\b", re.IGNORECASE)


def numbers_in(text: str, skip_historical: bool = False) -> set:
    """Every number followed by a gram unit or standing in a table cell, as floats.

    Deliberately broad: a stale value should be caught wherever it is written, not only
    inside the tables. With skip_historical, lines that explicitly frame a number as a
    past value are ignored.
    """
    found = set()
    for line in text.splitlines():
        if skip_historical and HISTORICAL.search(line):
            continue
        for m in re.finditer(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?:g\b|gf\b|\|)", line):
            found.add(float(m.group(1)))
    return found


class TestResultsNumbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = rollup(load_mass_budget())
        cls.frozen = float(cls.r["proposed_frozen_max_g"])

    def _read(self, rel):
        p = ROOT / rel
        self.assertTrue(p.is_file(), f"missing document: {rel}")
        return p.read_text(encoding="utf-8")

    def test_no_document_states_a_superseded_value(self):
        for rel in DOCS:
            present = numbers_in(self._read(rel), skip_historical=True)
            for stale in STALE_VALUES:
                # 156.0 is a live worst-case value; only flag a stale number if the
                # current rollup does not legitimately produce it.
                live = any(abs(stale - float(v)) < TOL
                           for v in (self.r["best_g"], self.r["nominal_g"], self.r["worst_g"],
                                     self.frozen, self.r["nominal_margin_g"]))
                if live:
                    continue
                self.assertFalse(
                    any(abs(stale - v) < TOL for v in present),
                    f"{rel} states {stale:g}, which belongs to a superseded mass rollup; "
                    f"regenerate from Analysis/budget.py",
                )

    def test_rollup_values_appear_where_they_are_tabulated(self):
        expected = {
            "best": float(self.r["best_g"]),
            "nominal": float(self.r["nominal_g"]),
            "worst": float(self.r["worst_g"]),
            "frozen maximum": self.frozen,
        }
        for rel in DOCS:
            present = numbers_in(self._read(rel))
            for name, want in expected.items():
                self.assertTrue(
                    any(abs(want - v) < TOL for v in present),
                    f"{rel} does not state the current {name} value {want:g} g",
                )

    def test_static_thrust_requirement_follows_the_frozen_maximum(self):
        text = self._read("Design Report/calculations.md")
        total = 2.0 * self.frozen
        per_motor = total / 4.0
        present = numbers_in(text)
        self.assertTrue(
            any(abs(total - v) < TOL for v in present),
            f"calculations.md does not state the derived total thrust requirement "
            f"2.0 x {self.frozen:g} g = {total:g} g",
        )
        self.assertTrue(
            any(abs(per_motor - v) < TOL for v in present),
            f"calculations.md does not state the derived per-motor requirement "
            f"{total:g} g / 4 = {per_motor:g} g",
        )

    def test_abort_threshold_claim_holds(self):
        # Mass-independent by construction, but assert it rather than assume it.
        self.assertTrue(self.r["below_abort_threshold"])
        self.assertLessEqual(self.frozen, 225.0)


if __name__ == "__main__":
    unittest.main()
