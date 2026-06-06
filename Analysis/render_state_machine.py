#!/usr/bin/env python3
"""Render Mermaid state transitions from the authoritative JSON source."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Controls" / "state_machine.json"


def render(source: Path = SOURCE) -> str:
    data = json.loads(source.read_text(encoding="utf-8"))
    lines = ["stateDiagram-v2", f"    [*] --> {data['initial']}"]
    for transition in data["transitions"]:
        label = transition["trigger"].replace(" ", "_")
        lines.append(f"    {transition['from']} --> {transition['to']}: {label}")
    return "\n".join(lines)


def main() -> None:
    print(render())


if __name__ == "__main__":
    main()
