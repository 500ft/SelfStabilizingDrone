#!/usr/bin/env python3
"""Generate the traceable subsystem report from validated research JSON."""

import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def uncertain(value, field: str, record: dict) -> bool:
    if field in record.get("uncertain", []):
        return True
    return isinstance(value, str) and "[uncertain]" in value


def render(value) -> str:
    if isinstance(value, list):
        if value and isinstance(value[0], dict):
            return "\n".join(
                f"- " + " | ".join(f"{key}: {item}" for key, item in row.items())
                for row in value
            )
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return "; ".join(f"{key}: {item}" for key, item in value.items())
    return str(value)


def main() -> None:
    fields_doc = yaml.safe_load((ROOT / "fields.yaml").read_text())
    fields = [
        field["name"]
        for category in fields_doc["field_categories"]
        for field in category["fields"]
    ]
    records = [json.loads(path.read_text()) for path in sorted(RESULTS.glob("*.json"))]

    lines = [
        "# Weight-Unrestricted Component Research",
        "",
        "Generated from the validated JSON evidence register. Fields explicitly marked uncertain are omitted here and remain visible in `results/`.",
        "",
        "## Contents",
        "",
    ]
    for index, record in enumerate(records, 1):
        name = record["subsystem"]
        lines.append(f"{index}. [{name}](#{slug(name)})")

    for record in records:
        name = record["subsystem"]
        lines.extend(["", f"## {name}", ""])
        for field in fields:
            if field == "subsystem" or field not in record:
                continue
            value = record[field]
            if value in (None, "", []) or uncertain(value, field, record):
                continue
            title = field.replace("_", " ").title()
            lines.extend([f"### {title}", "", render(value), ""])

    (ROOT / "report.md").write_text("\n".join(lines).rstrip() + "\n")


if __name__ == "__main__":
    main()
