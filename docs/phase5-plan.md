# Fase 5 Plan — Forensic Analysis

## Tujuan

Mengubah hasil baseline modeling Fase 4 menjadi analisis forensik trafik IoT yang dapat dipertanggungjawabkan secara akademik.

## Pertanyaan Analisis

1. Fitur trafik apa yang paling membedakan `normal` dan `dos_or_ddos`?
2. Model mana yang paling stabil jika dilihat dari macro F1, MCC, recall normal, dan false positive/false negative?
3. Pola trafik apa yang dapat dijelaskan sebagai indikasi DoS/DDoS pada arsitektur IoT?
4. Bagaimana risiko normal class kecil dan split-similarity memengaruhi klaim hasil?

## Artifact Target

- `scripts/run_forensic_analysis.py`
- `notebooks/03_forensic_analysis.ipynb`
- `results/tables/forensic_feature_importance.csv`
- `results/tables/forensic_error_analysis.csv`
- `results/figures/forensic_feature_importance.png`
- `results/figures/forensic_confusion_error_summary.png`
- `results/metrics/forensic_summary.json`
- `docs/phase5-method-notes.md`
- `reports/progress-5-forensic-analysis.md`

## Metode Awal

1. Gunakan artifact Fase 4 sebagai basis, bukan klaim manual.
2. Hitung feature importance untuk model tree/ensemble jika model dapat dilatih ulang secara reproducible.
3. Gunakan permutation importance untuk membandingkan pengaruh fitur pada evaluasi.
4. Buat ringkasan FP/FN dari confusion matrix Fase 4.
5. Jelaskan hasil tinggi secara hati-hati: normal class hanya 370 train dan 107 test.

## Gate

Fase 5 selesai jika feature importance, FP/FN discussion, forensic interpretation, dan limitation statement sudah ada serta lulus Codex review.
