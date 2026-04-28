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

Saat ini dashboard masih placeholder scaffold. Isi metrik akan diperbarui setelah eksperimen berjalan.

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

Fase berikutnya adalah audit dataset BoT-IoT sebelum EDA atau training model.

## Status

Current phase: **Fase 2 — Dataset Audit**

## Review History

| Review | Model/Reviewer | Score | Verdict | File |
|---|---|---:|---|---|
| Initial Fase 0B | Codex lecturer | 83 | NEEDS REVISION | `docs/REVIEW_phase0b.md` |
| Final Fase 0B | Codex lecturer | 91 | APPROVED | `docs/REVIEW_phase0b_final.md` |
| Strict Re-review Fase 0 | Codex gpt-5.5 + high reasoning | 90 | APPROVED | `docs/REVIEW_phase0_gpt55_high.md` |
| Fase 1 Literature Review | Codex gpt-5.5 + high reasoning | 92 | APPROVED | `docs/REVIEW_phase1_literature_final_approved.md` |

Lihat:

- `docs/project-control.md`
- `docs/roadmap.md`
- `docs/phase-gates.md`
- `docs/REVIEW_phase0b.md`
- `docs/REVIEW_phase0b_final.md`
- `docs/REVIEW_phase0_gpt55_high.md`
- `docs/REVIEW_phase1_literature_final_approved.md`
