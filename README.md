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

## Status

Current phase: **Fase 0B — Repository Setup**

Lihat:

- `docs/project-control.md`
- `docs/roadmap.md`
- `docs/phase-gates.md`
