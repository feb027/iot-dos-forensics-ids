# Project Control

## Current Phase

Fase 2 — Dataset Audit

## Status

Fase 1 literature review has been merged to `main` via PR #1 and approved with final score 92/100. Current work is Fase 2 Dataset Audit: verify BoT-IoT access, usable subset/format, label mapping, DoS/DDoS class availability, feature list, missing values, class imbalance, leakage risk, and split strategy before any modeling.

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
| Fase 2 dataset notes | `docs/dataset-notes.md` | audit checklist ready |

## Review Status

| Phase | Reviewer | Score | Verdict | File |
|---|---|---:|---|---|
| 0A/0B | Codex Lecturer Reviewer | 83 | NEEDS REVISION | `docs/REVIEW_phase0b.md` |
| 0A/0B revision | Codex Lecturer Reviewer | 91 | APPROVED | `docs/REVIEW_phase0b_final.md` |
| 0A/0B strict re-review | Codex gpt-5.5 + high reasoning | 90 | APPROVED | `docs/REVIEW_phase0_gpt55_high.md` |
| 1 | Codex Lecturer Reviewer | 88 | APPROVED | `docs/REVIEW_phase1_literature.md` |
| 1 final verification | Codex gpt-5.5 + high reasoning | 92 | APPROVED | `docs/REVIEW_phase1_literature_final_approved.md` |

## Blockers

None yet. Watch items for Fase 2: BoT-IoT full dataset is large, raw PCAP/CSV must not be committed, and dataset statistics must come only from inspected files/subsets.

## Next Action

1. Create branch `phase-2-dataset-audit`.
2. Verify BoT-IoT access/download method and decide usable subset.
3. Produce dataset audit artifacts: label mapping, feature list, missing values, class distribution, leakage checklist, and split strategy.
4. Run Codex review before moving to EDA/modeling.
