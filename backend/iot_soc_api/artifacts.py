from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "dashboard" / "data"


@lru_cache(maxsize=1)
def load_demo_bundle() -> dict[str, Any]:
    path = DATA_DIR / "demo-scenarios.json"
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_ranges() -> dict[str, Any]:
    path = DATA_DIR / "demo-feature-ranges.json"
    return json.loads(path.read_text(encoding="utf-8"))


def find_scenario(scenario_id: str | None) -> dict[str, Any] | None:
    if not scenario_id:
        return None
    for scenario in load_demo_bundle().get("scenarios", []):
        if scenario.get("id") == scenario_id:
            return scenario
    return None
