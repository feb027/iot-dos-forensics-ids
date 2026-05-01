# Fase 7 — Rencana Penulisan Naskah Ilmiah dan Setup Word

## Tujuan Fase

Menyusun naskah ilmiah UAS IoT berdasarkan template dosen, dengan draft utama ditulis dalam Markdown agar mudah dicopy ke Microsoft Word. Word digunakan sebagai media final untuk layout, penomoran, caption, sitasi, dan pengumpulan.

## Prinsip Utama

1. Jangan menulis klaim yang tidak didukung artifact proyek.
2. Jangan menyebut sistem sebagai real-time production IDS.
3. Tulis sebagai prototipe sistem analisis berbasis dataset BoT-IoT.
4. Dashboard dan SOC replay ditulis sebagai visualisasi/simulasi edukatif berbasis artifact, bukan PCAP replay aktual.
5. Semua angka performa model, jumlah data, dan hasil analisis harus bersumber dari file repo.
6. Naskah target 8–15 halaman, sehingga tiap bab harus padat.

## Judul Kerja yang Disarankan

**Sistem Analisis Serangan DoS pada Arsitektur IoT Berbasis Machine Learning dan Network Forensics Menggunakan Dataset BoT-IoT**

Judul ini lebih spesifik daripada judul awal, tetapi tetap mempertahankan inti yang sudah di-ACC dosen.

## Output yang Akan Dibuat

1. `reports/manuscript-word-guide.md`
   - Panduan setup Word: margin, font, style, spacing, numbering, caption, daftar pustaka, dan lampiran.
2. `reports/manuscript-draft.md`
   - Draft naskah utama siap copy-paste ke Word.
3. `reports/manuscript-assets-checklist.md`
   - Checklist gambar/tabel yang harus dimasukkan ke Word.
4. `docs/REVIEW_phase7_manuscript.md`
   - Review naskah oleh reviewer akademik/teknis sebelum final.

## Infrastruktur Word yang Akan Dipakai

### Page Setup

- Paper size: A4.
- Margin:
  - Left/kiri: 4 cm.
  - Top/atas: 3 cm.
  - Right/kanan: 3 cm.
  - Bottom/bawah: 3 cm.
- Orientation: Portrait.

### Font dan Paragraf

- Font utama: Times New Roman.
- Size utama: 12 pt.
- Line spacing: 1.5.
- Alignment: Justify.
- Spacing before: 0 pt.
- Spacing after: 0 pt atau maksimal 6 pt jika Word terlihat terlalu rapat.
- First line indent: 1 cm untuk paragraf isi, kecuali judul, tabel, daftar, dan abstrak jika template dosen tidak meminta indent.

### Style Word yang Akan Dibuat

Disarankan membuat style agar naskah rapi dan mudah diperbaiki:

1. `Normal-Naskah`
   - Times New Roman 12.
   - Justify.
   - Spasi 1.5.
   - First line indent 1 cm.
2. `Judul-Bab`
   - Times New Roman 12 atau 14.
   - Bold.
   - Uppercase.
   - Center atau left sesuai template.
3. `Subbab-1`
   - Times New Roman 12.
   - Bold.
   - Numbering 1.1, 1.2, dst.
4. `Subbab-2`
   - Times New Roman 12.
   - Bold atau regular sesuai kebutuhan.
   - Numbering 1.1.1 jika diperlukan.
5. `Caption-Tabel-Gambar`
   - Times New Roman 11 atau 12.
   - Center untuk caption gambar.
   - Above table untuk tabel, below image untuk gambar.
6. `Daftar-Pustaka`
   - Times New Roman 12.
   - Hanging indent 1 cm.
   - Spasi 1.0 atau 1.5 sesuai preferensi dosen.

### Penomoran Halaman

Rekomendasi aman:

1. Halaman judul tidak diberi nomor tampak.
2. Abstrak mulai halaman baru.
3. Isi Bab 1 sampai daftar pustaka diberi nomor halaman angka Arab: 1, 2, 3, dst.
4. Nomor halaman diletakkan di bawah tengah atau bawah kanan. Jika template tidak menentukan, bawah tengah lebih aman.
5. Gunakan Section Break setelah halaman judul agar nomor halaman cover bisa disembunyikan.

### Heading dan Daftar Isi

Template tidak mewajibkan daftar isi. Untuk naskah 8–15 halaman, daftar isi bisa tidak perlu kecuali dosen meminta.

Namun heading tetap harus memakai style Word agar rapi:

- `1. PENDAHULUAN`
- `1.1 Latar Belakang`
- `1.2 Rumusan Masalah`
- dan seterusnya.

### Gambar dan Tabel

Gunakan format caption Indonesia:

- `Gambar 3.1 Arsitektur Sistem Analisis Serangan DoS pada Arsitektur IoT`
- `Tabel 2.1 Penelitian Terdahulu`
- `Tabel 3.1 Kebutuhan Perangkat Lunak`
- `Tabel 4.1 Hasil Pengujian Model`

Posisi:

- Caption tabel di atas tabel.
- Caption gambar di bawah gambar.
- Semua gambar/tabel harus dirujuk di paragraf, misalnya: “Arsitektur sistem ditunjukkan pada Gambar 3.1.”

### Sitasi dan Daftar Pustaka

Rekomendasi: APA sederhana, karena template memberi contoh APA.

Di teks:

- Naratif: “Menurut Koroniotis et al. (2019), ...”
- Parentetik: “...(Koroniotis et al., 2019).”

Daftar pustaka:

- Urut alfabet berdasarkan nama penulis pertama.
- Gunakan hanging indent.
- Jangan mencantumkan referensi yang tidak dikutip di isi.

## Struktur Naskah yang Disesuaikan dengan Proyek

### Halaman Judul

Mengikuti template dosen.

Data yang masih perlu dari user:

- Nama lengkap: Febnawan Fatur Rochman.
- NPM: 237006029.
- Kelas: A.
- Program Studi: Informatika.
- Fakultas: Teknik.
- Universitas: Universitas Siliwangi.
- Kota: Tasikmalaya.

### Abstrak

Ditulis terakhir setelah Bab 4 dan Bab 5 selesai.

Isi abstrak:

1. Latar belakang singkat IoT rentan DoS.
2. Tujuan: membangun prototipe sistem analisis DoS berbasis BoT-IoT.
3. Metode: preprocessing, machine learning, evaluasi model, network forensics, dashboard.
4. Hasil utama: ambil dari artifact eksperimen.
5. Kesimpulan: sistem dapat mendukung analisis dan visualisasi pola serangan.

### 1. Pendahuluan

Subbab mengikuti template:

- 1.1 Latar Belakang
- 1.2 Rumusan Masalah
- 1.3 Tujuan Penelitian
- 1.4 Manfaat Penelitian
- 1.5 Batasan Masalah

Penekanan:

- IoT berkembang, tetapi rentan serangan DoS/DDoS.
- Serangan DoS mengganggu ketersediaan layanan/perangkat IoT.
- Diperlukan sistem analisis untuk deteksi, interpretasi, dan visualisasi.
- Dataset BoT-IoT dipakai karena merepresentasikan trafik IoT normal dan serangan.

### 2. Tinjauan Pustaka

Subbab disesuaikan:

- 2.1 Internet of Things (IoT)
- 2.2 Keamanan IoT dan Serangan DoS
- 2.3 Intrusion Detection System Berbasis Machine Learning
- 2.4 Digital Forensics dan Network Forensics
- 2.5 Dataset BoT-IoT
- 2.6 Penelitian Terdahulu
- 2.7 Kerangka Pemikiran

Tabel wajib:

- Tabel 2.1 Penelitian Terdahulu.

### 3. Metode Penelitian

Subbab disesuaikan:

- 3.1 Metode Penelitian
- 3.2 Tahapan Penelitian
- 3.3 Dataset dan Sumber Data
- 3.4 Analisis Kebutuhan Sistem
- 3.5 Perancangan Sistem
- 3.6 Preprocessing Data
- 3.7 Algoritma Machine Learning
- 3.8 Analisis Artefak Digital
- 3.9 Metode Pengujian

Catatan:

Karena tidak memakai hardware, bagian perangkat keras diubah menjadi lingkungan komputasi/simulasi. Jangan memaksa ESP32/sensor jika memang tidak digunakan.

### 4. Hasil dan Pembahasan

Subbab disesuaikan:

- 4.1 Hasil Implementasi Sistem
- 4.2 Hasil Pengujian Model
- 4.3 Hasil Analisis Forensik Trafik
- 4.4 Hasil Implementasi Dashboard
- 4.5 Pembahasan
- 4.6 Kelebihan dan Keterbatasan Sistem

Gambar/tabel yang kemungkinan masuk:

- Gambar arsitektur sistem.
- Gambar alur penelitian/flowchart.
- Screenshot dashboard.
- Tabel metrik model.
- Confusion matrix atau ringkasan klasifikasi.
- Tabel skenario SOC replay.

### 5. Kesimpulan dan Saran

Subbab mengikuti template:

- 5.1 Kesimpulan
- 5.2 Saran

Kesimpulan harus menjawab rumusan masalah, bukan mengulang teori.

### Daftar Pustaka

Minimal memuat:

- Paper/dokumentasi BoT-IoT UNSW.
- Referensi IoT security.
- Referensi DoS/DDoS pada IoT.
- Referensi IDS/machine learning.
- Referensi network forensics/digital forensics.

### Lampiran Opsional

Lampiran yang relevan:

- Lampiran A. Screenshot Dashboard.
- Lampiran B. Diagram Sistem.
- Lampiran C. Ringkasan Source Code/Repository.
- Lampiran D. Hasil Pengujian Tambahan.

## Rencana Eksekusi Penulisan

### Fase 7.0 — Setup Infrastruktur Word

Output:

- Panduan Word final.
- Struktur heading final.
- Checklist gambar/tabel.

Belum menulis isi bab panjang.

### Fase 7.1 — Audit Artifact dan Angka

Tujuan:

- Mengumpulkan angka yang boleh dikutip.
- Menentukan tabel/gambar yang masuk naskah.
- Memastikan tidak ada klaim tanpa sumber.

Sumber:

- `results/metrics/`
- `results/tables/`
- `results/figures/`
- `dashboard/data/dashboard-data.json`
- `reports/progress-*.md`
- review tiap fase.

### Fase 7.2 — Draft Bab 1

Output:

- Pendahuluan lengkap.
- Rumusan masalah spesifik proyek.
- Tujuan, manfaat, batasan masalah.

### Fase 7.3 — Draft Bab 2

Output:

- Tinjauan pustaka.
- Tabel penelitian terdahulu.
- Kerangka pemikiran.

Perlu riset referensi terkini dan validasi sitasi.

### Fase 7.4 — Draft Bab 3

Output:

- Metode penelitian.
- Tahapan penelitian.
- Dataset, preprocessing, model, evaluasi, forensik, dashboard.

### Fase 7.5 — Draft Bab 4

Output:

- Hasil implementasi.
- Hasil model.
- Analisis forensik.
- Dashboard.
- Pembahasan keterbatasan.

### Fase 7.6 — Draft Bab 5, Abstrak, Daftar Pustaka

Output:

- Kesimpulan dan saran.
- Abstrak final.
- Kata kunci.
- Daftar pustaka.

### Fase 7.7 — Review dan Revisi

Output:

- Review dosen-style.
- Perbaikan bahasa, struktur, sitasi, dan klaim.
- Final Markdown siap dipindahkan ke Word.

## Data yang Perlu Diminta dari User Sebelum Halaman Judul

- Nama lengkap: Febnawan Fatur Rochman.
- NPM: 237006029.
- Kelas: A.
- Program Studi: Informatika.
- Fakultas: Teknik.
- Universitas: Universitas Siliwangi.
- Kota: Tasikmalaya.

Jika data belum ada, halaman judul memakai placeholder dulu.

## Keputusan yang Sudah Dipilih

1. Judul memakai versi spesifik: **Sistem Analisis Serangan DoS pada Arsitektur IoT Berbasis Machine Learning dan Network Forensics Menggunakan Dataset BoT-IoT**.
2. Sitasi memakai **APA sederhana** karena template memberi contoh APA dan format ini paling mudah dikerjakan manual di Word.
3. Daftar isi **tidak dimasukkan** karena template tidak meminta dan panjang naskah hanya 8–15 halaman.
4. Target panjang: **10–12 halaman**.
5. Lampiran dipakai secara selektif: gambar/tabel utama masuk Bab 3–4, sedangkan lampiran hanya untuk screenshot dashboard tambahan, potongan source code, atau hasil pengujian rinci jika halaman utama terlalu penuh.

## Rekomendasi Final

- Gunakan APA sederhana, bukan IEEE, karena template dosen mencontohkan format nama-tahun.
- Tidak perlu daftar isi kecuali dosen meminta secara lisan.
- Gunakan lampiran ringan; jangan jadikan lampiran sebagai tempat isi utama.
- Fokuskan 10–12 halaman pada alur: masalah → metode → hasil → pembahasan → batasan.
