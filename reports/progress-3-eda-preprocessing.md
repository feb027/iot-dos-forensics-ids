# Progress 3 — EDA & Preprocessing

Tanggal: 2026-04-29

## Ringkasan

Fase 3 melakukan EDA dan menyusun rencana preprocessing untuk BoT-IoT/UNSW-IoT sebelum masuk ke baseline modeling. Fase ini tidak melakukan training model dan tidak mengklaim performa deteksi.

Script utama:

```bash
python3 scripts/run_eda_preprocessing.py
```

Notebook wrapper:

```text
notebooks/01_eda_preprocessing.ipynb
```

## Output Artifact

Tabel:

- `results/tables/eda_category_distribution.csv`
- `results/tables/eda_subcategory_distribution.csv`
- `results/tables/eda_binary_scope_distribution.csv`
- `results/tables/eda_protocol_distribution.csv`
- `results/tables/eda_numeric_feature_summary.csv`
- `results/tables/eda_label_consistency_checks.csv`
- `results/tables/preprocessing_feature_plan.csv`
- `results/tables/preprocessing_dataset_plan.csv`

Gambar:

- `results/figures/eda_category_distribution_log.png`
- `results/figures/eda_binary_scope_distribution_log.png`
- `results/figures/eda_protocol_by_scope_log.png`
- `results/figures/eda_numeric_feature_means_log.png`

Summary JSON:

- `results/metrics/preprocessing_summary.json`

## Distribusi Scope Binary

| Split | Scope | Count | Rate |
|---|---|---:|---:|
| test | dos_or_ddos | 715.421 | 97.5080% |
| test | normal | 107 | 0.0146% |
| test | other_attack | 18.177 | 2.4774% |
| train | dos_or_ddos | 2.861.463 | 97.5006% |
| train | normal | 370 | 0.0126% |
| train | other_attack | 72.984 | 2.4868% |


Interpretasi utama:

- `normal` sangat kecil: 370 train dan 107 test.
- `dos_or_ddos` sangat dominan: 2.861.463 train dan 715.421 test.
- `other_attack` tetap dipisah dan tidak boleh dianggap normal pada binary baseline utama.

## Label Consistency

Label consistency checks menghasilkan 0 pelanggaran untuk semua check: `attack=0` konsisten dengan `Normal`, `DoS/DDoS` konsisten sebagai attack, dan `Reconnaissance/Theft` tetap `other_attack`. Detail ada di `results/tables/eda_label_consistency_checks.csv`.

## Feature Plan

| Column | Role | Action |
|---|---|---|
| `attack` | label | exclude_from_features |
| `category` | label | exclude_from_features |
| `subcategory` | label | exclude_from_features |
| `pkSeqID` | identifier | exclude_from_features |
| `seq` | identifier | exclude_from_features |
| `daddr` | network_identifier | exclude_from_features |
| `dport` | network_identifier | exclude_from_features |
| `saddr` | network_identifier | exclude_from_features |
| `sport` | network_identifier | exclude_from_features |
| `proto` | categorical_feature | one_hot_encode |
| `stddev` | numeric_feature | scale_or_passthrough |
| `N_IN_Conn_P_SrcIP` | numeric_feature | scale_or_passthrough |
| `min` | numeric_feature | scale_or_passthrough |
| `state_number` | numeric_feature | scale_or_passthrough |
| `mean` | numeric_feature | scale_or_passthrough |
| `N_IN_Conn_P_DstIP` | numeric_feature | scale_or_passthrough |
| `drate` | numeric_feature | scale_or_passthrough |
| `srate` | numeric_feature | scale_or_passthrough |
| `max` | numeric_feature | scale_or_passthrough |


## Dataset Plan untuk Fase 4

| Track | Split | Normal | DoS/DDoS available | DoS/DDoS used | Ratio | Policy |
|---|---|---:|---:|---:|---|---|
| A_realistic_imbalanced | test | 107 | 715.421 | 715.421 | 1:6686.18 | exclude_from_binary_baseline |
| B_balanced_controlled_1_to_1 | test | 107 | 715.421 | 107 | 1:1 | exclude_from_binary_baseline |
| C_balanced_controlled_1_to_2 | test | 107 | 715.421 | 214 | 1:2 | exclude_from_binary_baseline |
| A_realistic_imbalanced | train | 370 | 2.861.463 | 2.861.463 | 1:7733.68 | exclude_from_binary_baseline |
| B_balanced_controlled_1_to_1 | train | 370 | 2.861.463 | 370 | 1:1 | exclude_from_binary_baseline |
| C_balanced_controlled_1_to_2 | train | 370 | 2.861.463 | 740 | 1:2 | exclude_from_binary_baseline |


Rekomendasi Fase 4:

1. **Track A — realistic imbalanced baseline**  
   Menggunakan distribusi asli setelah `other_attack` dikeluarkan. Ini menunjukkan kondisi real dari split yang diaudit, tetapi evaluasi tidak boleh bertumpu pada accuracy.

2. **Track B — balanced controlled 1:1**  
   Menggunakan semua normal dan sampel DoS/DDoS dengan jumlah sama. Ini menjadi mitigasi utama untuk normal class yang sangat kecil.

3. **Track C — controlled 1:2**  
   Eksperimen sensitivitas opsional, masih relatif seimbang tetapi memberi porsi attack lebih besar.

## Catatan SOTA / Praktik Terbaru

Riset cepat dengan Exa menunjukkan bahwa isu utama pada IDS modern tetap sama: preprocessing, imbalance handling, data leakage prevention, dan metrik evaluasi yang tepat. Karena proyek ini konteksnya UAS dan digital forensics, pendekatan yang paling aman bukan langsung memakai teknik sintetis sebagai klaim utama, tetapi:

- memisahkan baseline imbalanced dan balanced controlled subset,
- tidak memasukkan kolom identifier/topology,
- tidak memakai accuracy saja,
- menunda SMOTE/oversampling sebagai eksperimen tambahan jika waktu cukup.

Detail ringkas ada di:

```text
docs/phase3-method-notes.md
```

## Keputusan

Fase 3 sudah menyiapkan EDA dan preprocessing plan yang cukup untuk Fase 4 setelah review:

- Target utama tetap `normal` vs `dos_or_ddos`.
- `other_attack` dikeluarkan dari binary baseline utama.
- Label/identifier/network identifier dikeluarkan dari fitur.
- Fase 4 harus menjalankan minimal dua track: imbalanced dan balanced controlled subset.
