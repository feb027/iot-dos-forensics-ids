# Review Final Phase 7 Bab 2

Tanggal verifikasi: Fri May 1 02:17:29 PM UTC 2026

Draft diverifikasi: `reports/manuscript-draft-bab2.md`  
Review sebelumnya: `docs/REVIEW_phase7_bab2.md`

## Score Final

**94/100**

## Verdict

**APPROVED**

Bab 2 sudah memenuhi gate final: skor >= 90, tidak ada critical issue, dan tidak ada major blocker yang tersisa. Revisi dari review sebelumnya cukup untuk naskah UAS IoT.

## Checklist Perbaikan

| No | Item Verifikasi | Status | Catatan |
|---:|---|---|---|
| 1 | Bab 2 dipadatkan ke sekitar 1.100-1.300 kata | PASS | `wc -w` menunjukkan 1.242 kata untuk `reports/manuscript-draft-bab2.md`. Target pemadatan terpenuhi. |
| 2 | Struktur 2.1-2.7 tetap lengkap | PASS | Semua subbab 2.1 sampai 2.7 ada dan urut. |
| 3 | Tabel 2.1 tetap ada, 6 sumber, kolom sesuai, sumber ada di literature matrix | PASS | Tabel 2.1 ada, berisi 6 sumber, dengan kolom: No, Penulis/Tahun, Fokus Penelitian, Metode/Dataset, Hasil Utama, Relevansi dengan Penelitian Ini. Keenam sumber ada di `references/literature-matrix.md`. |
| 4 | Definisi teori utama memiliki sitasi memadai | PASS | IoT, DoS/DDoS, IDS ML, network forensics, dan BoT-IoT sudah ditopang sitasi yang relevan. |
| 5 | Klaim *chain of custody* dibatasi | PASS | Draft membatasi klaim sebagai keterlacakan penelitian berbasis dataset, bukan prosedur *chain of custody* forensik legal penuh. |
| 6 | Gap penelitian setelah Tabel 2.1 tajam | PASS | Gap sudah jelas: bukan sekadar performa model, tetapi alur audit dataset, skenario normal vs DoS/DDoS, metrik data tidak seimbang, dan interpretasi fitur sebagai artefak *network forensics*. |
| 7 | Bagian 2.7 tidak terlalu operasional | PASS | 2.7 masih menyebut alur penelitian, tetapi sudah ringkas dan layak sebagai kerangka pemikiran. |
| 8 | Tidak ada hasil eksperimen proyek di Bab 2 | PASS | Tidak ada angka performa model, distribusi kelas proyek, hasil fitur penting, atau klaim hasil eksperimen. |
| 9 | Tidak ada klaim berbahaya | PASS | Draft tidak mengklaim IDS produksi *real-time*, tidak mengklaim menyerang perangkat asli, dan tidak mengklaim PCAP *replay* aktual. |
| 10 | Bahasa dan format layak untuk Word copy-paste | PASS | Bahasa Indonesia akademik cukup natural, format heading dan tabel Markdown mudah dipindahkan ke Word. |

## Sisa Catatan

Tidak ada blocker. Catatan kecil: daftar metrik pada 2.3 masih cukup spesifik, tetapi masih dapat diterima karena digunakan untuk menjelaskan kehati-hatian evaluasi IDS, bukan memaparkan hasil eksperimen. Saat dipindahkan ke Word, pastikan Tabel 2.1 tidak terpotong dan tetap diberi label `Tabel 2.1`.

## Final Recommendation

**APPROVED untuk lanjut ke tahap berikutnya.** Bab 2 sudah cukup padat, lengkap, aman secara klaim akademik, dan selaras dengan batasan proyek berbasis dataset BoT-IoT.
