# Project Control

## Current Phase

Fase 3 — EDA & Preprocessing

## Status

Fase 2 Dataset Audit has been merged to `main` via PR #2 and approved with score 89/100. Fase 3 EDA & Preprocessing artifacts have been generated, reviewed, and final-verified by Codex with score 92/100. The phase defines filtered binary logic, leakage-safe feature handling, EDA tables/figures, and imbalanced/balanced dataset tracks for Fase 4 baseline modeling. Main carried-forward risks: normal class is extremely underrepresented, network identifiers must be excluded, duplicate feature signatures are high, and split-similarity risk must be disclosed.

## Fixed Decisions

| Item | Decision |
|---|---|
| Repo | `iot-dos-forensics-ids` |
| Judul dosen | Sistem Analisis Serangan DoS pada Arsitektur IoT |
| Tema | IoT + Cyber Security + Digital Forensics |
| Dataset utama | BoT-IoT UNSW |
| Dataset alternatif | RT-IoT2022 UCI |
| Scope utama | Binary classification normal vs DoS/DDoS |
| Dashboard | Static GitHub Pages |
| Review | Codex lecturer/technical review per phase |

## Artifact Inventory

| Area | Path | Status |
|---|---|---|
| Agent instructions | `AGENTS.md` | created |
| Roadmap | `docs/roadmap.md` | created |
| Phase gates | `docs/phase-gates.md` | created |
| Workflow | `docs/workflow.md` | created |
| Prompts | `prompts/` | created |
| Literature matrix | `references/literature-matrix.md` | 18 sources; Fase 1 approved |
| Dashboard spec | `docs/dashboard-spec.md` | created |
| Experiment log | `docs/experiment-log.md` | template created |
| Codex project config | `.codex/config.toml` | gpt-5.5 + high reasoning configured |
| Fase 1 research log | `docs/research-log.md` | completed |
| Fase 1 progress report | `reports/progress-1-literature-review.md` | completed |
| BibTeX references | `references/references.bib` | 18 entries; validated |
| Fase 2 dataset notes | `docs/dataset-notes.md` | audit findings documented |
| Fase 2 access evidence | `docs/dataset-access-evidence.md` | completed |
| Fase 2 progress report | `reports/progress-2-dataset-audit.md` | drafted |
| Dataset audit script | `scripts/audit_botiot_dataset.py` | completed |
| Dataset audit metrics | `results/metrics/dataset_audit.json` | generated |
| Dataset audit tables | `results/tables/dataset_files.csv`, `results/tables/class_distribution.csv`, `results/tables/column_profile.csv`, `results/tables/split_leakage_checks.csv` | generated |
| Fase 3 EDA script/notebook | `scripts/run_eda_preprocessing.py`, `notebooks/01_eda_preprocessing.ipynb` | generated |
| Fase 3 method notes | `docs/phase3-method-notes.md` | completed |
| Fase 3 progress report | `reports/progress-3-eda-preprocessing.md` | drafted |
| Fase 3 preprocessing summary | `results/metrics/preprocessing_summary.json` | generated |
| Fase 3 EDA tables | `results/tables/eda_*.csv`, `results/tables/preprocessing_*_plan.csv` | generated |
| Fase 3 label consistency checks | `results/tables/eda_label_consistency_checks.csv` | 0 violations |
| Fase 3 EDA figures | `results/figures/eda_*.png` | generated |

## Review Status

| Phase | Reviewer | Score | Verdict | File |
|---|---|---:|---|---|
| 0A/0B | Codex Lecturer Reviewer | 83 | NEEDS REVISION | `docs/REVIEW_phase0b.md` |
| 0A/0B revision | Codex Lecturer Reviewer | 91 | APPROVED | `docs/REVIEW_phase0b_final.md` |
| 0A/0B strict re-review | Codex gpt-5.5 + high reasoning | 90 | APPROVED | `docs/REVIEW_phase0_gpt55_high.md` |
| 1 | Codex Lecturer Reviewer | 88 | APPROVED | `docs/REVIEW_phase1_literature.md` |
| 1 final verification | Codex gpt-5.5 + high reasoning | 92 | APPROVED | `docs/REVIEW_phase1_literature_final_approved.md` |
| 2 | Codex gpt-5.5 + high reasoning | 89 | APPROVED | `docs/REVIEW_phase2_dataset_audit.md` |
| 3 | Codex gpt-5.5 + high reasoning | 88 | APPROVED | `docs/REVIEW_phase3_eda_preprocessing.md` |
| 3 final verification | Codex gpt-5.5 + high reasoning | 92 | APPROVED / MERGE | `docs/REVIEW_phase3_final_verification.md` |

## Blockers

Fase 3 review APPROVED and follow-up fixes applied. Watch items for Fase 4: normal class is extremely small, network identifiers must remain excluded, duplicate model-feature signatures are high, and train/test feature-signature overlap must be disclosed as split-similarity risk.

## Next Action

1. Commit and open PR `phase-3-eda-preprocessing`.
2. Merge after user approval.
3. After merge, run post-merge status sync and proceed to Fase 4 Baseline Modeling.
