#!/usr/bin/env python3
"""Confidence-bound helpers for launch-classifier testing."""

from __future__ import annotations

import math


def zero_event_upper_bound(trials: int, confidence: float = 0.95) -> float:
    """Exact one-sided binomial upper bound when zero events are observed."""
    if trials <= 0:
        raise ValueError("trials must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between zero and one")
    return 1.0 - (1.0 - confidence) ** (1.0 / trials)


def required_zero_event_trials(max_rate: float, confidence: float = 0.95) -> int:
    if not 0.0 < max_rate < 1.0:
        raise ValueError("max_rate must be between zero and one")
    return math.ceil(math.log(1.0 - confidence) / math.log(1.0 - max_rate))


def main() -> None:
    for trials in (300, 1000):
        bound = zero_event_upper_bound(trials)
        print(f"0 events / {trials} trials -> 95% upper bound = {bound * 100:.3f}%")
    for rate in (0.01, 0.003):
        print(
            f"Trials required for {rate * 100:.3f}% bound with zero events: "
            f"{required_zero_event_trials(rate)}"
        )


if __name__ == "__main__":
    main()
