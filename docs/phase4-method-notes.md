# Fase 4 Method Notes — Baseline Modeling

Tanggal: 2026-04-29

## Tujuan

Fase 4 menjalankan baseline modeling untuk target utama `normal` vs `dos_or_ddos` menggunakan keputusan leakage-safe dari Fase 3. `other_attack` tetap dikeluarkan dari binary baseline utama.

## Sumber Riset Cepat

Pencarian dilakukan dengan Exa/mcporter dan disimpan sebagai evidence:

- `references/raw-search/phase4_ids_imbalance_metrics_exa.json`
- `references/raw-search/phase4_botiot_ml_baselines_exa.json`
- `references/raw-sources/phase4_baseline_methods_exa_crawl.json`

Ringkasan keputusan dari riset cepat:

1. Literatur NIDS/IDS imbalanced menekankan bahwa accuracy dapat menyesatkan saat class imbalance ekstrem.
2. Metrik seperti macro F1, balanced accuracy, MCC, confusion matrix, serta false positive/false negative lebih tepat untuk interpretasi.
3. Studi BoT-IoT terbaru masih memakai baseline tradisional seperti Logistic Regression, Decision Tree, Random Forest, dan model probabilistik/ensemble sebagai pembanding.
4. Oversampling/SMOTE relevan tetapi tidak dijadikan klaim utama pada fase ini karena proyek berorientasi digital forensics dan harus menjaga interpretasi terhadap data nyata.

## Dataset Track

| Track | Split | Normal | DoS/DDoS | Total | Catatan |
|---|---|---:|---:|---:|---|
| A_realistic_imbalanced | train | 370 | 2.861.463 | 2.861.833 | Realistic imbalanced split after excluding other_attack. |
| A_realistic_imbalanced | test | 107 | 715.421 | 715.528 | Realistic imbalanced split after excluding other_attack. |
| B_balanced_controlled_1_to_1 | train | 370 | 370 | 740 | Balanced controlled subset using all normal rows and equal sampled DoS/DDoS rows. |
| B_balanced_controlled_1_to_1 | test | 107 | 107 | 214 | Balanced controlled subset using all normal rows and equal sampled DoS/DDoS rows. |
| C_balanced_controlled_1_to_2 | train | 370 | 740 | 1.110 | Moderately imbalanced controlled subset using all normal rows and twice as many sampled DoS/DDoS rows. |
| C_balanced_controlled_1_to_2 | test | 107 | 214 | 321 | Moderately imbalanced controlled subset using all normal rows and twice as many sampled DoS/DDoS rows. |


## Model Baseline

Model yang dijalankan:

- Dummy Majority — sanity baseline untuk menunjukkan bahaya majority-class prediction.
- Gaussian Naive Bayes — baseline probabilistik sederhana.
- SGD Logistic Regression — baseline linear dengan `class_weight=balanced`.
- Decision Tree — baseline tree dengan `class_weight=balanced`.
- Random Forest — baseline ensemble pada controlled tracks B dan C. Track A full imbalanced tidak menjalankan Random Forest secara default untuk menghindari runtime berlebihan pada jutaan baris attack.

## Metrik Utama

Accuracy disimpan tetapi bukan klaim utama. Prioritas interpretasi:

- macro F1,
- MCC,
- balanced accuracy,
- recall normal,
- recall attack,
- confusion matrix,
- false positive dan false negative.

## Hasil Ringkas

Best overall berdasarkan macro F1, MCC, dan recall normal:

- Track: `B_balanced_controlled_1_to_1`
- Model: `Random Forest`
- Macro F1: 1.0000
- MCC: 1.0000
- Balanced Accuracy: 1.0000

## Batasan Interpretasi

Hasil yang sangat tinggi pada controlled subset tidak boleh langsung diklaim sebagai generalisasi dunia nyata karena:

1. Normal class hanya 370 train dan 107 test.
2. Dataset memiliki risiko split-similarity dari audit Fase 2.
3. Beberapa fitur agregat trafik sangat memisahkan kelas pada subset ini.
4. Evaluasi Fase 5 perlu membahas feature importance dan error analysis agar klaim forensik lebih defensible.
