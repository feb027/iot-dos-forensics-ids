# Fase 3 Method Notes — EDA & Preprocessing

Tanggal riset cepat: 2026-04-29

## Tujuan

Fase 3 tidak langsung melakukan modeling. Tujuannya adalah membuat EDA dan rencana preprocessing yang aman dari leakage sebelum Fase 4 baseline modeling.

## Sumber Riset Cepat

Pencarian dilakukan dengan Exa via mcporter dan disimpan sebagai evidence:

- `references/raw-search/phase3_iot_ids_preprocessing_2026_exa.json`
- `references/raw-search/phase3_botiot_leakage_exa.json`
- `references/raw-search/phase3_ids_leakage_method_exa.json`
- `references/raw-sources/phase3_eda_preprocessing_methods_exa_crawl.json`

Sumber yang paling relevan untuk keputusan Fase 3:

1. *Dealing with Imbalanced Classes in Bot-IoT Dataset* — membahas masalah class imbalance pada BoT-IoT dan penggunaan SMOTE sebagai salah satu pendekatan mitigasi.
2. *Investigating Oversampling Techniques to Mitigate Class Imbalance in Network Intrusion Detection Datasets* — menekankan bahwa imbalance dapat menurunkan deteksi minority class dan membandingkan teknik oversampling seperti KMeans-SMOTE, SMOTE-NC, dan CVAE.
3. *Optimized Intrusion Detection in the IoT Through Statistical Selection and Classification with CatBoost and SNN* — menyoroti preprocessing, feature selection, rebalancing, dan evaluasi memakai precision, recall, F1, MCC, dan confidence interval.
4. *An empirical assessment of ML models for 5G network intrusion detection: A data leakage-free approach* — menekankan desain preprocessing dan eksperimen yang menghindari data leakage.

## Keputusan Metodologi untuk Proyek Ini

Karena proyek ini UAS individu, targetnya bukan mengejar model deep learning paling kompleks, tetapi membuat pipeline yang defensible dan reproducible.

Keputusan Fase 3:

1. **Tidak langsung memakai SMOTE sebagai klaim utama.**
   - SMOTE relevan untuk imbalance, tetapi untuk digital forensics, data sintetis harus hati-hati.
   - Jika dipakai nanti, posisinya hanya eksperimen tambahan, bukan baseline utama.

2. **Buat dua jalur Fase 4 sejak preprocessing.**
   - Jalur A: realistic imbalanced baseline mengikuti distribusi asli.
   - Jalur B: balanced controlled subset memakai semua normal dan sampel DoS/DDoS dengan seed tetap.
   - Jalur C opsional: ratio 1:2 sebagai kompromi.

3. **`other_attack` tidak boleh dianggap normal.**
   - Target utama adalah `normal` vs `dos_or_ddos`.
   - `Reconnaissance` dan `Theft` masuk `other_attack`; untuk binary baseline utama, baris ini dikeluarkan.

4. **Kolom leakage/identifier tetap dikeluarkan.**
   - Excluded: `attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, `dport`.
   - Fitur kandidat: `proto`, `stddev`, `N_IN_Conn_P_SrcIP`, `min`, `state_number`, `mean`, `N_IN_Conn_P_DstIP`, `drate`, `srate`, `max`.

5. **Evaluasi Fase 4 tidak boleh berbasis accuracy saja.**
   - Minimal: precision, recall, F1, confusion matrix.
   - Tambahan bagus: false positive/false negative discussion, MCC jika memungkinkan.

## Implikasi untuk Fase 4

Fase 4 baseline modeling nanti sebaiknya membandingkan minimal:

- Logistic Regression atau linear baseline sederhana.
- Decision Tree / Random Forest.
- Gradient boosting seperti HistGradientBoosting atau CatBoost/XGBoost jika dependensi tersedia.

Namun Fase 3 hanya menyiapkan EDA dan preprocessing plan. Tidak ada hasil modeling diklaim pada fase ini.
