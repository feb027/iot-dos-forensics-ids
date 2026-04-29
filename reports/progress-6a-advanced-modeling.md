# Progress 6A — Advanced/SOTA Modeling Extension

Tanggal: 2026-04-29

## Ringkasan

Fase 6A menjalankan advanced tabular modeling untuk memperkuat baseline Fase 4 dan interpretasi forensik Fase 5. Model yang digunakan adalah LightGBM, XGBoost, dan CatBoost dengan sampled SHAP explainability.

Runner dijalankan di WSL lokal PC `Aqua` karena resource lebih kuat daripada VPS:

- CPU threads: 12
- RAM WSL setelah konfigurasi: sekitar 13 GiB
- Python: 3.12.3

Command utama:

```bash
source .venv/bin/activate
export LD_LIBRARY_PATH="$PWD/.venv/lib:${LD_LIBRARY_PATH:-}"
python scripts/run_advanced_modeling.py --models all --tracks all --shap-sample 3000
python scripts/generate_dashboard_data.py
```

## Output Artifact

Tabel:

- `results/tables/advanced_model_metrics.csv`
- `results/tables/advanced_confusion_matrices.csv`
- `results/tables/advanced_feature_importance.csv`
- `results/tables/advanced_shap_summary.csv`
- `results/tables/advanced_skipped_runs.csv`
- `results/tables/advanced_label_consistency_checks.csv`

Summary JSON:

- `results/metrics/advanced_summary.json`

Gambar:

- `results/figures/advanced_macro_f1_vs_baseline.png`
- `results/figures/advanced_mcc_vs_baseline.png`
- `results/figures/advanced_confusion_matrix_grid.png`
- `results/figures/advanced_shap_summary.png`

## Completed Runs

Total completed advanced runs: 7

Skipped runs:

- `xgboost` pada `A_realistic_imbalanced`: Skipped by default to keep Track A memory/runtime controlled; rerun with --include-heavy-track-a if needed.
- `catboost` pada `A_realistic_imbalanced`: Skipped by default to keep Track A memory/runtime controlled; rerun with --include-heavy-track-a if needed.

## Model Ranking

| Rank | Track | Model | Macro F1 | MCC | Recall Normal | Recall Attack | Δ Macro F1 vs Baseline |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | `C_balanced_controlled_1_to_2` | `xgboost` | 0.9965 | 0.9930 | 1.0000 | 0.9953 | -0.0035 |
| 2 | `C_balanced_controlled_1_to_2` | `lightgbm` | 0.9965 | 0.9930 | 0.9907 | 1.0000 | -0.0035 |
| 3 | `B_balanced_controlled_1_to_1` | `xgboost` | 0.9953 | 0.9907 | 1.0000 | 0.9907 | -0.0047 |
| 4 | `B_balanced_controlled_1_to_1` | `catboost` | 0.9953 | 0.9907 | 1.0000 | 0.9907 | -0.0047 |
| 5 | `B_balanced_controlled_1_to_1` | `lightgbm` | 0.9953 | 0.9907 | 0.9907 | 1.0000 | -0.0047 |
| 6 | `C_balanced_controlled_1_to_2` | `catboost` | 0.9930 | 0.9861 | 1.0000 | 0.9907 | -0.0070 |
| 7 | `A_realistic_imbalanced` | `lightgbm` | 0.9885 | 0.9770 | 0.9907 | 1.0000 | 0.0218 |


## Best Advanced Run

Best run berdasarkan macro F1, MCC, dan recall normal:

- Track: `C_balanced_controlled_1_to_2`
- Model: `xgboost`
- Macro F1: 0.9965
- MCC: 0.9930
- Recall normal: 1.0000
- Recall attack: 0.9953
- FP normal → attack: 0
- FN attack → normal: 1
- Δ Macro F1 vs baseline track sama: -0.0035

## Track A Realistic Imbalanced Highlight

LightGBM pada Track A realistis menghasilkan macro F1 0.9885, MCC 0.9770, recall normal 0.9907, dan Δ Macro F1 vs baseline 0.0218. Ini menarik karena Track A adalah skenario paling realistis dan advanced model meningkatkan macro F1 dibanding baseline terbaik pada track yang sama.

## SHAP / Explainability Summary

Top SHAP feature groups:

| Rank | Feature Group | Normalized SHAP Share | Interpretasi |
|---:|---|---:|---|
| 1 | `N_IN_Conn_P_DstIP` | 0.4762 | jumlah koneksi masuk per destination IP; relevan untuk konsentrasi serangan ke target/gateway IoT |
| 2 | `stddev` | 0.1049 | deviasi statistik flow; membedakan stabilitas trafik normal dan variasi trafik serangan |
| 3 | `N_IN_Conn_P_SrcIP` | 0.1020 | jumlah koneksi masuk per source IP; membantu membaca pola flood dari sumber tertentu |
| 4 | `mean` | 0.0740 | rata-rata statistik flow; merepresentasikan intensitas umum trafik |
| 5 | `max` | 0.0689 | nilai maksimum statistik flow; menangkap spike intensitas trafik |
| 6 | `state_number` | 0.0597 | kode status koneksi; membantu membaca pola koneksi gagal/abnormal |


## Interpretasi Awal

- `N_IN_Conn_P_DstIP` tetap menjadi feature group paling dominan pada sampled SHAP. Ini konsisten dengan Fase 5 dan mendukung narasi bahwa DoS/DDoS IoT terlihat dari konsentrasi koneksi ke target/gateway IoT.
- Pada Track A realistis, LightGBM memberi peningkatan macro F1 dibanding baseline track yang sama. Ini menjadi bagian paling menarik untuk naskah karena Track A lebih dekat ke distribusi asli yang imbalance.
- Pada Track B/C controlled subset, baseline random forest sudah sangat tinggi sehingga advanced model tidak selalu melampaui baseline. Ini tidak boleh dibaca sebagai kegagalan, tetapi sebagai bukti bahwa controlled subset mudah dan rawan overclaim.
- XGBoost menjadi best overall secara ranking, tetapi delta terhadap baseline controlled Track C negatif kecil karena baseline track itu sudah sempurna/nyaris sempurna.

## Limitation Statement

- Normal class tetap sangat kecil; hasil tinggi tidak boleh diklaim sebagai deteksi sempurna dunia nyata.
- SHAP dihitung pada sample maksimal 3000 rows per run, bukan seluruh dataset.
- XGBoost dan CatBoost Track A di-skip default untuk menjaga resource lokal; LightGBM dipakai sebagai advanced representative untuk Track A.
- Kolom IP/port dan label tetap dikeluarkan sehingga interpretasi berbasis pola trafik agregat, bukan atribusi host spesifik.

## Keputusan

Fase 6A artifact siap untuk Codex technical/lecturer review. Klaim utama yang aman:

1. Advanced model memperkuat interpretasi fitur forensik yang sudah ditemukan pada Fase 5.
2. LightGBM meningkatkan performa pada Track A realistis dibanding baseline track yang sama.
3. Controlled subset tetap harus dibahas hati-hati karena baseline sudah sangat tinggi.
