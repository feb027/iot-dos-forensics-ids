# Fase 5 Method Notes — Forensic Analysis

Tanggal: 2026-04-29

## Tujuan

Fase 5 mengubah hasil baseline Fase 4 menjadi interpretasi forensik trafik IoT. Fokusnya bukan menambah klaim akurasi, tetapi menjelaskan fitur dan pola kesalahan yang mendukung analisis DoS/DDoS.

## Basis Artifact

Fase 5 memakai artifact Fase 4 sebagai basis:

- `results/tables/baseline_model_metrics.csv`
- `results/tables/baseline_confusion_matrices.csv`
- `results/metrics/baseline_summary.json`

Model interpretatif dilatih ulang secara reproducible dari script baseline, tanpa menyimpan model binary besar.

## Selected Runs

Selected runs dipilih karena mewakili baseline realistis dan controlled subset:

| Track | Model | Alasan |
|---|---|---|
| A_realistic_imbalanced | decision_tree | baseline terbaik pada distribusi realistis dan mudah diinterpretasi |
| B_balanced_controlled_1_to_1 | decision_tree | pembanding tree pada subset 1:1 |
| B_balanced_controlled_1_to_1 | random_forest | ensemble terbaik pada subset 1:1 |
| C_balanced_controlled_1_to_2 | decision_tree | pembanding tree pada subset 1:2 |
| C_balanced_controlled_1_to_2 | random_forest | ensemble terbaik pada subset 1:2 |

## Metode

1. Melatih ulang selected runs dengan fitur leakage-safe dari Fase 4.
2. Mengambil `feature_importances_` dari model tree/ensemble.
3. Menjalankan permutation importance berbasis penurunan macro F1 pada sampel test untuk melihat sensitivitas fitur mentah.
4. Menghasilkan ringkasan error dari prediksi test: TN, FP, FN, TP.
5. Menyimpan contoh FP/FN terbatas untuk bahan diskusi forensik tanpa mengembalikan kolom identifier IP/port.

## Top Feature Groups

| Rank | Feature Group | Mean Normalized Importance | Interpretasi |
|---:|---|---:|---|
| 1 | `N_IN_Conn_P_DstIP` | 0.7406 | jumlah koneksi masuk per destination IP; nilai tinggi relevan untuk konsentrasi serangan ke target IoT |
| 2 | `N_IN_Conn_P_SrcIP` | 0.0760 | jumlah koneksi masuk per source IP; nilai tinggi relevan untuk pola flood dari sumber tertentu |
| 3 | `stddev` | 0.0517 | deviasi statistik flow; membantu membedakan kestabilan trafik normal dan variasi trafik serangan |
| 4 | `srate` | 0.0411 | source packet rate; nilai tinggi dapat menunjukkan pengiriman paket agresif dari sumber serangan |
| 5 | `mean` | 0.0218 | rata-rata statistik flow; dapat merepresentasikan intensitas umum trafik |
| 6 | `max` | 0.0198 | nilai maksimum statistik flow; membantu menangkap spike intensitas trafik |
| 7 | `state_number` | 0.0184 | kode status koneksi; perubahan distribusi state membantu membaca pola koneksi gagal/abnormal |
| 8 | `drate` | 0.0065 | destination packet rate; perubahan tajam dapat menandai ketidakseimbangan aliran request-response |


## Error Totals pada Selected Runs

- False positive normal → attack: 2
- False negative attack → normal: 17
- Contoh FP/FN tersimpan: 16

## Batasan Interpretasi

1. Normal class sangat kecil: 370 train dan 107 test pada audited split.
2. Controlled Track B/C memakai semua normal dan sampel DoS/DDoS, sehingga hasil tinggi tidak boleh diklaim sebagai deteksi sempurna dunia nyata.
3. Kolom IP/port tetap dikeluarkan demi mencegah leakage/overfitting, sehingga interpretasi forensik berbasis fitur agregat trafik, bukan atribusi host spesifik.
4. Feature importance bersifat model-dependent; permutation importance dan error analysis dipakai sebagai pembanding.
