# Project Agent Instructions

## Project Identity

Project: **Sistem Analisis Serangan DoS pada Arsitektur IoT**

Theme: **IoT + Cyber Security + Digital Forensics**

Primary dataset: **BoT-IoT (UNSW)** — https://research.unsw.edu.au/projects/bot-iot-dataset

Alternative dataset: **RT-IoT2022 (UCI)** — https://archive-beta.ics.uci.edu/dataset/942/rt-iot2022

Working title:

**Sistem Analisis Serangan DoS pada Trafik IoT Berbasis Machine Learning dan Network Forensics Menggunakan Dataset BoT-IoT**

## Agent Roles

- Hermes: orchestrator, verifier, project manager.
- Codex Implementer: code, notebooks, dashboard, docs scaffolding.
- Codex Lecturer Reviewer: acts as IoT + Cyber Security + Digital Forensics lecturer.
- Codex Technical Reviewer: checks reproducibility, leakage, metrics, code quality, and dashboard consistency.
- Paper Writer: writes natural Indonesian academic text.
- Final Examiner: audits whole repo before submission.

## Non-Negotiable Rules

1. Do not invent experiment results.
2. Do not invent dataset statistics.
3. Do not invent citations, DOI, or paper claims.
4. Every quantitative claim must come from a committed artifact, script output, dataset inspection, or cited source.
5. If data or result is unavailable, write `TODO` or `limitation`; never guess.
6. Do not commit secrets, tokens, credentials, raw large datasets, full PCAP files, or large model binaries.
7. Commit important evidence artifacts: `results/tables/`, `results/figures/`, `results/metrics/`, and generated dashboard data.
8. Update documentation after every phase.
9. Keep Indonesian academic writing natural, clear, and suitable for an Informatics semester 6 student.
10. Use `Gambar` and `Tabel` labels in Indonesian reports.

## Workflow

Every phase follows:

```text
plan → execute → artifact → docs → Codex review → fix → commit → next phase
```

Do not proceed to the next phase if:

- critical review issues remain,
- artifacts are missing,
- documentation is stale,
- claims are unsupported,
- dataset/metric definitions are unclear.

## Review Gate

Minimum passing gate:

- Score >= 85
- Verdict: `APPROVED`
- No critical issue

Preferred gate:

- Score >= 90

## Git Rules

- Use clear conventional-style commit messages.
- Keep commits phase-based.
- For future work after scaffold, prefer phase branches such as `phase-1-literature-review`; direct commits to `main` are only acceptable for small scaffold/admin fixes explicitly requested by the user.
- Do not commit ignored data/model files.
- Before finalizing, run relevant checks and inspect `git status -sb`.

Suggested commit messages:

```text
docs: initialize IoT DoS project scaffold
research: add literature review matrix
data: document BoT-IoT dataset audit
analysis: add EDA outputs
model: add baseline classifier comparison
forensics: add feature importance analysis
dashboard: add static results dashboard
paper: add final scientific manuscript
```

## Dataset Rules

- Store raw datasets under `data/raw/` only; this directory is ignored.
- Store processed large datasets under `data/processed/`; this directory is ignored except `.gitkeep`.
- Small safe samples may be stored under `data/sample/`.
- Always document dataset source, download/access method, label mapping, and class distribution.

## Dashboard Rules

- Prefer static GitHub Pages dashboard.
- Dashboard must read generated JSON/CSV artifacts, not hardcoded manually copied results.
- Dashboard claims must match `results/tables/` and `results/metrics/`.
- Keep design clean, academic, white/light background, readable charts.

## Academic Writing Rules

- Use Indonesian natural academic style.
- Avoid over-polished AI tone.
- Explain technical terms clearly.
- Use citations for theoretical claims.
- Use placeholders instead of fabricated results when artifacts are not ready.
- Foreign technical terms in Markdown prose should use italic asterisks when appropriate.

## Current Known Commands

```bash
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 scripts/generate_dashboard_data.py
python3 -m http.server 8000 -d dashboard
```

Some commands may become active after scripts/tests are added.
