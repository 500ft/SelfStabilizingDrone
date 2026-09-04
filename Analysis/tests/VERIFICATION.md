# Verification record — test_results_numbers.py

Provenance for the numbers quoted in the commit message and pull request, recorded
because an earlier revision of that message asserted the full-suite result before the
run that produced it had happened.

| check | result | when |
|---|---|---|
| `Analysis.tests.test_results_numbers` (4 tests) | OK | after the historical-marker exemption |
| `unittest discover -s Analysis/tests` (73 tests) | **OK, 73/73**, 108 s | on commit `947e7b6`, i.e. the pushed tree |

Negative controls, each producing 2 failures in the new module:

- reintroducing the superseded `T_required_total = 2.0 * 155 g = 310 g` derivation in
  `Design Report/calculations.md`;
- adding 10 g to a `worst_g` row in `Engineering Data/mass_budget.csv`.

The first full-suite run in this work happened *before* the historical-marker exemption
was added and reported 1 failure — `BOM.md`'s "vs the prior 129.76 g", a correct
historical reference that the first version of the test wrongly flagged. That failure is
what motivated the exemption. The 73/73 above is the post-exemption run on the pushed
commit, not that earlier one.
