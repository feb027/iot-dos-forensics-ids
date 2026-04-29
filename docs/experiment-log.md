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

## 2026-04-29 — PR #3 merged and Fase 4 prepared

- Final Codex verification for Fase 3: `docs/REVIEW_phase3_final_verification.md`, score 92/100, verdict APPROVED, merge recommendation MERGE.
- Merged PR #3 (`phase-3-eda-preprocessing`) into `main`.
- Merge commit: `dfd8def0f0b5ff5205f3da0d25aa82b073bbf3b9`.
- Current phase updated to Fase 4 Baseline Modeling.
- Carry-forward constraints: exclude leakage/network identifier columns, keep `other_attack` out of primary binary baseline, use imbalanced and balanced controlled tracks, and avoid accuracy-only claims.

## 2026-04-29 — Fase 4 Baseline Modeling artifacts generated

- Ran `scripts/run_baseline_modeling.py` using Track A realistic imbalanced, Track B balanced 1:1, and Track C controlled 1:2.
- Completed 14 model runs across Dummy Majority, Gaussian Naive Bayes, SGD Logistic Regression, Decision Tree, and Random Forest.
- Generated baseline metrics, confusion matrices, dataset-track tables, and figures under `results/`.
- Updated dashboard data from real baseline artifacts; feature importance remains empty until Fase 5 forensic analysis.
- Key interpretation rule: accuracy is not the primary claim; use macro F1, MCC, balanced accuracy, recall normal/attack, and FP/FN discussion.
- Codex technical review Fase 4 approved: `docs/REVIEW_phase4_baseline_modeling.md`, score 90/100. Post-review sync fixes applied to README and dashboard hero text.

## 2026-04-29 — PR #4 merged and Fase 5 prepared

- Merged PR #4 (`phase-4-baseline-modeling`) into `main`.
- Merge commit: `8ae010124316f786ddaf2b56492a2a4cc3429775`.
- Current phase updated to Fase 5 Forensic Analysis.
- Carry-forward constraints: interpret high baseline scores carefully, keep feature importance artifact-backed, discuss FP/FN, and disclose normal-class/split-similarity limitations.

## 2026-04-29 — Fase 5 Forensic Analysis artifacts generated

- Ran `scripts/run_forensic_analysis.py` using selected baseline runs from Track A/B/C.
- Generated feature importance, permutation importance, FP/FN summaries, and example rows under `results/`.
- Top feature groups: N_IN_Conn_P_DstIP, N_IN_Conn_P_SrcIP, stddev, srate, mean.
- Selected-runs errors: FP=2, FN=17.
- Updated dashboard data to include forensic feature importance and error analysis.
- Codex review Fase 5 approved: `docs/REVIEW_phase5_forensic_analysis.md`, score 90/100. Follow-up fixes applied: README wording, review status sync, and stronger regression tests for leakage, permutation importance, and FP/FN consistency.

## 2026-04-29 — Fase 6A Advanced Modeling branch initialized

- PR #5 Fase 5 merged to `main`.
- Created branch `phase-6a-advanced-modeling`.
- Added advanced modeling plan and local WSL run guide.
- Implemented runner plan for LightGBM/XGBoost/CatBoost with sampled SHAP explainability.

## 2026-04-29 — Fase 6A Advanced/SOTA Modeling full run

- Ran `scripts/run_advanced_modeling.py --models all --tracks all --shap-sample 3000` on local WSL PC through reverse SSH tunnel.
- Completed 7 advanced runs.
- Best overall advanced run: `xgboost` on `C_balanced_controlled_1_to_2` with macro F1=0.9965, MCC=0.9930.
- Track A highlight: LightGBM macro F1=0.9885, Δ Macro F1 vs baseline=0.0218.
- Top SHAP feature group: `N_IN_Conn_P_DstIP`.
- Codex review Fase 6A approved: `docs/REVIEW_phase6a_advanced_modeling.md`, score 90/100. Minor follow-up applied: README dashboard wording and dashboard Track A highlight.

## 2026-04-29 — Post-merge Fase 6A status sync

- PR #6 Fase 6A Advanced/SOTA Modeling merged to `main`.
- Current phase updated to Fase 6 Dashboard Polish & Manuscript Preparation.
- Dashboard generator status updated to `Fase 6A merged; Fase 6 dashboard polish current`.
- Added `docs/phase6-dashboard-polish-plan.md`.

## 2026-04-29 — Fase 6 dashboard redesign prototype

- Created `docs/phase6-dashboard-design-brief.md` using UI/UX Pro Max guidance and design reference research.
- Redesigned static dashboard into dark SOC-style command center with sticky nav, KPI bento, Chart.js desktop charts, mobile fallback bars, interactive model tabs, confusion matrix selector, forensics/SHAP evidence, advanced Track A cards, and evidence accordion.
- Validated local preview with Playwright at 1440px and 375px: no JavaScript console errors and no horizontal overflow.

## 2026-04-29 — Fase 6 dashboard review fixes

- Codex dashboard review wrote `docs/REVIEW_phase6_dashboard.md` with score 86/100 NEEDS REVISION.
- Fixed class distribution desktop fallback visibility so Chart.js and fallback bars do not duplicate.
- Updated `docs/dashboard-spec.md` to match the approved dark SOC/cybersecurity dashboard direction and current data contract.
- Codex final verification wrote `docs/REVIEW_phase6_dashboard_final.md` with score 94/100 APPROVED / MERGE.

## 2026-04-29 — PR #7 dashboard polish merged

- PR #7 merged into `main` with merge commit `193e9ca3125070f056e43457e137984261bbb417`.
- Current phase updated to Fase 7 Scientific Manuscript.
- Dashboard generator status updated to `Fase 6 dashboard merged; Fase 7 manuscript current`.
- Added `docs/phase7-manuscript-plan.md` for the next phase.

## 2026-04-29 — GitHub Pages verified after Fase 6 merge

- GitHub Pages source remains `main` `/` and status is `built`.
- Live dashboard JSON returned HTTP 200 with status `Fase 6 dashboard merged; Fase 7 manuscript current`.
- Live dashboard page returned HTTP 200 at `https://feb027.github.io/iot-dos-forensics-ids/dashboard/`.

## 2026-04-29 — Fase 6B Interactive AI SOC Demo implemented

- Added modular demo frontend under `dashboard/demo.html`, `dashboard/styles/`, and `dashboard/scripts/`.
- Added generated demo artifacts: `demo-scenarios.json`, `demo-feature-ranges.json`, `demo-narrative-templates.json`.
- Added FastAPI backend under `backend/iot_soc_api/` with health, scenario, predict, SOC analyze, flow analyze, and constrained chat endpoints.
- Deployed prototype to `https://iot.aquarise.my.id/soc-demo/demo.html` with PM2 process `iot-dos-soc-demo-api`.
- Caddy route applied at runtime via `/tmp/Caddyfile.iot-soc-demo`; persistent `/etc/caddy/Caddyfile` update needs sudo if service restarts.

