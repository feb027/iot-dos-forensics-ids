# Final Verification Phase 7 BAB 5

Tanggal verifikasi: Fri May 1 05:08:23 PM UTC 2026

Draft diverifikasi: `reports/manuscript-draft-bab5.md`

Review awal: `docs/REVIEW_phase7_bab5.md`

## Score

**94/100**

## Verdict

**APPROVED**

## Ringkasan Final

BAB 5 sudah memenuhi fungsi sebagai bab penutup. Kesimpulan menjawab rumusan masalah BAB 1 secara konsisten: prototipe sistem berhasil dirancang, proses audit dan *preprocessing* dataset dijelaskan, kinerja model dirangkum dengan angka utama yang benar, dan hasil interpretasi forensik serta *dashboard* dijelaskan tanpa memperluas klaim. Bagian saran juga realistis dan mengarah ke pekerjaan lanjutan yang sesuai dengan keterbatasan penelitian.

Tidak ada revisi wajib dari review awal. Draft sudah berada pada panjang yang sesuai, yaitu 792 kata, dan tidak memakai tabel/gambar yang tidak diperlukan. Angka yang muncul tetap sesuai artifact BAB 4 dan tidak ada klaim baru yang berisiko.

## Checklist Verifikasi

- Struktur `# 5. KESIMPULAN DAN SARAN`, `## 5.1 Kesimpulan`, dan `## 5.2 Saran` lengkap.
- Panjang naskah 792 kata, sesuai target 650–950 kata.
- Kesimpulan menjawab empat rumusan masalah BAB 1.
- Saran relevan dengan keterbatasan dataset, imbalance, validasi eksternal, multikelas, tuning, perluasan forensik, dashboard, dan kebutuhan arsitektur baru untuk IDS *real-time*.
- Tidak ada tabel atau gambar yang tidak perlu.
- Bahasa cukup natural dan aman untuk naskah akademik mahasiswa semester 6.

## Cek Angka Artifact

Lulus.

- Total data 3.668.522 baris sesuai BAB 4 dan artifact audit.
- Jumlah normal 370 pada data latih dan 107 pada data uji sesuai audit.
- Track A realistis LightGBM: *macro F1* 0,9885 dan MCC 0,9770 sesuai `results/metrics/advanced_summary.json`.
- *Confusion matrix* LightGBM Track A: TN=106, FP=1, FN=4, TP=715.417 sesuai artifact.
- Track B/C disebut sebagai subset terkontrol dan tidak dijadikan klaim dunia nyata.
- Fitur `N_IN_Conn_P_DstIP`, `N_IN_Conn_P_SrcIP`, `srate`, `drate`, statistik *flow*, `state_number`, dan `proto` sesuai pembahasan artifact forensik BAB 4.

## Cek Klaim dan Scope

Lulus.

- Draft menyatakan penelitian berbasis *dataset* BoT-IoT.
- Tidak ada klaim serangan terhadap perangkat IoT asli.
- Tidak ada klaim sistem siap produksi.
- Tidak ada klaim IDS *real-time*.
- Tidak ada klaim PCAP *replay* aktual.
- Tidak ada klaim model berlaku universal untuk semua jaringan IoT.
- *Feature importance* dan *SHAP* tidak ditulis sebagai penyebab kausal serangan.
- Saran penggunaan PCAP/Argus/log jaringan asli sudah dibatasi dengan aspek legal dan etis.

## Sisa Catatan Minor

Tidak ada catatan substansial. Saat dipindahkan ke Word, pastikan format poin bernomor pada bagian saran tetap rapi dan istilah teknis yang memakai italic di Markdown tetap terbaca miring.

## Final Recommendation

**APPROVED untuk finalisasi BAB 5.** Tidak ada critical issue atau major issue. BAB 5 aman untuk digabungkan ke naskah utama bersama BAB 1 sampai BAB 4.