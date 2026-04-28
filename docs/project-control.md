# Project Control

## Current Phase

Fase 0B — Repository Setup

## Status

Fase 0A/0B approved. Initial repo, GitHub Pages, docs, prompts, tests, and scaffold are created and pushed.

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
| Literature matrix | `references/literature-matrix.md` | template created |
| Dashboard spec | `docs/dashboard-spec.md` | created |
| Experiment log | `docs/experiment-log.md` | template created |
| Codex project config | `.codex/config.toml` | gpt-5.5 + high reasoning configured |

## Review Status

| Phase | Reviewer | Score | Verdict | File |
|---|---|---:|---|---|
| 0A/0B | Codex Lecturer Reviewer | 83 | NEEDS REVISION | `docs/REVIEW_phase0b.md` |
| 0A/0B revision | Codex Lecturer Reviewer | 91 | APPROVED | `docs/REVIEW_phase0b_final.md` |
| 0A/0B strict re-review | Codex gpt-5.5 + high reasoning | 90 | APPROVED | `docs/REVIEW_phase0_gpt55_high.md` |

## Blockers

None yet.

## Next Action

1. Create branch `phase-1-literature-review`.
2. Start Fase 1 literature review.
3. Fill `docs/research-log.md` and `references/literature-matrix.md` in parallel.
4. Group references into dataset, IoT IDS, DoS/DDoS ML detection, leakage/evaluation methodology, and network forensics.
