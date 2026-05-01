# Review Phase 7 Bab 2

Tanggal review: Fri May 1 02:17:29 PM UTC 2026

Draft direview: `reports/manuscript-draft-bab2.md`

## Score

**86/100**

Rincian rubrik:

| Komponen | Bobot | Skor |
|---|---:|---:|
| Kesesuaian struktur template Bab 2 | 15 | 14 |
| Kelengkapan teori IoT, DoS/DDoS, IDS ML, forensik, BoT-IoT | 25 | 21 |
| Kualitas penelitian terdahulu dan sintesis gap | 20 | 16 |
| Keamanan klaim akademik dan konsistensi dengan Bab 1/artifact | 15 | 14 |
| Bahasa Indonesia akademik natural/anti-AI | 15 | 12 |
| Sitasi APA, italic istilah asing, format Markdown/table | 10 | 9 |

## Verdict

**NEEDS REVISION**

Masuk kategori revisi karena fondasinya sudah benar, tetapi Bab 2 masih terlalu panjang untuk target 2-2,5 halaman Word dan beberapa klaim teori belum cukup ditopang sitasi. Tidak ada critical blocker, tetapi ada major blocker pada kepadatan dan sintesis.

## Ringkasan Keputusan

Bab 2 sudah mengikuti struktur yang diminta, cakupan teorinya lengkap, dan tidak melanggar batasan besar proyek. Draft tidak mengarang hasil eksperimen, tidak mengklaim IDS produksi *real-time*, tidak mengklaim menyerang perangkat asli, dan tidak menyamakan SOC *replay* dengan *replay* PCAP aktual. Penjelasan BoT-IoT juga aman: UNSW disebut, normal/attack disebut, DoS/DDoS disebut, format PCAP/Argus/CSV disebut, dan rujukan primer tetap Koroniotis et al. (2019) serta UNSW Research (2021).

Masalah utamanya: naskah masih terasa seperti Bab 2 versi lengkap, bukan versi naskah UAS 8-15 halaman. Dengan 1.721 kata ditambah tabel, Bab 2 kemungkinan melewati 2,5 halaman Word pada Times New Roman 12 spasi 1,5. Sintesis penelitian terdahulu sudah ada, tetapi masih terlalu umum dan belum cukup tajam menunjukkan gap proyek.

## Temuan Critical

Tidak ada temuan critical.

## Temuan Major

1. **Terlalu panjang untuk target 2-2,5 halaman Word.**  
   Bab 2 berisi 1.721 kata sebelum dipindahkan ke Word. Dengan tabel, ini berpotensi menjadi sekitar 4-5 halaman. Untuk naskah UAS yang totalnya 8-15 halaman, Bab 2 harus dipadatkan. Bagian yang paling bisa diringkas adalah 2.1, paragraf metrik pada 2.3, dan 2.7.

2. **Sebagian definisi teori masih kurang sitasi.**  
   Definisi IoT pada 2.1, definisi IDS pada 2.3, definisi *digital forensics*/*network forensics* pada 2.4, dan pembahasan *chain of custody* perlu sitasi atau perlu ditulis lebih terbatas sebagai konteks penelitian. Klaim teori boleh sederhana, tetapi tetap harus punya sandaran pustaka.

3. **Sintesis gap penelitian terdahulu masih terlalu sopan dan generik.**  
   Paragraf setelah Tabel 2.1 sudah menyebut irisan IDS IoT, DoS/DDoS, dan *network forensics*, tetapi belum cukup eksplisit membedakan proyek ini dari studi terdahulu. Gap yang aman adalah: banyak literatur menekankan deteksi atau performa model, sedangkan proyek ini menekankan alur audit dataset, pembatasan scope normal vs DoS/DDoS, evaluasi metrik untuk data tidak seimbang, dan interpretasi fitur sebagai artefak forensik.

## Temuan Minor

1. **Istilah asing cukup konsisten, tetapi jangan berlebihan.**  
   Penggunaan italic untuk *dataset*, *machine learning*, *network forensics*, *flow*, *payload*, *metadata*, *preprocessing*, dan *dashboard* sudah cukup. Akronim dan nama proper seperti IoT, IDS, DoS, DDoS, BoT-IoT, UNSW, PCAP, Argus, CSV, MCC, dan SOC tidak perlu italic. Draft sudah mengikuti ini secara umum.

2. **Beberapa kalimat masih terasa repetitif.**  
   Frasa “artefak jaringan”, “pola trafik”, “analisis trafik”, dan “fitur flow” muncul berulang. Ini bukan salah konsep, tetapi membuat Bab 2 terasa panjang dan agak AI-like.

3. **Bagian 2.7 terlalu mendekati Bab 3.**  
   Kerangka pemikiran boleh menyebut alur penelitian, tetapi jangan terlalu operasional. Detail audit, *preprocessing*, metrik, dan visualisasi sebaiknya dipadatkan karena nanti akan dijelaskan di Bab 3 dan Bab 4.

## Perbaikan Wajib Spesifik

1. **Pangkas 25-35% isi Bab 2.**  
   Targetkan sekitar 1.100-1.300 kata termasuk pengantar tabel. Saran pemangkasan:
   - 2.1 cukup 2 paragraf.
   - 2.3 paragraf metrik cukup 3-4 kalimat.
   - 2.7 cukup 1 paragraf padat atau 2 paragraf pendek.

2. **Tambahkan sitasi pada definisi teori utama.**  
   Contoh revisi aman untuk 2.1:
   > Dalam penelitian ini, IoT dipahami sebagai sistem berlapis yang menghubungkan perangkat, jaringan, layanan komputasi, dan aplikasi untuk menghasilkan serta mengolah data. Pada konteks keamanan, trafik jaringan IoT dapat dianalisis sebagai sumber pola komunikasi dan indikasi intrusi (Jamalipour & Murali, 2022; Jayalaxmi et al., 2022).

3. **Batasi klaim *chain of custody*.**  
   Jangan membuat pembaca mengira penelitian ini menjalankan prosedur forensik legal penuh. Contoh kalimat yang lebih aman:
   > Dalam konteks penelitian berbasis dataset, prinsip keterlacakan diterapkan secara terbatas melalui pencatatan sumber data, proses transformasi, pemilihan fitur, hasil model, dan artifact visualisasi. Prinsip ini tidak dimaknai sebagai prosedur *chain of custody* forensik legal penuh.

4. **Perkuat gap setelah Tabel 2.1.**  
   Contoh kalimat:
   > Literatur terdahulu menunjukkan bahwa deteksi DoS/DDoS pada IoT umumnya berfokus pada pemilihan metode dan capaian performa model. Gap yang diambil penelitian ini adalah penyusunan alur analisis yang lebih mudah diaudit, mulai dari audit dataset BoT-IoT, pembentukan skenario normal vs DoS/DDoS, pemilihan metrik untuk data tidak seimbang, sampai interpretasi fitur sebagai artefak *network forensics*.

5. **Kurangi detail yang seharusnya masuk Bab 3/Bab 4.**  
   Di 2.7, cukup sebut model dievaluasi dengan metrik yang sesuai untuk data tidak seimbang. Daftar lengkap macro F1, MCC, balanced accuracy, recall, dan *confusion matrix* bisa muncul di Bab 3. Jangan terlalu sering mengulang daftar metrik di Bab 2.

## Cek Sitasi dan Tabel Penelitian Terdahulu

Tabel 2.1 **ada**, berisi **6 sumber**, dan kolomnya sesuai untuk naskah UAS: No, Penulis/Tahun, Fokus Penelitian, Metode/Dataset, Hasil Utama, Relevansi dengan Penelitian Ini.

Semua sumber pada tabel benar-benar ada di `references/literature-matrix.md`:

| Sumber di Tabel 2.1 | Status di literature matrix | Status di BibTeX |
|---|---|---|
| Koroniotis et al. (2019) | Ada, No. 1 | Ada |
| Jamalipour & Murali (2022) | Ada, No. 10 | Ada |
| Pakmehr et al. (2024) | Ada, No. 14 | Ada |
| Shukla et al. (2024) | Ada, No. 15 | Ada |
| Wu et al. (2021) | Ada, No. 17 | Ada |
| Kalakoti et al. (2022) | Ada, No. 7 | Ada |

UNSW Research (2021) dikutip di subbab BoT-IoT, ada di literature matrix No. 2 dan ada di `references.bib`. Ini aman.

Format sitasi di teks sudah mendekati APA sederhana. Perhatikan konsistensi: gunakan “Jamalipour & Murali (2022)” untuk naratif atau “(Jamalipour & Murali, 2022)” untuk parentetik. Draft sudah memakai bentuk naratif Indonesia “Jamalipour dan Murali (2022)”; ini masih dapat diterima, tetapi untuk gaya APA sederhana lebih konsisten memakai `&` pada sitasi parentetik dan “dan” pada narasi Indonesia.

## Cek Klaim Artifact dan Scope

1. **Tidak ada hasil eksperimen proyek yang ditulis sebagai hasil Bab 2.**  
   Bab 2 tidak memasukkan angka performa model, confusion matrix, distribusi kelas, atau hasil fitur penting. Ini benar; angka tersebut milik Bab 4.

2. **Klaim BoT-IoT aman.**  
   Draft menyebut BoT-IoT dari UNSW, memiliki trafik normal dan serangan, mencakup DoS/DDoS, tersedia dalam PCAP/Argus/CSV, dan relevan untuk *network forensic analytics*. Ini konsisten dengan Koroniotis et al. (2019), UNSW Research (2021), dan audit naskah.

3. **Klaim mirror dataset aman tetapi perlu tetap hati-hati.**  
   Kalimat “versi mirror digunakan sebagai working dataset” aman karena rujukan primer tetap artikel BoT-IoT dan halaman resmi UNSW. Jangan tambahkan klaim bahwa mirror tersebut “resmi”, “lengkap”, atau “identik” kecuali ada bukti artifact.

4. **Tidak ada klaim berbahaya.**  
   Draft tidak mengklaim sistem sebagai IDS produksi *real-time*, tidak mengklaim menyerang perangkat asli, dan tidak mengklaim melakukan *replay* PCAP aktual. Kalimat tentang SOC *replay* edukatif masih aman, tetapi untuk Bab 2 bisa dipadatkan menjadi “visualisasi edukatif berbasis hasil proyek”.

5. **Scope konsisten dengan Bab 1.**  
   Fokus normal vs DoS/DDoS, prototipe berbasis dataset, analisis fitur trafik, dan batasan forensik pada artefak jaringan selaras dengan Bab 1.

## Final Recommendation

**NEEDS REVISION, bukan reject.** Revisi yang harus dilakukan adalah pemadatan tajam, penambahan sitasi pada definisi teori, dan penguatan paragraf gap penelitian. Setelah tiga hal itu diperbaiki, Bab 2 berpotensi naik ke **APPROVED** karena struktur, cakupan, sitasi utama, dan keamanan klaim sudah berada di jalur yang benar.
