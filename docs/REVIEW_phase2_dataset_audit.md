# Review Fase 2 Dataset Audit

## Score
89

## Verdict
APPROVED

## Critical Issues
Tidak ada isu kritis yang menghalangi gate Fase 2. Audit dataset sudah cukup sebagai dasar masuk ke Fase 3 EDA/preprocessing, dengan syarat batasan imbalance dan risiko split similarity tetap dibawa ke fase berikutnya.

## Important Issues
1. `docs/phase-gates.md` masih belum menyinkronkan status checklist Fase 2 untuk source verification, akses/download, label mapping, konfirmasi kelas DoS/DDoS, ukuran data, fitur, dan missing values. Bukti sebenarnya sudah ada di `docs/dataset-notes.md`, `docs/dataset-access-evidence.md`, dan artifact `results/`, tetapi gate document masih tampak belum selesai.
2. Provenance mirror Hugging Face sudah jujur dan didukung `references/raw-metadata/hf-unsw-iot-api-phase2.json`, termasuk repository SHA `b33d67c3a80bc483dcf54fb2d492d9923f0dce40`. Namun `docs/dataset-access-evidence.md` belum menuliskan perintah download atau revision/commit mirror secara eksplisit. Untuk reproducibility akademik, detail ini sebaiknya dicantumkan sebelum Fase 3 dikunci.
3. Artifact `results/tables/dataset_files.csv` menunjukkan duplicate model-feature signature dalam split cukup besar, yaitu 1.487.901 pada train dan 202.630 pada test setelah identifier, network identifier, dan label dikeluarkan. Dokumen sudah membahas overlap model-feature antar split sebesar 327.338, tetapi duplicate signature dalam split juga perlu disebut sebagai risiko evaluasi/sampling agar modeling tidak salah menafsirkan banyak baris mirip sebagai variasi independen.

## Minor Issues
1. `README.md` masih menyebut dashboard sebagai placeholder scaffold, sementara `dashboard/data/dashboard-data.json` sudah berisi ringkasan audit Fase 2. Ini bukan fabrikasi hasil modeling, tetapi wording dapat dibuat lebih akurat setelah review.
2. Inferensi tipe di `column_profile.csv` menandai `dport` sebagai dominant integer walaupun sample values memuat nilai heksadesimal seperti `0x0102`. Dampaknya kecil karena `dport` sudah benar dikeluarkan sebagai network identifier, tetapi catatan ini perlu diingat bila ada validasi tipe lebih ketat di Fase 3.

## Evidence Checked
- Branch aktif: `phase-2-dataset-audit`.
- File diperiksa: `scripts/audit_botiot_dataset.py`, `tests/test_audit_botiot_dataset.py`, `docs/dataset-notes.md`, `docs/dataset-access-evidence.md`, `reports/progress-2-dataset-audit.md`, `results/metrics/dataset_audit.json`, `results/tables/dataset_files.csv`, `results/tables/class_distribution.csv`, `results/tables/column_profile.csv`, `results/tables/split_leakage_checks.csv`, `dashboard/data/dashboard-data.json`, `docs/project-control.md`, dan `docs/phase-gates.md`.
- Validasi dijalankan:
  - `python3 -m py_compile scripts/*.py` berhasil.
  - `python3 -m pytest -q` berhasil: 4 tests passed.
  - `python3 -m json.tool results/metrics/dataset_audit.json` berhasil.
  - `python3 -m json.tool dashboard/data/dashboard-data.json` berhasil.
- Sumber/access dataset terdokumentasi jujur: sumber ilmiah utama UNSW BoT-IoT dicantumkan, mirror kerja Hugging Face `Mireu-Lab/UNSW-IoT` dinyatakan sebagai akses praktis, raw CSV berada di `data/raw/bot-iot-hf/` dan tidak di-commit.
- Label mapping jelas: `attack=0` sebagai normal, `attack=1` sebagai attack, `category in {DoS, DDoS}` sebagai `dos_or_ddos`, `Normal` sebagai `normal`, dan kategori lain sebagai `other_attack`.
- Kolom yang dikeluarkan karena leakage/identifier sudah tepat untuk baseline: `attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, dan `dport`.
- Class distribution, missing values, duplicate checks, checksum file, dan split overlap didukung artifact CSV/JSON. Tidak ada missing values pada profil kolom, tidak ada exact duplicate row, tidak ada duplicate `pkSeqID`, dan tidak ada overlap full-row train/test.
- Dashboard data tidak mengarang hasil modeling: `model_comparison` kosong, `confusion_matrix` kosong, `feature_importance` kosong, dan status menyatakan modeling belum dimulai.

## Required Fixes Before Next Phase
1. Sinkronkan `docs/phase-gates.md` dan `docs/project-control.md` setelah review ini: tandai item Fase 2 yang sudah terbukti selesai dan ubah status review Fase 2 dari pending menjadi approved.
2. Tambahkan detail exact access method untuk mirror, minimal perintah download atau referensi Hugging Face revision SHA `b33d67c3a80bc483dcf54fb2d492d9923f0dce40`, ke dokumentasi akses dataset.
3. Tambahkan interpretasi singkat tentang duplicate model-feature signature dalam split ke `docs/dataset-notes.md` atau `reports/progress-2-dataset-audit.md` agar risiko sampling/evaluasi terbawa ke Fase 3.
