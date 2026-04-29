# Fase 6A — Advanced/SOTA Modeling Extension Plan

Tanggal: 2026-04-29

## Tujuan

Fase 6A memperkuat baseline Fase 4 dan interpretasi forensik Fase 5 dengan model tabular modern untuk trafik IoT:

- LightGBM
- XGBoost
- CatBoost
- sampled SHAP explainability

Fase ini tidak mengganti baseline, tetapi menjadi extension untuk menjawab apakah model modern dapat meningkatkan atau memvalidasi pola deteksi DoS/DDoS pada BoT-IoT.

## Pertanyaan Eksperimen

1. Apakah model gradient boosting modern meningkatkan macro F1/MCC dibanding baseline Fase 4 pada track yang sama?
2. Apakah recall normal dan FP/FN membaik tanpa hanya mengejar accuracy?
3. Apakah fitur dominan advanced model konsisten dengan temuan forensik Fase 5?
4. Apakah sampled SHAP memperkuat interpretasi bahwa pola koneksi/rate trafik relevan untuk DoS/DDoS IoT?

## Dataset dan Track

Menggunakan track yang sama dengan Fase 4:

| Track | Tujuan |
|---|---|
| A_realistic_imbalanced | distribusi realistis setelah `other_attack` dikeluarkan |
| B_balanced_controlled_1_to_1 | kontrol 1:1 memakai semua normal + sampel DoS/DDoS |
| C_balanced_controlled_1_to_2 | sensitivitas 1:2 memakai semua normal + dua kali sampel DoS/DDoS |

Default runner:

- LightGBM berjalan pada Track A/B/C.
- XGBoost dan CatBoost berjalan pada Track B/C secara default.
- XGBoost/CatBoost Track A hanya dijalankan jika `--include-heavy-track-a` dipakai.

Alasan: Track A berisi jutaan attack rows dan normal class sangat kecil; default dibuat aman untuk RAM WSL lokal.

## Model

| Model | Alasan |
|---|---|
| LightGBM | cepat untuk tabular data, cocok untuk fitur flow IDS |
| XGBoost | model boosting populer dan kuat untuk tabular benchmark |
| CatBoost | modern gradient boosting sebagai pembanding tambahan |

Semua model memakai fitur leakage-safe dari Fase 4:

- `proto`
- `stddev`
- `N_IN_Conn_P_SrcIP`
- `min`
- `state_number`
- `mean`
- `N_IN_Conn_P_DstIP`
- `drate`
- `srate`
- `max`

Kolom label dan identifier tetap dikeluarkan:

- `attack`, `category`, `subcategory`
- `pkSeqID`, `seq`
- `saddr`, `sport`, `daddr`, `dport`

## Output Artifact

Script:

- `scripts/run_advanced_modeling.py`

Notebook wrapper:

- `notebooks/04_advanced_modeling.ipynb`

Tabel:

- `results/tables/advanced_model_metrics.csv`
- `results/tables/advanced_confusion_matrices.csv`
- `results/tables/advanced_feature_importance.csv`
- `results/tables/advanced_shap_summary.csv`
- `results/tables/advanced_skipped_runs.csv`

Summary:

- `results/metrics/advanced_summary.json`

Figures:

- `results/figures/advanced_macro_f1_vs_baseline.png`
- `results/figures/advanced_mcc_vs_baseline.png`
- `results/figures/advanced_confusion_matrix_grid.png`
- `results/figures/advanced_shap_summary.png`

## Command Plan

Smoke test:

```bash
source .venv/bin/activate
python scripts/run_advanced_modeling.py --tracks B_balanced_controlled_1_to_1 --models lightgbm --max-train-rows 20000 --max-test-rows 10000 --shap-sample 100
```

Default full local WSL run:

```bash
source .venv/bin/activate
python scripts/run_advanced_modeling.py --models all --tracks all --shap-sample 3000
python scripts/generate_dashboard_data.py
```

Optional heavier run:

```bash
source .venv/bin/activate
python scripts/run_advanced_modeling.py --models all --tracks all --include-heavy-track-a --shap-sample 3000
```

## Claim Policy

- Accuracy tetap bukan klaim utama.
- Klaim improvement harus memakai perbandingan dengan baseline track yang sama.
- Normal class kecil dan split-similarity risk tetap disebut sebagai batasan.
- SHAP dibaca sebagai evidence pendukung interpretasi, bukan bukti kausal absolut.
