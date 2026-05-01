# Review Phase 7 BAB 1

Tanggal review: Fri May 1 01:54:42 PM UTC 2026

Reviewer: Codex Lecturer Reviewer

Draft: `reports/manuscript-draft-bab1.md`

## Score

**91/100**

## Verdict

**APPROVED**

## Ringkasan Keputusan

BAB 1 sudah layak masuk tahap berikutnya. Struktur 1.1 sampai 1.5 sesuai rencana naskah, rumusan masalah dan tujuan sejajar, scope tetap berada pada IoT, *cyber security*, dan *digital forensics*, serta klaim berbahaya sudah dibatasi dengan cukup jelas. Angka dataset yang dipakai juga sesuai dengan artifact audit.

Catatan utama sebelum Bab 2 bukan blocker, tetapi tetap perlu dibereskan saat penyuntingan akhir: beberapa istilah asing panjang belum di-*italic*, panjang BAB 1 mulai mendekati batas atas untuk target dua halaman Word, dan gaya bahasa masih agak terlalu rapi/seragam pada beberapa paragraf sehingga perlu sedikit dibuat lebih natural.

## Rincian Rubrik

| Rubrik | Bobot | Nilai | Catatan |
|---|---:|---:|---|
| Kesesuaian template dosen | 20 | 19 | Struktur BAB 1 lengkap: 1.1 Latar Belakang, 1.2 Rumusan Masalah, 1.3 Tujuan Penelitian, 1.4 Manfaat Penelitian, 1.5 Batasan Masalah. |
| Ketepatan scope judul dan masalah | 20 | 19 | Scope kuat dan tidak melebar. Fokus normal vs DoS/DDoS, BoT-IoT, ML, *network forensics*, dan *dashboard* edukatif konsisten. |
| Kekuatan latar belakang dan alur argumen | 20 | 18 | Alur dari IoT, ancaman DoS/DDoS, dataset, prototipe, lalu evaluasi imbalance sudah masuk akal. Masih bisa dibuat sedikit lebih tajam pada gap penelitian. |
| Keamanan klaim akademik dan fakta artifact | 15 | 15 | Tidak ada klaim hasil eksperimen palsu. Angka 107 normal dan 715.421 DoS/DDoS sesuai artifact audit. |
| Bahasa Indonesia akademik natural/anti-AI | 15 | 12 | Jelas dan layak akademik, tetapi beberapa kalimat terasa terlalu generik dan terlalu halus. Perlu sedikit variasi agar tidak terasa seperti teks template AI. |
| Sitasi APA, italic istilah asing, Markdown | 10 | 8 | Sitasi yang muncul ada di matrix. Format Markdown rapi. Masih ada istilah asing yang sebaiknya di-*italic*. |

## Temuan Critical

Tidak ada critical issue.

## Temuan Major

Tidak ada major blocker.

## Temuan Minor

1. **Gap penelitian belum cukup tajam.** Latar belakang sudah aman, tetapi masih lebih banyak menjelaskan konteks daripada menegaskan kekosongan yang diisi penelitian. Tambahkan satu kalimat yang menekankan bahwa proyek ini tidak hanya mengejar klasifikasi, tetapi juga audit data dan interpretasi artefak trafik.

   Contoh perbaikan:

   > Dengan demikian, penelitian ini menempatkan deteksi sebagai bagian dari alur analisis yang dapat diaudit, bukan sekadar pencarian nilai akurasi tertinggi.

2. **Beberapa istilah asing panjang belum di-*italic*.** Frasa seperti `Denial of Service`, `Distributed Denial of Service`, dan `SOC replay` perlu dicek. Akronim seperti IoT, DoS, DDoS, IDS, UNSW, dan BoT-IoT tidak perlu dipaksa italic.

   Contoh perbaikan:

   > Salah satu ancaman yang relevan pada arsitektur IoT adalah serangan *Denial of Service* (DoS) dan *Distributed Denial of Service* (DDoS).

3. **Panjang BAB 1 agak padat untuk target dua halaman Word.** Draft berisi sekitar 861 kata. Dengan Times New Roman 12, spasi 1,5, margin skripsi/tugas kampus, ini berpotensi menjadi lebih dari dua halaman jika judul, numbering, dan spacing Word ikut dihitung. Kalau template dosen ketat dua halaman, pangkas bagian manfaat atau batasan yang terlalu rinci.

4. **Bahasa masih sedikit terlalu bersih dan seragam.** Ini bukan masalah substansi, tetapi beberapa paragraf memakai pola kalimat yang mirip: konteks umum, manfaat, lalu pembatasan. Untuk naskah mahasiswa semester 6, boleh dibuat lebih langsung.

   Contoh alternatif:

   > Karena itu, penelitian ini tidak hanya melihat apakah model dapat membedakan trafik normal dan serangan, tetapi juga menelusuri fitur trafik apa yang paling berperan dalam proses deteksi.

## Perbaikan Wajib Sebelum Bab 2

1. Rapikan italic istilah asing, terutama *Denial of Service*, *Distributed Denial of Service*, *real-time*, *machine learning*, *preprocessing*, *network forensics*, *dashboard*, *flow*, dan *replay* jika berdiri sebagai istilah asing. Jangan italic akronim dan nama proper seperti IoT, DoS, DDoS, IDS, UNSW, BoT-IoT, dan SOC.
2. Tambahkan satu kalimat gap penelitian pada akhir paragraf ketiga atau awal paragraf keempat agar kontribusi Bab 1 lebih tajam.
3. Saat masuk Word, cek panjang aktual. Jika melewati dua halaman, pangkas batasan masalah nomor 7 atau gabungkan nomor 3 dan 5 karena sama-sama membatasi prototipe dan visualisasi.

## Cek Wajib

1. **Struktur 1.1-1.5:** Lulus. Struktur lengkap dan urutan sesuai template.
2. **Rumusan masalah 4 poin dan tujuan sejajar 4 poin:** Lulus. Poin 1-4 pada tujuan mengikuti rumusan masalah secara langsung.
3. **Scope IoT + Cyber Security + Digital Forensics:** Lulus. Scope tidak melebar ke hardware, mitigasi jaringan operasional, atau IDS produksi.
4. **Klaim berbahaya:** Lulus. Draft secara eksplisit menyatakan bukan serangan perangkat asli, bukan IDS produksi *real-time*, bukan replay PCAP aktual, dan tidak mengklaim generalisasi universal.
5. **Angka dataset 107 normal dan 715.421 DoS/DDoS:** Lulus. Angka sesuai `reports/manuscript-artifact-audit.md`, bagian Scope DoS/DDoS vs Normal Track A realistis test set: 107 normal dan 715.421 DoS/DDoS.
6. **Sitasi ada di literature matrix:** Lulus. Jamalipour & Murali (2022), Jayalaxmi et al. (2022), Pakmehr et al. (2024), Shukla et al. (2024), Koroniotis et al. (2019), dan UNSW Research (2021) semuanya ada di `references/literature-matrix.md`.
7. **Italic istilah asing:** Lulus sebagian. Banyak istilah sudah benar, tetapi frasa panjang DoS/DDoS perlu diperbaiki.
8. **Bahasa terlalu AI-polished/generik/kaku:** Minor. Teks layak, tetapi masih terlalu steril pada beberapa bagian.
9. **Panjang cocok untuk target dua halaman Word:** Lulus bersyarat. Masih mungkin masuk, tetapi harus dicek di Word.
10. **Perbaikan sebelum Bab 2:** Ada minor fix format dan ketajaman gap, tetapi tidak menghambat penulisan Bab 2.

## Cek Fakta Artifact

- Klaim data uji memuat 107 baris normal dan 715.421 baris DoS/DDoS benar berdasarkan artifact audit.
- Draft tidak memakai angka performa model, sehingga tidak ada risiko klaim metrik yang belum ditempatkan pada Bab 4.
- Draft sudah menyebut imbalance sebagai batasan evaluasi. Ini tepat dan penting karena jumlah normal sangat kecil dibanding DoS/DDoS.
- Tidak ada klaim bahwa sistem sudah berjalan pada jaringan IoT nyata atau produksi.

## Cek Sitasi

- Semua sitasi yang muncul di BAB 1 tersedia pada literature matrix.
- Format parentetik sudah cukup konsisten untuk APA sederhana.
- Untuk Bab 2 nanti, pastikan setiap sumber yang dikutip di isi masuk daftar pustaka, dan jangan menambah referensi baru tanpa masuk matrix atau `references.bib`.

## Cek Bahasa dan Format

- Markdown rapi dan mudah dipindahkan ke Word.
- Label BAB dan subbab sesuai pola naskah.
- Bahasa Indonesia jelas dan tidak berlebihan.
- Istilah asing mayoritas sudah di-*italic*, tetapi masih perlu penyisiran kecil.
- Hindari membuat Bab 1 terdengar seperti janji sistem keamanan operasional. Draft saat ini sudah aman, jangan dibuat lebih bombastis pada revisi.

## Final Recommendation

**APPROVED dengan minor revision.** Lanjutkan ke Bab 2 setelah memperbaiki italic istilah asing dan menambahkan satu kalimat gap penelitian. Tidak ada blocker metodologis atau klaim berbahaya pada BAB 1.
