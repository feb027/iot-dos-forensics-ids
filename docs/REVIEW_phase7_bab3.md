# Review Phase 7 Bab 3

Tanggal review: Fri May 1 02:53:05 PM UTC 2026.

Draft yang direview: `reports/manuscript-draft-bab3.md`

## Score

**92/100**

## Verdict

**APPROVED**

## Ringkasan Keputusan

Bab 3 layak masuk naskah Word dengan revisi minor. Struktur 3.1 sampai 3.9 lengkap, angka dataset cocok dengan artefak, ruang lingkup metodologi aman, dan bagian pengujian sudah menolak akurasi sebagai klaim utama. Tidak ditemukan klaim berbahaya seperti serangan ke perangkat asli, IDS produksi *real-time*, PCAP *replay* aktual, atau generalisasi universal.

Kelemahan utama bukan pada substansi, melainkan pada kerapian format Word: penyebutan Gambar 3.1 dan Gambar 3.2 masih berupa rujukan naratif, belum tegas sebagai placeholder gambar yang akan disisipkan di Word. Ada juga beberapa istilah asing yang belum konsisten memakai italic. Ini perlu dibersihkan sebelum final, tetapi tidak sampai menggugurkan Bab 3.

## Temuan Critical

Tidak ada temuan critical.

## Temuan Major

Tidak ada major blocker.

## Temuan Minor

1. **Placeholder gambar belum cukup eksplisit untuk Word.**  
   Draft menyebut Gambar 3.1 dan Gambar 3.2, tetapi belum ada baris placeholder yang jelas untuk penempatan gambar. Untuk naskah Word, ini rawan terlewat saat copy-paste.

2. **Kalimat rujukan gambar masih kaku.**  
   Kalimat "Gambar 3.2 Alur Tahapan Penelitian menunjukkan..." lebih cocok diganti menjadi kalimat akademik yang normal.

3. **Istilah asing belum sepenuhnya konsisten.**  
   Beberapa istilah seperti `working mirror`, `baseline`, `track`, `Gradient Boosting`, `Static web dashboard`, dan `identifier bias` belum konsisten di-*italic*. Akronim dan nama proper seperti IoT, IDS, CSV, BoT-IoT, UNSW, LightGBM, XGBoost, SHAP tidak perlu di-*italic*.

4. **Tabel kebutuhan perangkat lunak masih bisa dibuat lebih spesifik.**  
   Tabel 3.2 aman karena tidak mengklaim hardware IoT, tetapi komponen `Static web dashboard` sebaiknya disesuaikan menjadi teknologi yang nyata dipakai, misalnya HTML/CSS/JavaScript atau dashboard statis berbasis data JSON/CSV.

## Perbaikan Wajib Spesifik

1. Tambahkan placeholder gambar eksplisit saat dipindahkan ke Word:

   **Contoh untuk Gambar 3.1:**

   `[PLACEHOLDER GAMBAR 3.1: Arsitektur Sistem Analisis Serangan DoS pada Arsitektur IoT]`

   Caption Word:

   `Gambar 3.1 Arsitektur Sistem Analisis Serangan DoS pada Arsitektur IoT`

2. Rapikan rujukan Gambar 3.2.

   Kalimat saat ini:

   `Gambar 3.2 Alur Tahapan Penelitian menunjukkan urutan kerja tersebut secara konseptual.`

   Perbaikan:

   `Urutan kerja penelitian ditunjukkan secara konseptual pada Gambar 3.2.`

3. Konsistenkan italic istilah asing.

   Contoh aman:

   - `*working mirror*`
   - `*baseline*`
   - `*track*`
   - `*identifier bias*`
   - `*gradient boosting*`
   - `*dashboard*`

   Jangan italic untuk nama proper atau akronim: BoT-IoT, UNSW, CSV, IoT, IDS, LightGBM, XGBoost, SHAP.

## Cek Angka Artifact

Status: **lulus**.

- Total data **3.668.522 baris**: benar, cocok dengan `results/metrics/preprocessing_summary.json`.
- Split *train* **2.934.817 baris**: benar.
- Split *test* **733.705 baris**: benar.
- Fitur kandidat **10**: benar.
- Fitur kategorikal **1**, yaitu `proto`: benar.
- Fitur numerik **9**: benar.
- Kolom dikeluarkan **9**: benar, yaitu `attack`, `category`, `daddr`, `dport`, `pkSeqID`, `saddr`, `seq`, `sport`, dan `subcategory`.
- Track A: **2.861.833 train** dan **715.528 test** dengan komposisi normal/DoS-DDoS benar.
- Track B: **740 train** dan **214 test** dengan rasio 1:1 benar.
- Track C: **1.110 train** dan **321 test** dengan rasio 1:2 benar.
- Tabel 3.1 memuat angka Track A/B/C dengan benar sesuai artifact audit dan `results/tables/baseline_dataset_tracks.csv`.
- Tabel 3.2 ada dan tidak mengklaim sensor, mikrokontroler, gateway fisik, atau hardware IoT.

## Cek Metode dan Scope

Status: **lulus**.

- Struktur 3.1 sampai 3.9 lengkap sesuai kebutuhan Bab 3.
- Metode *preprocessing* menjelaskan seleksi label, pengecualian serangan lain, fitur kandidat, *encoding*, *scaling*, dan pencegahan *leakage*.
- Model dijelaskan secara metodologis dan tidak mencuri pembahasan hasil Bab 4.
- Fitur artefak digital lengkap: `N_IN_Conn_P_DstIP`, `N_IN_Conn_P_SrcIP`, `srate`, `drate`, `state_number`, `proto`, `mean`, `stddev`, `min`, dan `max`.
- Metode pengujian sudah memakai macro F1, MCC, balanced accuracy, recall normal, recall attack, dan *confusion matrix*.
- Penjelasan bahwa akurasi bukan klaim utama sudah benar dan penting karena Track A sangat tidak seimbang.

## Cek Klaim/Scope

Status: **aman**.

Tidak ditemukan klaim berbahaya berikut:

- menyerang perangkat IoT asli,
- menguji jaringan produksi,
- mengklaim IDS produksi *real-time*,
- melakukan PCAP *replay* aktual,
- mengklaim generalisasi universal untuk semua jaringan IoT,
- menyebut fitur penting sebagai penyebab serangan secara kausal.

Draft justru secara eksplisit membatasi sistem sebagai prototipe berbasis dataset dan SOC *replay* sebagai visualisasi edukatif berbasis artefak. Ini konsisten dengan Bab 1 dan Bab 2.

## Cek Format/Tabel/Word

Status: **lulus dengan revisi minor**.

- Panjang **1.844 kata**, masuk rentang 1.500-1.900 kata dan cocok untuk target naskah 8-15 halaman.
- Tabel 3.1 dan Tabel 3.2 sudah ada.
- Caption tabel menggunakan format Indonesia dan masih aman untuk Word.
- Gambar 3.1 dan Gambar 3.2 sudah disebut, tetapi perlu placeholder eksplisit agar tidak hilang saat penyusunan Word.
- Bahasa Indonesia akademik cukup natural untuk mahasiswa Informatika semester 6. Tidak terlalu kaku dan tidak berlebihan.
- Istilah asing cukup banyak sudah di-*italic*, tetapi konsistensinya perlu satu kali penyisiran sebelum final.

## Final Recommendation

**APPROVED dengan revisi minor format.** Bab 3 sudah kuat secara metodologi dan aman secara akademik. Perbaikan wajib sebelum final Word adalah memperjelas placeholder Gambar 3.1/Gambar 3.2, merapikan satu-dua kalimat rujukan gambar, dan menyisir konsistensi italic istilah asing. Jangan ubah angka dataset atau scope klaim karena bagian itu sudah benar.
