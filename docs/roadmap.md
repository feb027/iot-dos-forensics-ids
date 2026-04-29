# Roadmap Proyek

## Fase 0A — Agent & Workflow Scaffold

Tujuan: menyiapkan operating model Hermes + Codex, review gate, prompt template, dan aturan proyek.

Status: completed and governed by review gate.

## Fase 0B — Repository Setup

Tujuan: membuat repo GitHub, struktur folder, README, `.gitignore`, docs dasar, dan initial commit.

Deliverables:

- GitHub repo
- Folder structure
- README
- AGENTS.md
- Docs/prompt templates
- Initial commit pushed

## Fase 1 — Literature Review

Tujuan: mengumpulkan 10–15 referensi relevan tentang IoT security, IDS, DoS/DDoS, BoT-IoT, RT-IoT2022, dan network forensics.

Status: completed — final review 92/100 APPROVED.

## Fase 2 — Dataset Audit

Tujuan: memverifikasi akses dataset, label, fitur, ukuran, kelas DoS/DDoS, risiko imbalance, dan risiko leakage.

Status: completed — Codex review 89/100 APPROVED.

## Fase 3 — EDA & Preprocessing

Tujuan: eksplorasi dataset, cleaning, encoding, split strategy, dan visualisasi awal.

Status: completed — final verification 92/100 APPROVED; merged via PR #3.

## Fase 4 — Baseline Modeling

Tujuan: melatih minimal 3 model baseline dan menyimpan metrik evaluasi.

Status: completed — Codex technical review 90/100 APPROVED; merged via PR #4.

## Fase 5 — Forensic Analysis

Tujuan: menganalisis fitur penting, confusion matrix, dan interpretasi pola DoS/DDoS.

Status: completed and merged via PR #5 — Codex review 90/100 APPROVED.

## Fase 6A — Advanced/SOTA Modeling Extension

Tujuan: membandingkan model tabular modern seperti LightGBM/XGBoost/CatBoost terhadap baseline Fase 4 dan menambahkan explainability sampel untuk memperkuat interpretasi forensik.

Status: completed and merged via PR #6 — Codex review 90/100 APPROVED.

## Fase 6 — Dashboard

Tujuan: membangun static dashboard untuk menampilkan dataset summary, model performance, confusion matrix, feature importance, forensic interpretation, dan advanced modeling highlight.

Status: current phase after PR #6 merge; dashboard exists and needs final polish/Pages verification.

## Fase 7 — Scientific Manuscript

Tujuan: menulis naskah ilmiah final berbasis artifact proyek.

## Fase 8 — Final Audit & Release

Tujuan: audit repo, laporan, dashboard, referensi, artifact, dan kesiapan submit.
