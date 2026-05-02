# Codex Review Phase 7 Daftar Pustaka dan Lampiran

Tanggal review: Sat May 2 06:36:19 AM UTC 2026

Draft direview:
- `reports/manuscript-daftar-pustaka.md`
- `reports/manuscript-lampiran.md`

## Score
**94/100**

## Verdict
**APPROVED**

## Ringkasan Keputusan

Daftar pustaka dan lampiran sudah layak masuk finalisasi naskah UAS. Daftar pustaka memuat seluruh sumber yang benar-benar dirujuk pada BAB 1-5, termasuk Koroniotis et al. (2019), UNSW Research (2021), Jamalipour & Murali (2022), Jayalaxmi et al. (2022), Pakmehr et al. (2024), Shukla et al. (2024), Wu et al. (2021), Koroniotis et al. (2020), dan Kalakoti et al. (2022). RT-IoT2022 juga masuk secara wajar karena disebut sebagai dataset alternatif/saran pada BAB 5.

Lampiran sudah membantu kesiapan dokumen Word karena menunjuk artefak yang benar-benar ada di repo: `results/metrics/`, `results/tables/`, `results/figures/`, `dashboard/data/`, `dashboard/demo.html`, dan dokumen review fase 7. Lampiran juga menjaga batasan penting bahwa dashboard dan SOC *replay* adalah visualisasi edukatif, bukan IDS produksi *real-time*, bukan PCAP *replay* aktual, dan bukan sistem operasional.

## Critical Issues

Tidak ada critical issue.

## Major Issues

Tidak ada major issue.

## Minor Issues

1. Entri UNSW Research berupa halaman web dataset belum mencantumkan tanggal akses pada daftar pustaka. Ini bukan penghambat approval, tetapi sebaiknya ditambahkan saat final Word karena halaman web dapat berubah.
2. Entri RT-IoT2022 ditulis tahun 2024, sedangkan `references/references.bib` memakai tahun 2023 dan `references/literature-matrix.md` menulis 2023/2024. Karena RT-IoT2022 hanya dipakai sebagai dataset alternatif/saran, dampaknya minor, tetapi tahun sebaiknya diseragamkan dengan metadata yang dipilih.
3. Lampiran H menyebut banyak dokumen review. Ini valid sebagai jejak proses, tetapi untuk Word final sebaiknya hanya dipilih dokumen inti bila halaman naskah terbatas.

## Cek Daftar Pustaka

Lulus.

Daftar pustaka sudah mencakup sumber yang dikutip atau dirujuk dalam BAB 1-5:

- `Koroniotis et al. (2019)` tersedia untuk BoT-IoT dan *network forensic analytics*.
- `UNSW Research (2021)` tersedia untuk halaman resmi BoT-IoT.
- `Jamalipour & Murali (2022)` tersedia untuk taksonomi IDS IoT berbasis *machine learning*.
- `Jayalaxmi et al. (2022)` tersedia untuk survey IDS/IPS IoT.
- `Pakmehr et al. (2024)` tersedia untuk survey deteksi DDoS pada IoT.
- `Shukla et al. (2024)` tersedia untuk review deteksi DDoS berbasis trafik IoT.
- `Wu et al. (2021)` tersedia untuk *IoT network traffic analysis* dan forensik.
- `Koroniotis et al. (2020)` tersedia untuk kerangka *network forensic* IoT berbasis *deep learning*.
- `Kalakoti et al. (2022)` tersedia untuk *feature selection* botnet/IoT.
- `Sharmila & Nagapadma` untuk RT-IoT2022 tersedia sebagai dataset alternatif dan referensi saran penelitian lanjutan.

Tidak ditemukan referensi yang jelas-jelas dikutip dalam BAB 1-5 tetapi hilang dari daftar pustaka. Sebaliknya, daftar pustaka juga tidak terlalu melebar dengan memasukkan seluruh literatur matrix yang tidak dipakai dalam naskah inti. Ini baik untuk naskah UAS karena daftar pustaka tetap fokus.

Detail DOI, jurnal, volume, nomor, halaman, dan artikel terlihat konsisten dengan `references/literature-matrix.md` dan `references/references.bib` untuk sumber utama. Saya tidak menemukan indikasi DOI atau klaim bibliografis yang tampak diinventarisasi tanpa sumber internal. Catatan minor hanya pada konsistensi tahun RT-IoT2022 dan tanggal akses web UNSW.

## Cek Lampiran

Lulus.

Lampiran sudah dibagi rapi menjadi bagian repositori/dashboard, artefak dataset dan *preprocessing*, artefak model, artefak *network forensics* dan *explainability*, gambar pendukung, file data dashboard, perintah reproduksi, serta dokumen review/verifikasi.

Path yang disebut dalam lampiran sudah tersedia di repo, termasuk:

- `results/metrics/dataset_audit.json`
- `results/metrics/preprocessing_summary.json`
- `results/metrics/baseline_summary.json`
- `results/metrics/advanced_summary.json`
- `results/metrics/forensic_summary.json`
- `results/tables/baseline_dataset_tracks.csv`
- `results/tables/baseline_model_metrics.csv`
- `results/tables/advanced_model_metrics.csv`
- `results/tables/advanced_confusion_matrices.csv`
- `results/tables/forensic_error_examples.csv`
- `results/tables/advanced_shap_summary.csv`
- `results/figures/advanced_macro_f1_vs_baseline.png`
- `results/figures/advanced_confusion_matrix_grid.png`
- `results/figures/advanced_shap_summary.png`
- `dashboard/data/dashboard-data.json`
- `dashboard/data/demo-scenarios.json`
- `dashboard/demo.html`
- dokumen review BAB 1 sampai BAB 5 pada `docs/`.

Lampiran tidak menyertakan raw dataset, secrets, kredensial, full PCAP, atau model besar. Kalimat "Data mentah tidak dilampirkan langsung di naskah" sudah tepat dan sesuai aturan dataset proyek.

## Cek Klaim dan Scope

Lulus.

Lampiran menegaskan batasan yang dibutuhkan:

- Dashboard adalah media visualisasi edukatif berbasis *artifact* eksperimen.
- Dashboard bukan IDS produksi *real-time*.
- SOC *replay* bukan PCAP *replay* aktual.
- Data dashboard bukan data sensor langsung atau aliran paket jaringan *real-time*.
- Fitur penting dibaca sebagai indikator artefak trafik pada dataset, bukan penyebab kausal serangan.
- Track B dan Track C diperlakukan sebagai subset terkontrol, bukan bukti generalisasi dunia nyata.

Pernyataan tersebut konsisten dengan BAB 1, BAB 3, BAB 4, BAB 5, `reports/manuscript-artifact-audit.md`, `docs/REVIEW_phase7_bab4_final.md`, dan `docs/REVIEW_phase7_bab5_codex.md`.

## Cek Format dan Word Readiness

Lulus.

Daftar pustaka sudah menggunakan gaya yang cukup konsisten untuk naskah akademik: nama penulis, tahun, judul, nama jurnal atau repositori, volume/nomor/halaman atau artikel jika tersedia, dan DOI/URL. Format italic pada nama jurnal dan dataset sudah cukup rapi untuk dipindahkan ke Word.

Lampiran sudah Word-ready karena:

- heading lampiran jelas dari Lampiran A sampai Lampiran H;
- path artefak ditulis dengan format monospace sehingga mudah dicek;
- gambar utama untuk BAB 4 sudah disebut dengan pasangan fungsi/caption;
- perintah reproduksi dipisahkan dalam blok kode;
- ada catatan pemilihan lampiran agar dokumen Word tidak terlalu panjang.

Satu hal yang perlu diperhatikan saat konversi ke Word: path artefak panjang sebaiknya memakai font kecil atau tabel dua kolom agar tidak melebar keluar margin.

## Rekomendasi Revisi Konkret

Revisi berikut bersifat opsional dan tidak menghalangi approval.

1. File: `reports/manuscript-daftar-pustaka.md`, entri `UNSW Research. (2021)`.
   - Tambahkan keterangan akses setelah URL, misalnya: `Diakses pada 2 Mei 2026.`
   - Alasan akademik: halaman web dataset dapat berubah, sehingga tanggal akses membantu keterlacakan.

2. File: `reports/manuscript-daftar-pustaka.md`, entri `Sharmila, B. S., & Nagapadma, R. (2024). *RT-IoT2022* [Dataset].`
   - Seragamkan tahun dengan metadata repo yang dipakai. Jika mengikuti `references/references.bib`, gunakan tahun 2023; jika mengikuti halaman UCI terbaru, pertahankan 2024 tetapi pastikan ada alasan/tanggal akses.
   - Alasan akademik: menghindari ketidakkonsistenan kecil antara daftar pustaka, BibTeX, dan literature matrix.

3. File: `reports/manuscript-lampiran.md`, Lampiran H.
   - Bila dokumen Word mendekati batas halaman, cukup pertahankan review final yang paling relevan, misalnya `docs/REVIEW_phase7_bab4_final.md`, `docs/REVIEW_phase7_bab5_codex.md`, dan review daftar pustaka/lampiran ini.
   - Alasan akademik: lampiran harus mendukung klaim dan verifikasi, bukan membuat dokumen akhir terlalu berat.

4. File: `reports/manuscript-lampiran.md`, Lampiran E.
   - Setelah screenshot dashboard tersedia, ganti catatan "Screenshot final perlu diambil..." menjadi path file screenshot yang benar-benar ada di repo.
   - Alasan akademik: Word final lebih kuat jika setiap gambar yang disebut memiliki file artefak yang spesifik.

## Final Recommendation

**APPROVED untuk finalisasi daftar pustaka dan lampiran.** Draft memenuhi gate approval karena score >= 90, tidak memiliki critical/major issue, daftar pustaka mencakup sumber utama BAB 1-5, lampiran menunjuk artefak yang ada di repo, dan scope dashboard/SOC *replay* sudah aman untuk naskah UAS IoT + Cyber Security + Digital Forensics.
