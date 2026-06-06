import csv
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]


class RepositoryTests(unittest.TestCase):
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
