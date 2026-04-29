# Review Fase 6A Advanced/SOTA Modeling

## Score
90

## Verdict
APPROVED

## Critical Issues
Tidak ada critical issue.

Gate Advanced/SOTA Modeling layak dilewati. Artifact Fase 6A sudah cukup kuat untuk lanjut ke dashboard/manuscript polish dengan catatan bahwa narasi tetap harus hati-hati terhadap normal class yang sangat kecil dan controlled subset yang baseline-nya sudah sempurna.

## Important Issues
Tidak ada issue penting yang memblokir fase berikutnya.

## Minor Issues
1. Ringkasan SHAP agregat menjumlahkan kontribusi normalized per run, sehingga `N_IN_Conn_P_DstIP` menjadi top global. Untuk manuscript, bedakan dengan jelas antara agregat semua run dan SHAP Track A saja, karena Track A LightGBM sendiri menempatkan `mean`, `proto`, dan `state_number` lebih tinggi daripada `N_IN_Conn_P_DstIP`.
2. Dashboard sudah membaca artifact nyata, tetapi panel advanced masih menonjolkan best overall berdasarkan macro F1 (`xgboost` Track C). Saat polish dashboard, sebaiknya tambahkan highlight Track A realistis agar kontribusi paling relevan tidak tenggelam oleh controlled subset.
3. README bagian Dashboard Preview masih menyebut Fase 2-5, sementara bagian Advanced/SOTA sudah memuat Fase 6A. Ini minor documentation stale wording.
4. Unit test Fase 6A sudah memeriksa schema, model spec, skip policy, dan leakage-safe feature list, tetapi belum menjalankan smoke experiment end-to-end dengan fixture kecil. Artifact full run sudah tersedia, jadi ini bukan blocker.

## Evidence Checked
- Branch: `phase-6a-advanced-modeling`.
- `scripts/run_advanced_modeling.py`: menggunakan LightGBM, XGBoost, CatBoost; membandingkan tiap run dengan best baseline Fase 4 pada track yang sama; menulis metrics, confusion matrix, native importance, sampled SHAP, skipped runs, label checks, JSON summary, dan figures.
- `tests/test_run_advanced_modeling.py`: memeriksa advanced model specs, Track A skip policy, feature group collapse, leakage-safe baseline features, summary schema, metrics schema, dan SHAP schema.
- `notebooks/04_advanced_modeling.ipynb`: valid JSON dan menjadi wrapper reproducible untuk runner advanced serta dashboard data generation.
- `docs/phase6a-advanced-modeling-plan.md`, `docs/phase6a-local-run-guide.md`, `reports/progress-6a-advanced-modeling.md`, `README.md`, `docs/project-control.md`, dan `docs/phase-gates.md`: sudah mendokumentasikan tujuan, track, model, command, WSL workaround, output artifact, dan batasan klaim.
- `results/metrics/advanced_summary.json`: valid; memuat 7 completed runs, 2 skipped heavy Track A runs, excluded columns, metric policy, best_by_track, top native feature groups, top SHAP feature groups, dan limitations.
- `results/tables/advanced_model_metrics.csv`: 7 run tersedia pada Track A/B/C. Model yang muncul: `lightgbm`, `xgboost`, `catboost`. Delta baseline konsisten dengan `baseline_model_metrics.csv`.
- Track A realistis: LightGBM macro F1 0.98847752, MCC 0.97704843, recall normal 0.99065421, FP 1, FN 4, delta macro F1 +0.0218161, delta MCC +0.04260782 terhadap baseline Track A `decision_tree`.
- Controlled Track B/C: baseline `random_forest` sudah 1.0 macro F1/MCC; advanced model tidak meng-overclaim dan delta negatif kecil tercatat jelas.
- `results/tables/advanced_confusion_matrices.csv`: 7 confusion matrix sesuai metrics.
- `results/tables/advanced_feature_importance.csv`: 92 rows native importance dengan interpretation hints forensik.
- `results/tables/advanced_shap_summary.csv`: 92 rows sampled SHAP; sample Track A 3000 rows, controlled tracks memakai seluruh test subset.
- `results/tables/advanced_skipped_runs.csv`: XGBoost dan CatBoost Track A di-skip by default karena kontrol RAM/runtime WSL, terdokumentasi.
- `results/tables/advanced_label_consistency_checks.csv`: semua 8 checks bernilai 0 violation.
- `results/figures/advanced_confusion_matrix_grid.png`, `advanced_macro_f1_vs_baseline.png`, `advanced_mcc_vs_baseline.png`, dan `advanced_shap_summary.png`: tersedia dan berukuran wajar.
- `scripts/generate_dashboard_data.py`: membaca CSV/JSON artifact advanced, bukan hardcoded metric manual.
- `dashboard/data/dashboard-data.json`: valid JSON dan memuat 7 advanced model rows, advanced confusion, advanced SHAP, serta advanced_summary.
- `dashboard/app.js`: valid JavaScript dan membaca `dashboard-data.json`.
- Leakage: fitur model memakai `proto`, `stddev`, `N_IN_Conn_P_SrcIP`, `min`, `state_number`, `mean`, `N_IN_Conn_P_DstIP`, `drate`, `srate`, `max`; kolom `attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, `dport` tetap excluded. Catatan residual: fitur agregat per SrcIP/DstIP bukan raw identifier, tetapi tetap perlu dibahas sebagai fitur statistik yang dataset-specific.
- Large file tracking: `git ls-files data/raw data/processed results/models` hanya menampilkan `.gitkeep`; raw CSV besar ada lokal di `data/raw/bot-iot-hf/` tetapi tidak tracked.

Validasi yang dijalankan:

```text
python3 -m py_compile scripts/*.py                         PASS
python3 -m pytest -q                                      PASS, 22 passed
python3 -m json.tool results/metrics/advanced_summary.json PASS
python3 -m json.tool dashboard/data/dashboard-data.json    PASS
python3 -m json.tool notebooks/04_advanced_modeling.ipynb  PASS
node --check dashboard/app.js                              PASS
git ls-files data/raw data/processed results/models        PASS, only .gitkeep tracked
```

`git status -sb` menunjukkan working tree memang berisi artifact Fase 6A yang belum di-commit, termasuk README/docs/dashboard data/results advanced. Tidak ada raw dataset besar, processed data besar, atau model binary yang masuk tracking.

## Required Fixes Before Next Phase
Tidak ada required fix yang memblokir lanjut ke fase dashboard/manuscript polish.

Saat masuk fase polish, lakukan perbaikan minor berikut tanpa mengubah hasil eksperimen:

1. Tambahkan highlight Track A realistis pada dashboard agar pembaca tidak menyimpulkan controlled subset sebagai klaim utama.
2. Perjelas di manuscript bahwa SHAP summary global adalah agregat seluruh run, sedangkan interpretasi Track A perlu dibaca dari row Track A LightGBM.
3. Update wording README Dashboard Preview agar menyebut Fase 6A.
