# Review Fase 4 Baseline Modeling

## Score
90

## Verdict
APPROVED

## Critical Issues
Tidak ada critical issue yang memblokir Fase 5.

## Important Issues
1. Dashboard dan README masih punya sebagian teks statis yang tertinggal dari fase sebelumnya. `dashboard/index.html` masih menyatakan hasil model dan confusion matrix akan ditambahkan setelah eksperimen tersedia, padahal `dashboard/data/dashboard-data.json` sudah berisi 14 baseline run dan 14 confusion matrix. README bagian Dashboard Preview juga masih menyebut dashboard hanya menampilkan Fase 2/Fase 3. Ini tidak merusak artifact, tetapi perlu dirapikan sebelum publikasi/PR agar narasi dashboard konsisten.
2. Random Forest sengaja tidak dijalankan pada Track A realistic imbalanced karena runtime, dan alasan skip sudah terdokumentasi. Ini dapat diterima untuk gate Fase 4 karena Track A tetap menjalankan Dummy Majority, Gaussian NB, SGD Logistic Regression, dan Decision Tree; namun laporan akhir harus menyatakan bahwa perbandingan Random Forest hanya berlaku untuk Track B/C.

## Minor Issues
1. Notebook `notebooks/02_baseline_modeling.ipynb` valid sebagai wrapper reproducible, tetapi belum menyimpan output eksekusi. Ini masih cukup untuk fase ini karena artifact CSV/JSON/PNG sudah tersedia dan valid.
2. Test baseline sudah mengunci fitur, excluded columns, scope mapping, deklarasi track/model, dan schema artifact. Untuk fase berikutnya, coverage bisa ditingkatkan dengan fixture kecil yang menjalankan `build_track_split` agar rasio Track B/C dan exclusion `other_attack` ikut diuji secara langsung.

## Evidence Checked
- Branch dan worktree: `git status -sb` menunjukkan branch `phase-4-baseline-modeling`; perubahan fase 4 belum dikomit.
- Validasi perintah:
  - `python3 -m py_compile scripts/*.py`: pass.
  - `python3 -m pytest -q`: pass, 9 tests.
  - `python3 -m json.tool results/metrics/baseline_summary.json`: pass.
  - `python3 -m json.tool dashboard/data/dashboard-data.json`: pass.
  - `python3 -m json.tool notebooks/02_baseline_modeling.ipynb`: pass.
  - `node --check dashboard/app.js`: pass.
  - `git ls-files data/raw data/processed results/models`: hanya `.gitkeep` yang terlacak; tidak ada raw dataset, processed dataset besar, atau model binary.
- `scripts/run_baseline_modeling.py`:
  - Fitur model dibatasi ke `proto`, `stddev`, `N_IN_Conn_P_SrcIP`, `min`, `state_number`, `mean`, `N_IN_Conn_P_DstIP`, `drate`, `srate`, dan `max`.
  - Kolom leakage/identifier `attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, dan `dport` dikeluarkan dari fitur.
  - `other_attack` tetap dipisah oleh `classify_scope()` dan `build_track_split()` hanya memilih `normal` serta `dos_or_ddos`.
  - Model baseline yang tersedia dan dijalankan mencakup Dummy Majority, Gaussian Naive Bayes, SGD Logistic Regression, Decision Tree, dan Random Forest.
- Artifact baseline:
  - `results/tables/baseline_model_metrics.csv`: 14 completed runs; Track A 4 run, Track B 5 run, Track C 5 run.
  - `results/tables/baseline_dataset_tracks.csv`: Track A realistic imbalanced, Track B 1:1, dan Track C 1:2 tersedia untuk train/test.
  - `results/tables/baseline_label_consistency_checks.csv`: 8 check, total violations 0.
  - `results/tables/baseline_confusion_matrices.csv`: 14 confusion matrix, sesuai jumlah completed runs.
  - `results/metrics/baseline_summary.json`: `total_completed_runs=14`, `other_attack_policy=excluded_from_primary_binary_baseline`, metric policy tidak memakai accuracy sebagai klaim utama.
  - `results/figures/baseline_macro_f1_comparison.png`, `baseline_mcc_comparison.png`, dan `baseline_confusion_matrix_grid.png` tersedia dan non-empty.
- Dashboard:
  - `scripts/generate_dashboard_data.py` membaca `baseline_model_metrics.csv`, `baseline_confusion_matrices.csv`, dan `baseline_summary.json`.
  - `dashboard/data/dashboard-data.json` memuat 14 `model_comparison`, 14 `confusion_matrix`, dan `feature_importance: []`; tidak ada feature importance palsu sebelum Fase 5.
  - `dashboard/app.js` menampilkan ringkasan baseline dari artifact dan menyatakan accuracy bukan klaim utama.
- Dokumentasi:
  - `docs/phase4-method-notes.md`, `docs/phase4-local-run-guide.md`, dan `reports/progress-4-baseline-modeling.md` mendokumentasikan track A/B/C, metrik utama, skip Random Forest pada Track A, serta interpretasi hati-hati untuk hasil sangat tinggi.
  - `docs/project-control.md` dan `docs/phase-gates.md` sudah menandai Fase 4 pending technical review dan membawa risiko normal class kecil serta split-similarity ke Fase 5.

## Required Fixes Before Next Phase
Tidak ada fix wajib yang memblokir Fase 5 Forensic Analysis.

Sebelum PR/merge Fase 4, rapikan teks statis `dashboard/index.html` dan README Dashboard Preview agar tidak menyatakan bahwa hasil model/confusion matrix belum tersedia. Untuk Fase 5, wajib lanjutkan interpretasi feature importance dan FP/FN secara hati-hati, terutama karena normal class hanya 370 train dan 107 test serta ada risiko split-similarity dari audit sebelumnya.
