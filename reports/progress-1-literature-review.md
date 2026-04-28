# Progress 1 — Literature Review

Tanggal: 2026-04-28

## Tujuan Fase

Fase 1 bertujuan membangun dasar teori dan rujukan awal untuk proyek **Sistem Analisis Serangan DoS pada Arsitektur IoT**. Fokusnya bukan eksperimen, melainkan memilih literatur yang cukup kuat untuk mendukung tahap dataset audit, baseline modeling, dan analisis forensik.

## Artefak yang Dibuat

| Artefak | Path | Status |
|---|---|---|
| Literature matrix | `references/literature-matrix.md` | berisi 18 sumber |
| BibTeX | `references/references.bib` | berisi 18 entry |
| Research log | `docs/research-log.md` | terisi ringkasan seleksi |
| Raw search evidence | `references/raw-search/` | tersimpan |
| Raw source evidence | `references/raw-sources/` | tersimpan |
| Raw metadata evidence | `references/raw-metadata/` | tersimpan |

## Komposisi Referensi

| Kelompok | Jumlah | Contoh Sumber |
|---|---:|---|
| Dataset utama/pembanding | 5 | BoT-IoT, RT-IoT2022, TON_IoT, CICIoT2023 |
| Eksperimen IDS/DoS/DDoS | 4 | BoT-IoT IDS, feature selection, lightweight DDoS, QAE RT-IoT2022 |
| Survey IoT IDS | 4 | Jamalipour & Murali, Jayalaxmi et al., Kikissagbe & Adda, Rahman et al. |
| Survey DoS/DDoS IoT | 2 | Pakmehr et al., Shukla et al. |
| Evaluasi/leakage | 1 | Bouke & Abdullah |
| Network forensics | 2 | Wu et al.; Koroniotis et al. |

## Sintesis Awal

BoT-IoT dipertahankan sebagai dataset utama karena paper intinya memang diarahkan untuk botnet IoT dan *network forensic analytics*. RT-IoT2022 tetap masuk sebagai alternatif karena lebih ringan, tersedia melalui UCI, dan memiliki label serangan yang eksplisit. Namun, kedua dataset tetap perlu diaudit pada Fase 2 sebelum ada klaim statistik atau hasil model.

Arah proyek yang paling realistis adalah **klasifikasi biner normal vs DoS/DDoS** lebih dulu, lalu dilanjutkan dengan analisis fitur penting untuk mendukung sudut pandang *network forensics*. Bagian forensik sekarang diperkuat oleh literatur khusus tentang analisis trafik IoT dan kerangka forensik jaringan IoT. Gap yang diambil bukan membuat algoritma baru, tetapi membuat pipeline yang dapat diaudit: sumber data jelas, label mapping jelas, evaluasi tidak bocor, metrik tersimpan, dan hasil diterjemahkan menjadi interpretasi forensik.

## Keputusan Sementara

1. Dataset utama tetap BoT-IoT.
2. Dataset alternatif tetap RT-IoT2022.
3. Scope eksperimen awal tetap binary classification normal vs DoS/DDoS.
4. Model baseline yang layak dipertimbangkan pada Fase 4: Logistic Regression, Decision Tree, Random Forest, KNN/Naive Bayes, dan XGBoost/LightGBM jika resource cukup.
5. Fase 2 wajib memprioritaskan pemeriksaan leakage sebelum EDA/modeling.

## Risiko yang Harus Dibawa ke Fase 2

- Ketimpangan kelas besar antara normal dan DoS/DDoS.
- Duplikasi flow/baris antar split.
- Fitur yang mengandung label atau terlalu dekat dengan label.
- Model menghafal IP/port/skenario simulator.
- Split random terlalu optimistis jika trafik sangat mirip antar waktu/skenario.
- Dataset besar membuat runtime lokal/Colab berat.

## Status

Fase 1 literature review sudah memenuhi target jumlah referensi awal dan revisi wajib dari review pertama sudah ditindaklanjuti: format BibTeX TON_IoT diperbaiki dan sumber network forensics ditambahkan. Final verification review menyatakan **APPROVED** dengan skor **92/100**. Fase berikutnya adalah Fase 2 Dataset Audit.
