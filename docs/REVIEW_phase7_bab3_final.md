# Final Verification Phase 7 Bab 3

Tanggal verifikasi final: Fri May 1 02:53:05 PM UTC 2026.

Draft yang diverifikasi: `reports/manuscript-draft-bab3.md`  
Review sebelumnya: `docs/REVIEW_phase7_bab3.md`

## Score Final

**94/100**

## Verdict

**APPROVED**

## Checklist Perbaikan

| No. | Item verifikasi | Status | Catatan |
|---:|---|---|---|
| 1 | Placeholder eksplisit Gambar 3.1 dan Gambar 3.2 sudah ada | PASS | Draft memuat `[PLACEHOLDER GAMBAR 3.1: ...]` dan `[PLACEHOLDER GAMBAR 3.2: ...]`, sehingga aman untuk pemindahan ke Word. |
| 2 | Rujukan Gambar 3.2 lebih natural | PASS | Kalimat sudah menjadi "Urutan kerja penelitian ditunjukkan secara konseptual pada Gambar 3.2." |
| 3 | Istilah asing dirapikan | PASS dengan catatan minor | Istilah utama seperti *working mirror*, *track*, *identifier bias*, *gradient boosting*, *pipeline*, dan *dashboard* sudah dominan rapi. Masih ada "model baseline" dan "dashboard statis" pada Tabel 3.2 yang bisa di-*italic* saat polish Word, tetapi tidak mengganggu kelayakan substansi. |
| 4 | Tabel 3.2 spesifik untuk kebutuhan perangkat lunak/dashboard statis | PASS | Tabel sudah menyebut Python, pandas, scikit-learn, LightGBM/XGBoost, HTML/CSS/JavaScript dashboard statis, JSON/CSV, dan Git/GitHub. Tidak ada klaim sensor, mikrokontroler, gateway fisik, atau hardware IoT. |
| 5 | Angka dataset, track, dan fitur tetap benar | PASS | Total 3.668.522 baris, split 2.934.817 train dan 733.705 test, Track A/B/C, 10 fitur kandidat, 1 fitur kategorikal, 9 fitur numerik, dan 9 kolom excluded tetap sesuai artefak. |
| 6 | Tidak ada hasil model Bab 4 masuk Bab 3 | PASS | Bab 3 hanya menjelaskan metode, model, metrik, dan batas evaluasi. Tidak ada nilai performa, ranking model final, atau klaim hasil eksperimen detail. |
| 7 | Tidak ada klaim berbahaya | PASS | Draft eksplisit membatasi penelitian sebagai prototipe berbasis dataset, bukan serangan perangkat asli, bukan IDS produksi *real-time*, bukan PCAP *replay* aktual, dan bukan generalisasi universal. |
| 8 | Panjang 1.500-1.900 kata | PASS | `wc -w` menunjukkan **1.854 kata**, masih dalam rentang target. |

## Sisa Catatan

Tidak ada critical issue atau major blocker. Sisa catatan hanya format kecil: saat masuk Word, italic pada istilah asing di dalam tabel dapat diseragamkan lagi, terutama "baseline" dan "dashboard" pada Tabel 3.2. Catatan ini tidak perlu membuka revisi substansi.

## Final Recommendation

**APPROVED.** Revisi minor dari review sebelumnya sudah cukup. Bab 3 layak digunakan sebagai bagian metode/perancangan sistem naskah UAS IoT dengan batasan akademik yang aman, angka yang konsisten dengan artefak, dan tanpa klaim hasil model yang mendahului Bab 4.
