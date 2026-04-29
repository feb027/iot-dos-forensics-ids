# Review Fase 5 Forensic Analysis

## Score
90

## Verdict
APPROVED

## Critical Issues
Tidak ada critical issue. Artifact Fase 5 sudah cukup untuk gate Forensic Analysis karena feature importance, permutation importance, FP/FN analysis, interpretasi forensik, dan limitation statement tersedia serta dapat ditelusuri ke script/artifact.

## Important Issues
1. Worktree belum siap untuk lanjut fase dari sisi kontrol proyek. `git status -sb` masih menunjukkan perubahan modified dan artifact Fase 5 yang untracked, termasuk `scripts/run_forensic_analysis.py`, `tests/test_run_forensic_analysis.py`, `notebooks/03_forensic_analysis.ipynb`, `results/metrics/forensic_summary.json`, `results/tables/forensic_*.csv`, dan `results/figures/forensic_*.png`. Ini bukan masalah isi analisis, tetapi harus dibereskan dengan commit fase setelah review/fix.
2. Test Fase 5 masih tipis. `tests/test_run_forensic_analysis.py` memeriksa konstanta, schema summary, dan schema CSV, tetapi belum menguji bahwa leakage columns tidak pernah masuk `CANDIDATE_FEATURES`, permutation importance wajib ada untuk semua selected runs, dan FP/FN forensic cocok dengan `baseline_confusion_matrices.csv`. Verifikasi manual pada review ini lulus, tetapi sebaiknya dijadikan test agar tidak regresi.

## Minor Issues
1. `README.md` masih punya bagian Dashboard Preview/Next Phase yang sebagian berbunyi seolah Fase 5 belum berjalan, walaupun bagian Forensic Analysis Snapshot sudah ditambahkan. Ini perlu dirapikan sebelum PR agar dokumentasi tidak terasa stale.
2. Dashboard sudah membaca artifact forensik nyata, tetapi hanya menampilkan baris `tree_feature_importance` teratas. Permutation importance tetap tersedia di CSV dan docs, namun belum ditampilkan di dashboard. Ini tidak blocking karena dashboard tidak mengklaim menampilkan permutation importance.
3. `docs/phase-gates.md` sudah menandai checklist artifact Fase 5 sebagai selesai dan menyisakan review approval. Setelah file review ini masuk, baris review perlu diperbarui pada commit berikutnya sesuai workflow.

## Evidence Checked
- Branch aktif: `phase-5-forensic-analysis`.
- Validasi CLI:
  - `python3 -m py_compile scripts/*.py` lulus.
  - `python3 -m pytest -q` lulus: 13 passed.
  - `python3 -m json.tool results/metrics/forensic_summary.json` lulus.
  - `python3 -m json.tool dashboard/data/dashboard-data.json` lulus.
  - `python3 -m json.tool notebooks/03_forensic_analysis.ipynb` lulus.
  - `node --check dashboard/app.js` lulus.
  - `git ls-files data/raw data/processed results/models` hanya menampilkan `.gitkeep`.
- Feature importance:
  - `results/tables/forensic_feature_importance.csv` berisi 116 data rows: 66 `tree_feature_importance` dan 50 `permutation_macro_f1_drop`.
  - Kedua metode tersedia untuk semua selected runs: Track A decision tree, Track B decision tree/random forest, dan Track C decision tree/random forest.
  - `results/metrics/forensic_summary.json` mengambil top feature groups dari artifact, bukan klaim manual. Top group `N_IN_Conn_P_DstIP` konsisten dengan CSV dan interpretasinya masuk akal untuk konsentrasi koneksi ke target IoT.
- Permutation importance:
  - Ada pada CSV dengan method `permutation_macro_f1_drop`, `importance_std`, dan `sample_rows`.
  - Docs menyebut permutation importance sebagai pembanding model-dependent feature importance.
- FP/FN analysis:
  - `results/tables/forensic_error_analysis.csv` tersedia dan cocok dengan `results/tables/baseline_confusion_matrices.csv` untuk semua selected runs.
  - Total selected runs pada summary cocok: FP normal-as-attack = 2, FN attack-as-normal = 17, examples saved = 16.
  - `results/tables/forensic_error_examples.csv` menyimpan contoh terbatas tanpa IP/port identifier.
- Leakage control:
  - `scripts/run_baseline_modeling.py` mendefinisikan `CANDIDATE_FEATURES` hanya `proto`, `stddev`, `N_IN_Conn_P_SrcIP`, `min`, `state_number`, `mean`, `N_IN_Conn_P_DstIP`, `drate`, `srate`, dan `max`.
  - Label columns dan identifier/network columns (`attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, `dport`) tidak masuk fitur model.
  - `scripts/run_forensic_analysis.py` melatih dan memprediksi dengan `train_frame[baseline.CANDIDATE_FEATURES]` dan `test_frame[baseline.CANDIDATE_FEATURES]`; label dipakai sesudah prediksi untuk error analysis.
- Interpretasi dan overclaim:
  - `docs/phase5-method-notes.md`, `reports/progress-5-forensic-analysis.md`, dan `forensic_summary.json` eksplisit menyebut normal class sangat kecil: 370 train dan 107 test.
  - Controlled Track B/C dan perfect/high metrics tidak dioverclaim; split-similarity risk disebut sebagai limitation.
- Dashboard:
  - `scripts/generate_dashboard_data.py` membaca `results/tables/forensic_feature_importance.csv`, `results/tables/forensic_error_analysis.csv`, dan `results/metrics/forensic_summary.json`.
  - `dashboard/data/dashboard-data.json` berisi `feature_importance`, `forensic_error_analysis`, dan `forensic_summary` dari artifact.
  - `dashboard/app.js` menampilkan feature/error totals dari JSON dan menyertakan note kehati-hatian terkait normal class kecil dan split-similarity.
- Figures dan tracked data risk:
  - `results/figures/forensic_feature_importance.png` dan `results/figures/forensic_confusion_error_summary.png` valid PNG.
  - Raw dataset lokal `data/raw/bot-iot-hf/` ter-ignore oleh `.gitignore`; tidak ada raw dataset besar, processed data besar, atau model binary yang ter-track.

## Required Fixes Before Next Phase
Tidak ada blocking technical fix untuk isi Fase 5. Sebelum lanjut ke advanced modeling/dashboard/manuscript, lakukan minimal:

1. Commit artifact dan dokumentasi Fase 5 pada branch `phase-5-forensic-analysis`.
2. Rapikan wording README yang masih menyebut Fase 5 sebagai pekerjaan mendatang.
3. Tambahkan test regresi ringan untuk presence permutation importance, FP/FN match terhadap baseline confusion, dan leakage exclusion agar gate ini tetap reproducible di CI.
