# Progress 4 — Baseline Modeling

Tanggal: 2026-04-29

## Ringkasan

Fase 4 melatih baseline model untuk deteksi `normal` vs `dos_or_ddos` pada BoT-IoT/UNSW-IoT. Fase ini mengikuti keputusan Fase 3:

- `other_attack` dikeluarkan dari binary baseline utama.
- Kolom leakage/identifier tidak digunakan sebagai fitur.
- Evaluasi tidak bertumpu pada accuracy saja.
- Track A/B/C digunakan untuk membandingkan realistic imbalance dan controlled balanced subset.

Script utama:

```bash
source .venv/bin/activate
python scripts/run_baseline_modeling.py
python scripts/generate_dashboard_data.py
```

Notebook wrapper:

```text
notebooks/02_baseline_modeling.ipynb
```

## Output Artifact

Tabel:

- `results/tables/baseline_model_metrics.csv`
- `results/tables/baseline_confusion_matrices.csv`
- `results/tables/baseline_dataset_tracks.csv`
- `results/tables/baseline_label_consistency_checks.csv`
- `results/tables/baseline_skipped_runs.csv`

Gambar:

- `results/figures/baseline_macro_f1_comparison.png`
- `results/figures/baseline_mcc_comparison.png`
- `results/figures/baseline_confusion_matrix_grid.png`

Summary JSON:

- `results/metrics/baseline_summary.json`

## Dataset Track yang Dijalankan

| Track | Split | Normal | DoS/DDoS | Total |
|---|---|---:|---:|---:|
| A_realistic_imbalanced | train | 370 | 2.861.463 | 2.861.833 |
| A_realistic_imbalanced | test | 107 | 715.421 | 715.528 |
| B_balanced_controlled_1_to_1 | train | 370 | 370 | 740 |
| B_balanced_controlled_1_to_1 | test | 107 | 107 | 214 |
| C_balanced_controlled_1_to_2 | train | 370 | 740 | 1.110 |
| C_balanced_controlled_1_to_2 | test | 107 | 214 | 321 |


## Top Baseline Results

| Rank | Track | Model | Macro F1 | MCC | Balanced Acc | Recall Normal | Recall Attack | FP | FN |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | B_balanced_controlled_1_to_1 | Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 | 0 |
| 2 | C_balanced_controlled_1_to_2 | Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 | 0 |
| 3 | B_balanced_controlled_1_to_1 | Decision Tree | 0.9953 | 0.9907 | 0.9953 | 1.0000 | 0.9907 | 0 | 1 |
| 4 | B_balanced_controlled_1_to_1 | SGD Logistic Regression | 0.9907 | 0.9815 | 0.9907 | 1.0000 | 0.9813 | 0 | 2 |
| 5 | C_balanced_controlled_1_to_2 | Decision Tree | 0.9896 | 0.9793 | 0.9930 | 1.0000 | 0.9860 | 0 | 3 |
| 6 | C_balanced_controlled_1_to_2 | SGD Logistic Regression | 0.9861 | 0.9726 | 0.9907 | 1.0000 | 0.9813 | 0 | 4 |
| 7 | A_realistic_imbalanced | Decision Tree | 0.9667 | 0.9344 | 0.9906 | 0.9813 | 1.0000 | 2 | 13 |
| 8 | C_balanced_controlled_1_to_2 | Gaussian Naive Bayes | 0.9378 | 0.8827 | 0.9206 | 0.8411 | 1.0000 | 17 | 0 |
| 9 | B_balanced_controlled_1_to_1 | Gaussian Naive Bayes | 0.8620 | 0.7573 | 0.8645 | 0.7290 | 1.0000 | 29 | 0 |
| 10 | A_realistic_imbalanced | Gaussian Naive Bayes | 0.5412 | 0.1064 | 0.6118 | 0.2243 | 0.9994 | 83 | 449 |


## Interpretasi Awal

- Dummy Majority memperlihatkan bahwa accuracy pada Track A bisa terlihat sangat tinggi tetapi gagal mendeteksi normal (`recall_normal=0`). Ini membuktikan accuracy tidak layak menjadi klaim utama.
- Decision Tree pada Track A menjadi baseline realistis yang kuat: macro F1 0.9667, MCC 0.9344.
- Random Forest pada Track B/C mencapai nilai sempurna pada subset controlled, tetapi ini harus dibaca hati-hati karena normal class sangat kecil dan Fase 2 sudah menemukan risiko split-similarity.
- Fase 5 perlu fokus pada feature importance, confusion matrix interpretation, dan diskusi FP/FN agar hasil menjadi analisis forensik, bukan sekadar klasifikasi.

## Keputusan

Fase 4 artifact cukup untuk technical review:

- Minimal 3 baseline model terpenuhi.
- Track A realistic imbalanced dijalankan.
- Track B 1:1 dan Track C 1:2 dijalankan.
- Metrics, confusion matrix, dan comparison figures tersimpan.
- Dashboard sudah membaca baseline metrics, tetapi feature importance tetap kosong sampai Fase 5.
