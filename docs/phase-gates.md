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

- [ ] Minimal 10–15 paper relevan.
- [ ] `references/literature-matrix.md` lengkap.
- [ ] `docs/research-log.md` terisi.
- [ ] Research gap sementara ditulis.
- [ ] Referensi punya link/DOI saat tersedia.
- [ ] Codex lecturer review score >= 85.

## Fase 2 — Dataset Audit

Done jika:

- [ ] Source BoT-IoT diverifikasi.
- [ ] Akses/download method jelas.
- [ ] Label mapping terdokumentasi.
- [ ] Kelas DoS/DDoS dikonfirmasi.
- [ ] Ukuran data, fitur, dan missing values dicatat.
- [ ] Risiko class imbalance dan leakage dicatat.

## Fase 3 — EDA & Preprocessing

Done jika:

- [ ] Notebook/script EDA ada.
- [ ] Class distribution figure tersimpan.
- [ ] Key feature plots tersimpan.
- [ ] Preprocessing pipeline terdokumentasi.
- [ ] Train/test split strategy jelas.

## Fase 4 — Baseline Modeling

Done jika:

- [ ] Minimal 3 model baseline dilatih.
- [ ] Metrics tersimpan ke CSV/JSON.
- [ ] Confusion matrix tersimpan.
- [ ] Model comparison figure tersimpan.
- [ ] Tidak ada leakage obvious.
- [ ] Technical review approved.

## Fase 5 — Forensic Analysis

Done jika:

- [ ] Feature importance CSV/figure tersedia.
- [ ] Interpretasi forensik tertulis.
- [ ] False positive/false negative dibahas jika artifact tersedia.
- [ ] Semua klaim terkait artifact.

## Fase 6 — Dashboard

Done jika:

- [ ] Static dashboard tersedia.
- [ ] Dashboard data generated via script.
- [ ] Local preview works.
- [ ] GitHub Pages works jika enabled.
- [ ] Dashboard claims cocok dengan result artifacts.

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
