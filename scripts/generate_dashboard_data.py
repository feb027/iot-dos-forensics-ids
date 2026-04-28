from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dashboard" / "data" / "dashboard-data.json"


def main() -> None:
    data = {
        "project": {
            "title": "Sistem Analisis Serangan DoS pada Arsitektur IoT",
            "theme": "IoT + Cyber Security + Digital Forensics",
            "primary_dataset": "BoT-IoT (UNSW)",
            "alternative_dataset": "RT-IoT2022 (UCI)",
            "status": "Scaffold created; experiment results pending"
        },
        "dataset_summary": {},
        "class_distribution": [],
        "model_comparison": [],
        "confusion_matrix": {},
        "feature_importance": [],
        "forensic_notes": [
            "Hasil forensik akan diisi setelah feature importance dan error analysis tersedia."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
