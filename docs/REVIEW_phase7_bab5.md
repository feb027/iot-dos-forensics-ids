# Review Phase 7 BAB 5 — Lecturer Reviewer

Tanggal review: Fri May 1 05:08:23 PM UTC 2026

Draft direview: `reports/manuscript-draft-bab5.md`

## Score

**92/100**

## Verdict

**APPROVED**

## Ringkasan Keputusan

BAB 5 sudah layak sebagai bab penutup naskah UAS. Struktur sudah tepat dengan dua subbab utama, yaitu kesimpulan dan saran. Panjang naskah 792 kata, masih berada dalam target 650–950 kata. Isi kesimpulan menjawab empat rumusan masalah BAB 1: rancangan prototipe, proses *preprocessing* dan pembentukan skenario, hasil kinerja model, serta interpretasi artefak dan visualisasi melalui *dashboard*.

Secara substansi, BAB 5 tidak menambah klaim baru di luar BAB 4. Angka yang dipakai masih sesuai artifact, terutama total data 3.668.522 baris, kelas normal 370 data latih dan 107 data uji, serta hasil utama LightGBM Track A dengan *macro F1* 0,9885 dan MCC 0,9770. Batasan penelitian juga tetap aman: tidak ada klaim serangan terhadap perangkat IoT asli, tidak ada klaim IDS produksi *real-time*, tidak ada klaim PCAP *replay* aktual, dan tidak ada generalisasi universal.

## Temuan Critical

Tidak ada temuan critical.

Draft tidak melanggar batasan keamanan akademik. Tidak ditemukan klaim bahwa sistem menyerang perangkat asli, siap produksi, atau melakukan PCAP *replay* aktual.

## Temuan Major

Tidak ada major blocker.

BAB 5 sudah cukup kuat untuk menutup naskah. Kesimpulan dan saran konsisten dengan BAB 1–4 dan tidak mengubah ruang lingkup penelitian.

## Temuan Minor

1. Kesimpulan cukup panjang dengan enam poin naratif. Ini masih dapat diterima, tetapi saat dipindahkan ke Word bisa dibuat sedikit lebih padat bila halaman terlalu panjang.
2. Beberapa istilah seperti Track A/B/C, LightGBM, Random Forest, dan Decision Tree tidak dimiringkan. Ini wajar karena dipakai sebagai nama skenario/model.
3. Saran sudah realistis, tetapi jika dosen meminta implementasi lanjutan yang lebih konkret, bagian saran nomor 7 dapat dijadikan dasar untuk menjelaskan bahwa IDS *real-time* membutuhkan arsitektur baru.

## Cek Angka Artifact

Lulus.

- Total data 3.668.522 baris sesuai artifact BAB 4 dan `preprocessing_summary.json`.
- Kelas normal 370 data latih dan 107 data uji sesuai audit dataset.
- Hasil utama Track A realistis LightGBM: *macro F1* 0,9885 dan MCC 0,9770 sesuai `advanced_summary.json`.
- *Confusion matrix* LightGBM Track A: TN=106, FP=1, FN=4, TP=715.417 sesuai artifact.
- Track B/C disebut sebagai subset terkontrol dan tidak dijadikan klaim dunia nyata.
- Fitur forensik yang disebut, seperti `N_IN_Conn_P_DstIP`, `N_IN_Conn_P_SrcIP`, `srate`, `drate`, statistik *flow*, `state_number`, dan `proto`, sesuai pembahasan BAB 4.

## Cek Klaim dan Scope

Lulus.

- Penelitian disebut sebagai *prototype* berbasis *dataset*, bukan hardware IoT.
- Tidak ada klaim IDS produksi *real-time*.
- Tidak ada klaim PCAP *replay* aktual.
- Tidak ada klaim model mendeteksi semua DoS/DDoS IoT secara universal.
- *Feature importance* dan *SHAP* dijelaskan sebagai interpretasi yang saling melengkapi, bukan bukti kausal.
- Saran tentang PCAP/Argus/log jaringan asli dibatasi dengan syarat legal dan etis.

## Cek Format dan Word Readiness

Lulus.

- Heading `# 5. KESIMPULAN DAN SARAN`, `## 5.1 Kesimpulan`, dan `## 5.2 Saran` lengkap.
- Tidak ada tabel atau gambar yang tidak perlu.
- Angka desimal menggunakan koma Indonesia.
- Bahasa cukup natural untuk mahasiswa semester 6 dan tidak terlalu berlebihan.
- Format poin pada saran mudah dipindahkan ke Word.

## Final Recommendation

**APPROVED untuk finalisasi BAB 5.** Tidak ada revisi wajib. Jika ingin dipoles saat layout Word, cukup rapikan spasi dan pastikan istilah teknis yang ingin dimiringkan tetap konsisten setelah copy-paste.