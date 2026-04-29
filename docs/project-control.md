# Project Control

## Current Phase

Fase 2 — Dataset Audit

## Status

Fase 1 literature review has been merged to `main` via PR #1 and approved with final score 92/100. Fase 2 Dataset Audit artifacts have been generated and are pending Codex review. BoT-IoT access was verified via official UNSW/GitHub sources, and a practical Hugging Face CSV mirror was audited locally. Main finding: DoS/DDoS rows are available, but normal traffic is extremely underrepresented and feature-similarity leakage risk must be disclosed before modeling.

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

## Review Status

| Phase | Reviewer | Score | Verdict | File |
|---|---|---:|---|---|
| 0A/0B | Codex Lecturer Reviewer | 83 | NEEDS REVISION | `docs/REVIEW_phase0b.md` |
| 0A/0B revision | Codex Lecturer Reviewer | 91 | APPROVED | `docs/REVIEW_phase0b_final.md` |
| 0A/0B strict re-review | Codex gpt-5.5 + high reasoning | 90 | APPROVED | `docs/REVIEW_phase0_gpt55_high.md` |
| 1 | Codex Lecturer Reviewer | 88 | APPROVED | `docs/REVIEW_phase1_literature.md` |
| 1 final verification | Codex gpt-5.5 + high reasoning | 92 | APPROVED | `docs/REVIEW_phase1_literature_final_approved.md` |
| 2 | Codex gpt-5.5 + high reasoning | 89 | APPROVED | `docs/REVIEW_phase2_dataset_audit.md` |

## Blockers

Fase 2 review APPROVED with required sync fixes applied. Technical watch items for Fase 3: normal class is extremely small, network identifiers must be excluded, duplicate model-feature signatures are high, and train/test feature-signature overlap must be disclosed as split-similarity risk.

## Next Action

1. Commit and open PR `phase-2-dataset-audit`.
2. Merge after user approval.
3. After merge, run post-merge status sync and proceed to Fase 3 EDA & Preprocessing.
