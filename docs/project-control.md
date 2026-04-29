# Project Control

## Current Phase

Fase 6 — Dashboard Polish & Manuscript Preparation

## Status

Fase 4 Baseline Modeling has been merged to `main` via PR #4, Fase 5 Forensic Analysis has been merged via PR #5, and Fase 6A Advanced/SOTA Modeling Extension has been merged via PR #6. Advanced artifacts are available and approved by Codex reviewer with score 90/100. Current work moves to Fase 6 Dashboard Polish and manuscript preparation. Main carried-forward risks: very high model scores must be explained cautiously because normal class is tiny, network identifiers remain excluded, split-similarity risk must be disclosed, and global SHAP aggregation must be distinguished from Track A-specific SHAP interpretation.

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
| Fase 4 baseline runner | `scripts/run_baseline_modeling.py`, `notebooks/02_baseline_modeling.ipynb` | generated |
| Fase 4 method notes | `docs/phase4-method-notes.md` | completed |
| Fase 4 local run guide | `docs/phase4-local-run-guide.md` | completed |
| Fase 4 progress report | `reports/progress-4-baseline-modeling.md` | drafted |
| Fase 4 baseline summary | `results/metrics/baseline_summary.json` | generated |
| Fase 4 baseline tables | `results/tables/baseline_*.csv` | generated |
| Fase 4 baseline figures | `results/figures/baseline_*.png` | generated |
| Fase 5 plan | `docs/phase5-plan.md` | drafted |
| Fase 5 forensic runner | `scripts/run_forensic_analysis.py`, `notebooks/03_forensic_analysis.ipynb` | generated |
| Fase 5 method notes | `docs/phase5-method-notes.md` | completed |
| Fase 5 progress report | `reports/progress-5-forensic-analysis.md` | drafted |
| Fase 5 forensic summary | `results/metrics/forensic_summary.json` | generated |
| Fase 5 forensic tables | `results/tables/forensic_*.csv` | generated |
| Fase 5 forensic figures | `results/figures/forensic_*.png` | generated |
| Fase 6A advanced plan | `docs/phase6a-advanced-modeling-plan.md` | drafted |
| Fase 6A local run guide | `docs/phase6a-local-run-guide.md` | drafted |
| Fase 6A advanced runner | `scripts/run_advanced_modeling.py`, `notebooks/04_advanced_modeling.ipynb` | generated |
| Fase 6A advanced summary | `results/metrics/advanced_summary.json` | generated |
| Fase 6A advanced tables | `results/tables/advanced_*.csv` | generated |
| Fase 6A advanced figures | `results/figures/advanced_*.png` | generated |
| Fase 6A progress report | `reports/progress-6a-advanced-modeling.md` | completed |
| Fase 6 dashboard polish plan | `docs/phase6-dashboard-polish-plan.md` | drafted |
| Fase 6 dashboard design brief | `docs/phase6-dashboard-design-brief.md` | drafted |

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
| 4 | Codex Technical Reviewer | 90 | APPROVED | `docs/REVIEW_phase4_baseline_modeling.md` |
| 5 | Codex Technical/Lecturer Reviewer | 90 | APPROVED | `docs/REVIEW_phase5_forensic_analysis.md` |
| 6A | Codex Technical/Lecturer Reviewer | 90 | APPROVED | `docs/REVIEW_phase6a_advanced_modeling.md` |

## Blockers

No active blockers. Watch items for Fase 6/7: verify GitHub Pages after status sync, keep dashboard claims tied to artifact JSON/CSV, emphasize Track A realistic highlight, and keep manuscript language cautious around controlled-subset scores.

## Next Action

1. Review redesigned dashboard visuals on branch `phase-6-dashboard-polish`.
2. Run Codex dashboard review gate after user approves the visual direction.
3. Open/merge Fase 6 dashboard polish PR after review fixes.
4. Draft manuscript sections from committed artifact tables/figures only.
