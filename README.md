# IoT DoS Forensics IDS

Proyek UAS individu mata kuliah IoT Semester 6.

## Judul

**Sistem Analisis Serangan DoS pada Arsitektur IoT**

Judul kerja yang diperjelas:

**Sistem Analisis Serangan DoS pada Trafik IoT Berbasis Machine Learning dan Network Forensics Menggunakan Dataset BoT-IoT**

## Tema

IoT + Cyber Security + Digital Forensics

## Dataset

- Dataset utama: BoT-IoT (UNSW) — https://research.unsw.edu.au/projects/bot-iot-dataset
- Dataset alternatif: RT-IoT2022 (UCI) — https://archive-beta.ics.uci.edu/dataset/942/rt-iot2022

## Scope Awal

- Fokus utama: klasifikasi biner `normal` vs `DoS/DDoS`.
- Fokus tambahan jika waktu cukup: klasifikasi multi-kelas dan validasi pembanding dengan RT-IoT2022.
- Output utama: naskah ilmiah, eksperimen reproducible, grafik/tabel evaluasi, analisis forensik fitur, dan dashboard static GitHub Pages.

## Prinsip Proyek

- Evidence-first: setiap angka pada laporan harus berasal dari artifact atau referensi yang jelas.
- Tidak mengarang statistik dataset, hasil eksperimen, atau sitasi.
- Dataset besar tidak di-commit ke GitHub.
- Result penting seperti tabel, grafik, metrik, dan dashboard data ringkas di-commit.

## Struktur Repo

```text
docs/        Dokumentasi proyek, roadmap, log, dan spesifikasi
references/  Literatur dan BibTeX
notebooks/   Notebook EDA, preprocessing, modeling, dan forensic analysis
scripts/     Script reproducible untuk dataset, training, evaluasi, dashboard data
results/     Tabel, grafik, metrik, dan model output
dashboard/   Static dashboard untuk visualisasi hasil
reports/     Progress report dan naskah ilmiah
prompts/     Prompt template untuk Codex/Hermes workflow
```

## Dashboard Preview

GitHub Pages: https://feb027.github.io/iot-dos-forensics-ids/

Dashboard saat ini menampilkan ringkasan audit dataset Fase 2, EDA/preprocessing Fase 3, dan hasil baseline modeling Fase 4. Feature importance dan interpretasi forensik detail akan diperbarui setelah Fase 5 berjalan.

## Definition of Done

Proyek dianggap selesai jika:

- literature review berisi minimal 10–15 referensi relevan,
- dataset audit BoT-IoT jelas dan dapat direproduksi,
- EDA dan preprocessing terdokumentasi,
- minimal 3 model baseline dilatih dan dievaluasi,
- tabel/grafik/metrik tersimpan di `results/`,
- analisis forensik fitur tersedia,
- dashboard static menampilkan hasil dari artifact,
- naskah ilmiah final selesai dan sesuai artifact,
- final review menyatakan siap submit.

## Literature Review Snapshot

Fase 1 sudah selesai dan sudah di-*merge* ke `main` melalui PR #1. Ringkasan artefak:

- `references/literature-matrix.md`: 18 sumber.
- `references/references.bib`: 18 BibTeX entries.
- `docs/research-log.md`: log seleksi dan sintesis awal.
- `reports/progress-1-literature-review.md`: laporan progres Fase 1.
- Final review: `docs/REVIEW_phase1_literature_final_approved.md` — **92/100 APPROVED**.

Fase 1 sudah selesai; Fase 2 Dataset Audit juga sudah selesai dan di-*merge* ke `main` melalui PR #2.

## Dataset Audit Snapshot

Fase 2 Dataset Audit sudah selesai dan di-*merge* ke `main` melalui PR #2. Artifact awal dari BoT-IoT/UNSW-IoT CSV mirror:

- `scripts/audit_botiot_dataset.py`: script audit reproducible tanpa pandas.
- `results/metrics/dataset_audit.json`: ringkasan audit machine-readable.
- `results/tables/dataset_files.csv`: file, row count, checksum, duplicate summary.
- `results/tables/class_distribution.csv`: distribusi `attack`, `category`, `subcategory`, dan scope DoS/DDoS.
- `results/tables/column_profile.csv`: profil kolom dan missing values.
- `results/tables/split_leakage_checks.csv`: cek overlap train/test.
- `reports/progress-2-dataset-audit.md`: laporan progres Fase 2.

Temuan utama: DoS/DDoS tersedia, tetapi normal class sangat kecil dan ada risiko kemiripan fitur agregat antar split. Fase 3 harus memakai evaluasi yang tidak bergantung pada accuracy saja.

## EDA & Preprocessing Snapshot

Fase 3 EDA & Preprocessing sudah selesai dan di-*merge* ke `main` melalui PR #3. Artifact utama:

- `scripts/run_eda_preprocessing.py`: script EDA/preprocessing streaming untuk BoT-IoT/UNSW-IoT CSV split.
- `notebooks/01_eda_preprocessing.ipynb`: notebook wrapper untuk menjalankan script.
- `results/metrics/preprocessing_summary.json`: ringkasan machine-readable.
- `results/tables/eda_*.csv`: distribusi scope, kategori, protokol, dan ringkasan fitur numerik.
- `results/tables/eda_label_consistency_checks.csv`: validasi konsistensi label/scope.
- `results/tables/preprocessing_feature_plan.csv`: kolom fitur, label, identifier, dan aksi preprocessing.
- `results/tables/preprocessing_dataset_plan.csv`: rencana track imbalanced dan balanced controlled subset untuk Fase 4.
- `results/figures/eda_*.png`: visualisasi EDA awal.
- `reports/progress-3-eda-preprocessing.md`: laporan progres Fase 3.

Keputusan utama: `other_attack` tidak dianggap normal; baseline utama adalah `normal` vs `dos_or_ddos`, dengan jalur imbalanced dan balanced controlled subset.

## Baseline Modeling Snapshot

Fase 4 sudah menjalankan baseline modeling untuk target `normal` vs `dos_or_ddos`:

- `scripts/run_baseline_modeling.py`: runner baseline reproducible untuk Track A/B/C.
- `notebooks/02_baseline_modeling.ipynb`: notebook wrapper untuk menjalankan runner.
- `results/metrics/baseline_summary.json`: ringkasan baseline machine-readable.
- `results/tables/baseline_model_metrics.csv`: metrik model baseline.
- `results/tables/baseline_confusion_matrices.csv`: confusion matrix tiap run.
- `results/tables/baseline_dataset_tracks.csv`: ukuran dataset per track/split.
- `results/figures/baseline_*.png`: visualisasi perbandingan macro F1, MCC, dan confusion matrix.
- `reports/progress-4-baseline-modeling.md`: laporan progres Fase 4.

Keputusan utama: accuracy disimpan tetapi bukan klaim utama; interpretasi memakai macro F1, MCC, balanced accuracy, recall normal/attack, dan FP/FN.

## Next Phase — Forensic Analysis

Setelah Fase 4 di-*merge*, Fase 5 berfokus pada interpretasi forensik dari hasil baseline:

- feature importance dan/atau permutation importance,
- analisis false positive dan false negative,
- interpretasi pola trafik DoS/DDoS dari fitur dominan,
- pembahasan risiko normal class kecil dan split-similarity,
- rekomendasi mitigasi IDS IoT berbasis temuan eksperimen.

## Status

Current phase: **Fase 5 — Forensic Analysis**

## Review History

| Review | Model/Reviewer | Score | Verdict | File |
|---|---|---:|---|---|
| Initial Fase 0B | Codex lecturer | 83 | NEEDS REVISION | `docs/REVIEW_phase0b.md` |
| Final Fase 0B | Codex lecturer | 91 | APPROVED | `docs/REVIEW_phase0b_final.md` |
| Strict Re-review Fase 0 | Codex gpt-5.5 + high reasoning | 90 | APPROVED | `docs/REVIEW_phase0_gpt55_high.md` |
| Fase 1 Literature Review | Codex gpt-5.5 + high reasoning | 92 | APPROVED | `docs/REVIEW_phase1_literature_final_approved.md` |
| Fase 2 Dataset Audit | Codex gpt-5.5 + high reasoning | 89 | APPROVED | `docs/REVIEW_phase2_dataset_audit.md` |
| Fase 3 EDA & Preprocessing | Codex gpt-5.5 + high reasoning | 88 | APPROVED | `docs/REVIEW_phase3_eda_preprocessing.md` |
| Fase 3 Final Verification | Codex gpt-5.5 + high reasoning | 92 | APPROVED / MERGE | `docs/REVIEW_phase3_final_verification.md` |
| Fase 4 Baseline Modeling | Codex gpt-5.5 + high reasoning | 90 | APPROVED | `docs/REVIEW_phase4_baseline_modeling.md` |

Lihat:

- `docs/project-control.md`
- `docs/roadmap.md`
- `docs/phase-gates.md`
- `docs/REVIEW_phase0b.md`
- `docs/REVIEW_phase0b_final.md`
- `docs/REVIEW_phase0_gpt55_high.md`
- `docs/REVIEW_phase1_literature_final_approved.md`
- `docs/REVIEW_phase2_dataset_audit.md`
- `docs/REVIEW_phase3_eda_preprocessing.md`
- `docs/REVIEW_phase3_final_verification.md`
- `docs/REVIEW_phase4_baseline_modeling.md`
