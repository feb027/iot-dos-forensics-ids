# Codex Review Phase 7 BAB 5

Tanggal review: Sat May 2 06:29:57 AM UTC 2026

Draft direview: `reports/manuscript-draft-bab5.md`

## Score

**95/100**

## Verdict

**APPROVED**

## Ringkasan Keputusan

BAB 5 sudah layak masuk finalisasi naskah UAS. Struktur wajib terpenuhi, panjang aman sekitar 792 kata, kesimpulan menjawab empat rumusan masalah BAB 1, dan batasan scope ditulis dengan cukup tegas. Draft tidak jatuh ke klaim berlebihan seperti IDS produksi *real-time*, deteksi universal DoS/DDoS IoT, serangan terhadap perangkat asli, atau PCAP *replay* aktual.

Angka kunci yang digunakan konsisten dengan artifact: total data 3.668.522 baris, normal 370 train dan 107 test, LightGBM Track A realistis dengan *macro F1* 0,9885, MCC 0,9770, TN=106, FP=1, FN=4, TP=715.417, serta pembatasan Track B/C sebagai subset terkontrol. Bagian saran juga realistis dan tidak menjanjikan pengembangan yang belum dibuktikan.

## Critical Issues

Tidak ada critical issue.

## Major Issues

Tidak ada major issue.

## Minor Issues

1. Kesimpulan sudah kuat, tetapi urutan enam poin agak lebih panjang daripada kebutuhan BAB 5. Ini masih dapat diterima karena tetap dalam rentang kata aman dan tidak melebar dari rumusan masalah.
2. Kalimat "model mampu membedakan trafik normal dan DoS/DDoS pada skenario yang digunakan" sudah aman, tetapi harus dipertahankan bersama pembatas setelahnya. Jangan dipotong saat masuk Word karena tanpa pembatas kalimat ini bisa terbaca terlalu luas.
3. Bagian saran nomor 6 menyebut screenshot final dan lampiran artifact. Ini baik, tetapi jika screenshot belum tersedia di repo, jangan ditulis sebagai hasil yang sudah dilakukan.

## Cek Kesesuaian dengan Rumusan Masalah BAB 1

- RM1: Terjawab. Draft menyatakan prototipe berbasis BoT-IoT mencakup audit data, *preprocessing*, skenario pengujian, pemodelan, evaluasi, interpretasi artefak forensik, *dashboard*, dan SOC *replay* edukatif. Scope sebagai prototipe akademik juga jelas.
- RM2: Terjawab. Draft mencatat total data 3.668.522 baris, fokus normal vs DoS/DDoS, normal 370 train dan 107 test, serta penggunaan Track A/B/C untuk membaca distribusi realistis dan subset terkontrol.
- RM3: Terjawab. Draft menonjolkan LightGBM Track A realistis sebagai hasil utama dengan *macro F1* 0,9885, MCC 0,9770, TN=106, FP=1, FN=4, TP=715.417, serta membatasi Random Forest sempurna pada Track B/C sebagai hasil subset terkontrol.
- RM4: Terjawab. Draft menyebut fitur forensik utama, perbedaan *native feature importance* dan SHAP, serta *dashboard*/SOC *replay* edukatif sebagai visualisasi artifact, bukan sistem operasional atau PCAP *replay* aktual.

## Cek Angka dan Artifact

Lulus.

- Total data 3.668.522 baris sesuai `results/metrics/preprocessing_summary.json`.
- Normal 370 train dan 107 test sesuai artifact preprocessing dan track modeling.
- Track A realistis LightGBM sesuai `results/metrics/advanced_summary.json`: *macro F1* 0,9885, MCC 0,9770, TN=106, FP=1, FN=4, TP=715.417.
- Track B/C disebut sebagai subset terkontrol. Draft tidak mengklaim nilai sempurna Random Forest pada B/C sebagai generalisasi dunia nyata.
- Fitur forensik yang disebut aman: `N_IN_Conn_P_DstIP`, `N_IN_Conn_P_SrcIP`, `srate`, `drate`, statistik *flow*, `state_number`, dan `proto`.
- Interpretasi *native feature importance* dan SHAP dibatasi sebagai sudut interpretasi berbeda, bukan bukti kausal universal.

## Cek Klaim dan Scope

Lulus.

- Tidak ada klaim bahwa model mendeteksi semua DoS/DDoS IoT secara universal.
- Tidak ada klaim sistem siap produksi atau IDS *real-time*.
- Tidak ada klaim serangan dilakukan terhadap perangkat IoT asli.
- Tidak ada klaim PCAP *replay* aktual.
- Tidak ada klaim fitur penting sebagai penyebab kausal serangan.
- *Dashboard* dan SOC *replay* disebut sebagai visualisasi edukatif berbasis artifact, sesuai batasan BAB 1 dan BAB 4.

## Cek Format, Bahasa, dan Word Readiness

Lulus.

- Struktur wajib terpenuhi: `# 5. KESIMPULAN DAN SARAN`, `## 5.1 Kesimpulan`, dan `## 5.2 Saran`.
- Panjang aman untuk BAB 5, sekitar 792 kata, masih dalam target 650-950 kata.
- Bahasa Indonesia akademik cukup natural untuk level semester 6.
- Format angka Indonesia konsisten: koma desimal dan titik pemisah ribuan.
- Istilah asing penting seperti *dataset*, *preprocessing*, *machine learning*, *dashboard*, *replay*, *real-time*, *artifact*, *feature importance*, dan *flow* sudah cukup rapi.

## Rekomendasi Revisi Konkret

Tidak ada revisi wajib sebelum finalisasi. Revisi berikut bersifat opsional untuk merapikan Word:

1. Bagian 5.1, paragraf ketiga:
   - Pertahankan kalimat pembatas "hasil tersebut hanya berlaku pada *dataset* dan skenario eksperimen yang digunakan".
   - Alasan akademik: kalimat ini mencegah pembaca menafsirkan performa Track A sebagai generalisasi universal.

2. Bagian 5.2, saran nomor 6:
   - Jika screenshot final belum tersedia sebagai artifact, gunakan frasa "dapat menambahkan screenshot final" dan jangan mengubahnya menjadi klaim "telah menambahkan screenshot final".
   - Alasan akademik: menjaga konsistensi antara saran pengembangan dan artifact yang benar-benar ada di repo.

3. Bagian 5.1, paragraf kelima:
   - Jika ingin lebih ringkas, kalimat "Interpretasi tersebut tetap dibatasi sebagai bukti berbasis *artifact* trafik, bukan bukti kausal universal" sudah cukup dan tidak perlu ditambah klaim sebab-akibat baru.
   - Alasan akademik: fitur penting hanya menunjukkan kontribusi model pada data, bukan penyebab serangan.

## Final Recommendation

**APPROVED untuk finalisasi BAB 5.** Draft memenuhi gate approval karena score >= 90, tidak memiliki critical/major issue, struktur lengkap, angka sesuai artifact, rumusan masalah terjawab, dan scope klaim aman untuk naskah UAS IoT + Cyber Security + Digital Forensics.
