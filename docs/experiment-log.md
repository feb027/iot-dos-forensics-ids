# Experiment Log

## Template Eksperimen

### Eksperimen 001

- Tanggal:
- Dataset:
- Target label:
- Fitur:
- Preprocessing:
- Model:
- Parameter:
- Train/test split:
- Accuracy:
- Precision:
- Recall:
- F1-score:
- Artifact:
- Catatan:
- Keputusan lanjut:
## 2026-04-29 — Fase 2 Dataset Audit

- Ran `python3 scripts/audit_botiot_dataset.py` against `data/raw/bot-iot-hf/train.csv` and `data/raw/bot-iot-hf/test.csv`.
- Generated dataset audit artifacts under `results/metrics/` and `results/tables/`.
- Key finding: DoS/DDoS rows are available, but normal class is extremely small and must be handled carefully in Fase 3.
- No model training was performed in this phase.
- Codex review Fase 2 approved: `docs/REVIEW_phase2_dataset_audit.md`, score 89/100. Required sync fixes applied before PR.

## 2026-04-29 — PR #2 merged and Fase 3 prepared

- Merged PR #2 (`phase-2-dataset-audit`) into `main`.
- Merge commit: `6cf268254651d76167ae6095a859f103c1adcc29`.
- Current phase updated to Fase 3 EDA & Preprocessing.
- Carry-forward constraints: exclude leakage/identifier columns, handle extreme normal-class imbalance, and document split-similarity risk.
## 2026-04-29 — Fase 3 EDA artifacts generated

- Ran `python3 scripts/run_eda_preprocessing.py` against `data/raw/bot-iot-hf/train.csv` and `data/raw/bot-iot-hf/test.csv`.
- Generated EDA tables under `results/tables/`, figures under `results/figures/`, and preprocessing summary JSON under `results/metrics/preprocessing_summary.json`.
- Added notebook wrapper `notebooks/01_eda_preprocessing.ipynb`.
- Key decision: Fase 4 must use imbalanced and balanced controlled tracks; `other_attack` is excluded from the primary binary baseline.
- No model training was performed in this phase.
- Codex review Fase 3 approved: `docs/REVIEW_phase3_eda_preprocessing.md`, score 88/100. Follow-up fixes applied: label consistency checks, stricter preprocessing tests, robust notebook path, and full A/B/C dashboard plan.
