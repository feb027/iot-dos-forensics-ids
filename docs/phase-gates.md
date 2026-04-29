# Phase Gates

Setiap fase hanya dianggap selesai jika artifact tersedia, dokumentasi diperbarui, dan review gate lolos.

## Review Verdict

- `APPROVED`: boleh lanjut.
- `NEEDS REVISION`: revisi dulu.
- `REJECTED`: fase belum layak, ulangi pendekatan.

Minimum passing score: **85**.

Target ideal: **90+**.

## Fase 0A — Agent & Workflow Scaffold

Done jika:

- [x] Skill/workflow proyek ditentukan.
- [x] Agent roles ditentukan.
- [x] Review gate ditentukan.
- [x] Prompt template ditentukan.
- [x] User menyetujui operating model.

## Fase 0B — Repository Setup

Done jika:

- [x] GitHub repo dibuat.
- [x] Struktur folder dibuat.
- [x] README awal dibuat.
- [x] `.gitignore` melindungi dataset/model besar.
- [x] `AGENTS.md` dibuat.
- [x] Docs awal dibuat.
- [x] Initial commit pushed.
- [x] GitHub Pages placeholder aktif.
- [x] Baseline smoke test tersedia dan dapat dijalankan.

## Fase 1 — Literature Review

Done jika:

- [x] Minimal 10–15 paper relevan.
- [x] `references/literature-matrix.md` lengkap.
- [x] `docs/research-log.md` terisi.
- [x] Research gap sementara ditulis.
- [x] Referensi punya link/DOI saat tersedia.
- [x] Codex lecturer review score >= 85.

## Fase 2 — Dataset Audit

Done jika:

- [x] Source BoT-IoT diverifikasi.
- [x] Akses/download method jelas.
- [x] Label mapping terdokumentasi.
- [x] Kelas DoS/DDoS dikonfirmasi.
- [x] Ukuran data, fitur, dan missing values dicatat.
- [x] Risiko class imbalance dan leakage dicatat.
- [x] Kolom label atau fitur label-like yang harus dikeluarkan dicatat.
- [x] Duplikasi flow/baris diperiksa.
- [x] Strategi split awal ditentukan sebelum modeling.
- [x] Codex review Fase 2 approved.

## Fase 3 — EDA & Preprocessing

Done jika:

- [x] Notebook/script EDA ada.
- [x] Class distribution figure tersimpan.
- [x] Key feature plots tersimpan.
- [x] Preprocessing pipeline terdokumentasi.
- [x] Train/test split strategy jelas.
- [x] Filtered binary dataset logic jelas: `normal` vs `dos_or_ddos`, `other_attack` tidak diam-diam dianggap normal.
- [x] Leakage columns tetap dikeluarkan: `attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, `dport`.
- [x] Balanced controlled subset plan dibuat untuk mitigasi normal class kecil.
- [x] EDA menyimpan artifact ke `results/tables/` dan `results/figures/`.
- [x] Codex review Fase 3 approved.

## Fase 4 — Baseline Modeling

Done jika:

- [x] Branch `phase-4-baseline-modeling` dibuat dari `main` setelah PR #3 merge.
- [x] Minimal 3 model baseline dilatih.
- [x] Track A realistic imbalanced baseline dijalankan.
- [x] Track B balanced controlled 1:1 dijalankan.
- [x] Track C 1:2 sensitivity check dijalankan atau alasan skip didokumentasikan.
- [x] Metrics tersimpan ke CSV/JSON.
- [x] Confusion matrix tersimpan.
- [x] Model comparison figure tersimpan.
- [x] Accuracy tidak menjadi klaim utama; precision, recall, F1, dan FP/FN dibahas.
- [x] Tidak ada leakage obvious.
- [x] Technical review approved.

## Fase 5 — Forensic Analysis

Done jika:

- [x] Feature importance CSV/figure tersedia.
- [x] Interpretasi forensik tertulis.
- [x] False positive/false negative dibahas jika artifact tersedia.
- [x] Semua klaim terkait artifact.
- [x] Codex review Fase 5 approved.

## Fase 6A — Advanced/SOTA Modeling Extension

Done jika:

- [x] Advanced model metrics tersimpan dan dibandingkan dengan baseline Fase 4.
- [x] Confusion matrix advanced models tersedia.
- [x] Explainability/SHAP sample tersedia tanpa membebani memori.
- [x] Klaim improvement memakai macro F1/MCC/recall/FP-FN, bukan accuracy saja.
- [x] Raw dataset, processed data besar, dan model binary tetap tidak ter-track.
- [x] Codex review Fase 6A approved.

## Fase 6 — Dashboard

Done jika:

- [x] Static dashboard tersedia.
- [x] Dashboard data generated via script.
- [ ] Local preview works after Fase 6A merge.
- [ ] GitHub Pages works after Fase 6A status sync.
- [ ] Dashboard claims cocok dengan result artifacts after polish review.

## Fase 7 — Scientific Manuscript

Done jika:

- [ ] Draft naskah lengkap.
- [ ] Semua gambar/tabel dirujuk benar.
- [ ] Sitasi valid dan berurutan.
- [ ] Tidak ada angka palsu.
- [ ] Lecturer review approved.

## Fase 8 — Final Audit & Release

Done jika:

- [ ] Repo clean.
- [ ] README lengkap.
- [ ] Dashboard link hidup.
- [ ] Final report siap submit.
- [ ] Final examiner approved.
