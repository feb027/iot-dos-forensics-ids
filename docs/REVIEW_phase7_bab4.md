# Review Phase 7 BAB 4 — Lecturer Reviewer

Tanggal review: Fri May 1 03:31:15 PM UTC 2026

Draft direview: `reports/manuscript-draft-bab4.md`

## Score

**91/100**

## Verdict

**APPROVED**

## Ringkasan Keputusan

BAB 4 layak masuk tahap finalisasi Word dengan revisi minor. Struktur 4.1 sampai 4.7 lengkap, panjang 1.904 kata masuk batas 1.900-2.400 kata, dan angka utama dataset, *baseline*, *advanced model*, delta metrik, *confusion matrix*, *feature importance*, SHAP, serta klaim *dashboard* konsisten dengan artifact. Draft juga tidak menjual akurasi sebagai klaim utama dan cukup disiplin membatasi Track B/C sebagai subset kecil terkontrol.

Kelemahannya bukan pada validitas angka, tetapi pada kesiapan naskah akademik final: beberapa tabel masih terlalu ringkas, Tabel 4.3 punya satu baris yang kabur, caption gambar masih berupa placeholder, dan sebagian istilah asing belum konsisten dimiringkan. Masalah ini tidak menggugurkan approval, tetapi wajib dibereskan sebelum dikirim sebagai naskah final.

## Temuan Critical

Tidak ada temuan critical.

Tidak ditemukan angka fabrikasi, klaim serangan perangkat IoT asli, klaim IDS produksi *real-time*, klaim PCAP *replay* aktual, atau generalisasi universal yang melanggar batasan Bab 1-3.

## Temuan Major

Tidak ada major blocker.

Catatan keras: status APPROVED ini bergantung pada fakta bahwa draft tetap memakai angka artifact yang sama. Jangan menambah klaim performa, klaim forensik, atau klaim dashboard baru tanpa artifact pendukung.

## Temuan Minor

1. **Panjang naskah terlalu mepet batas bawah.** `wc -w` menunjukkan 1.904 kata. Ini valid, tetapi hanya lebih 4 kata dari batas minimum. Setelah konversi Word, penghapusan placeholder, atau perapihan caption, jumlah kata mudah jatuh di bawah 1.900. Tambahkan 1 paragraf pendek pada 4.4 atau 4.7 agar aman.

2. **Tabel 4.1 belum sepenuhnya seimbang sebagai tabel evaluasi.** Tabel sudah benar, tetapi hanya menampilkan MCC untuk model *advanced*. Karena pembahasan membandingkan *baseline* vs *advanced*, lebih baik tambahkan kolom `MCC Baseline` dan `Delta MCC`. Ini akan membuat Tabel 4.1 lebih kuat dan tidak bergantung pada narasi.

3. **Tabel 4.3 memiliki baris "Error FP/FN" yang terlalu kabur.** Kolom nilai hanya menulis "FP dan FN Track A", padahal artifact menyediakan angka spesifik. Baris ini harus diganti dengan angka yang jelas, misalnya `Decision Tree Track A: FP=2, FN=13` atau `LightGBM Track A: FP=1, FN=4`, sesuai konteks yang ingin dibahas.

4. **Caption gambar masih placeholder.** Urutan Gambar 4.1 sampai 4.4 sudah benar, tetapi untuk Word final placeholder harus diganti menjadi rujukan file artifact atau caption final. Jangan biarkan format `[PLACEHOLDER ...]` masuk naskah final kecuali memang diminta oleh template.

5. **Istilah asing belum sepenuhnya konsisten italic.** Banyak istilah sudah benar, tetapi masih ada `artifact`, `track`, `attack`, `advanced`, `risk score`, `analyst`, `native importance`, `destination IP`, dan `source IP` yang kadang tidak dimiringkan. Rapikan secara konsisten. Untuk nama fitur dalam backtick, jangan diubah.

6. **URL dashboard perlu tanggal akses bila masuk naskah Word.** Kalimat live dashboard aman karena didukung audit artifact, tetapi di naskah akademik lebih rapi jika diberi keterangan akses pada 1 Mei 2026 atau dipindahkan ke catatan kaki/lampiran.

## Perbaikan Wajib Spesifik

Perbaiki Tabel 4.1 agar pembaca langsung melihat dampak *baseline* vs *advanced*. Contoh struktur yang lebih siap:

| Track | Baseline Terbaik | Macro F1 Baseline | MCC Baseline | Advanced Terbaik | Macro F1 Advanced | MCC Advanced | Delta Macro F1 | Delta MCC | Catatan |
|---|---|---:|---:|---|---:|---:|---:|---:|---|
| A | Decision Tree | 0,9667 | 0,9344 | LightGBM Gradient Boosting | 0,9885 | 0,9770 | +0,0218 | +0,0426 | Data besar sangat tidak seimbang |
| B | Random Forest | 1,0000 | 1,0000 | XGBoost Histogram Boosting | 0,9953 | 0,9907 | -0,0047 | -0,0093 | Subset 1:1 kecil |
| C | Random Forest | 1,0000 | 1,0000 | XGBoost Histogram Boosting | 0,9965 | 0,9930 | -0,0035 | -0,0070 | Subset 1:2 kecil |

Perbaiki baris error pada Tabel 4.3. Contoh kalimat aman:

> Pada Track A, Decision Tree menghasilkan 2 *false positive* dan 13 *false negative*, sedangkan LightGBM menurunkannya menjadi 1 *false positive* dan 4 *false negative*. Angka ini digunakan sebagai konteks skenario edukatif, bukan bukti performa operasional IDS.

Tambahkan satu paragraf pendek agar panjang aman. Contoh:

> Secara praktis, hasil ini menunjukkan bahwa evaluasi IDS berbasis *dataset* tidak cukup berhenti pada skor agregat. Pada skenario sangat tidak seimbang, perbedaan kecil pada FP dan FN tetap perlu dibaca karena jumlah normal sangat terbatas. Oleh sebab itu, pembahasan model dalam penelitian ini lebih menekankan jejak kesalahan, keseimbangan metrik, dan batas interpretasi daripada sekadar urutan skor tertinggi.

## Cek Angka Artifact

Lulus.

- Total data: 3.668.522 baris, sesuai `preprocessing_summary.json`.
- Split: train 2.934.817 dan test 733.705, sesuai artifact.
- Track A: train 370 normal + 2.861.463 DoS/DDoS; test 107 normal + 715.421 DoS/DDoS, sesuai `baseline_dataset_tracks.csv`.
- Track B: train 370 + 370; test 107 + 107, sesuai artifact.
- Track C: train 370 + 740; test 107 + 214, sesuai artifact.
- Baseline Track A: Decision Tree, macro F1 0,9667, MCC 0,9344, TN=105, FP=2, FN=13, TP=715.408, sesuai `baseline_summary.json`.
- Baseline Track B/C: Random Forest sempurna pada subset uji, sesuai artifact.
- Advanced Track A: LightGBM, macro F1 0,9885, MCC 0,9770, TN=106, FP=1, FN=4, TP=715.417, sesuai `advanced_summary.json`.
- Advanced Track B: XGBoost, macro F1 0,9953, MCC 0,9907, TN=107, FP=0, FN=1, TP=106, sesuai artifact.
- Advanced Track C: XGBoost, macro F1 0,9965, MCC 0,9930, TN=107, FP=0, FN=1, TP=213, sesuai artifact.
- Delta Track A: macro F1 +0,0218 dan MCC +0,0426, sesuai artifact.
- Delta Track B/C negatif terhadap Random Forest baseline, sesuai artifact.
- Feature importance Decision Tree Track A: `N_IN_Conn_P_DstIP` 0,9689; `drate` 0,0096; `stddev` 0,0074; `proto=arp` 0,0054; `min` 0,0039, sesuai artifact.
- LightGBM native importance dan SHAP Track A cocok dengan `advanced_feature_importance.csv` dan `advanced_shap_summary.csv`.

## Cek Klaim dan Scope

Lulus dengan catatan minor.

Draft sudah aman karena menyatakan penelitian berbasis BoT-IoT CSV, bukan uji perangkat IoT asli. Draft juga jelas menyebut SOC *replay* sebagai visualisasi edukatif, bukan PCAP *replay* aktual. Tidak ada klaim bahwa sistem adalah IDS produksi *real-time*. Tidak ada klaim kausal universal dari *feature importance* atau SHAP.

Bagian forensik sudah cukup hati-hati, terutama kalimat bahwa *feature importance* dan SHAP membantu interpretasi tetapi bukan bukti kausal universal. Pertahankan batasan ini. Jangan ubah menjadi "fitur X membuktikan serangan" atau "model dapat mendeteksi semua DoS/DDoS IoT".

## Cek Format, Tabel, dan Word Readiness

Belum sepenuhnya siap Word, tetapi mudah diperbaiki.

- Struktur 4.1-4.7 lengkap.
- Tabel 4.1, 4.2, 4.3 ada dan angka inti benar.
- Gambar 4.1-4.3 sudah merujuk file artifact repo, dan Gambar 4.4 masih berupa placeholder screenshot dashboard karena file PNG screenshot dashboard belum tersedia di repo.
- Format angka Indonesia konsisten memakai koma desimal dan titik ribuan.
- Istilah asing perlu dirapikan italic.
- Tabel 4.1 dan 4.3 perlu sedikit diperkuat agar tidak terlalu ringkas.
- Untuk Word final, pastikan caption memakai format konsisten: `Gambar 4.x ...` dan `Tabel 4.x ...`, bukan placeholder mentah.

## Final Recommendation

**APPROVED untuk lanjut finalisasi**, dengan revisi minor wajib sebelum naskah Word final. Fokus revisi: amankan jumlah kata, lengkapi Tabel 4.1 dengan MCC/delta, perjelas Tabel 4.3 pada baris FP/FN, ganti placeholder gambar menjadi caption final berbasis file artifact, dan rapikan italic istilah asing. Secara substansi angka dan klaim, BAB 4 sudah aman.
