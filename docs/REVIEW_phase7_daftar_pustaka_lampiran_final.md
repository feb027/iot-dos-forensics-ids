# Final Verification Phase 7 Daftar Pustaka dan Lampiran

Tanggal verifikasi: Sat May 2 06:36:19 AM UTC 2026

Draft diverifikasi:
- `reports/manuscript-daftar-pustaka.md`
- `reports/manuscript-lampiran.md`

Review awal:
- `docs/REVIEW_phase7_daftar_pustaka_lampiran.md`

## Score

**95/100**

## Verdict

**APPROVED**

## Ringkasan Final

Daftar pustaka dan lampiran sudah layak masuk naskah akhir. Daftar pustaka memuat sumber utama yang dikutip atau dirujuk pada BAB 1 sampai BAB 5, termasuk sumber BoT-IoT, IDS IoT berbasis *machine learning*, DoS/DDoS pada IoT, *network forensics*, *feature selection*, dan RT-IoT2022 sebagai dataset alternatif. Setelah review Codex, catatan minor tentang tanggal akses web dan konsistensi tahun RT-IoT2022 sudah diterapkan.

Lampiran sudah menunjuk artefak yang benar-benar ada di repo dan tidak menyertakan raw dataset, kredensial, PCAP besar, atau model besar. Lampiran juga menjaga batasan klaim: dashboard/SOC *replay* adalah visualisasi edukatif, bukan IDS produksi *real-time*, bukan PCAP *replay* aktual, dan bukan sistem operasional.

## Checklist Verifikasi

- Daftar pustaka memiliki heading `# DAFTAR PUSTAKA`.
- Lampiran memiliki heading `# LAMPIRAN`.
- Lampiran A sampai Lampiran H lengkap.
- Review Codex tersedia dan berstatus **94/100 APPROVED**.
- Tidak ada critical issue atau major issue dari review Codex.
- Catatan akses untuk UNSW Research dan RT-IoT2022 sudah ditambahkan.
- Tahun dataset RT-IoT2022 sudah diseragamkan dengan `references/references.bib`, yaitu 2023.

## Cek Daftar Pustaka

Lulus.

Sumber utama yang tercakup:

- Koroniotis et al. (2019) untuk BoT-IoT.
- UNSW Research (2021) untuk halaman resmi BoT-IoT.
- Jamalipour & Murali (2022) untuk taksonomi IDS IoT.
- Jayalaxmi et al. (2022) untuk survey IDS/IPS IoT.
- Pakmehr et al. (2024) untuk survey deteksi DDoS IoT.
- Shukla et al. (2024) untuk review deteksi DDoS berbasis trafik IoT.
- Wu et al. (2021) untuk analisis trafik IoT dalam konteks forensik.
- Koroniotis et al. (2020) untuk kerangka *network forensic* IoT.
- Kalakoti et al. (2022) untuk *feature selection* pada deteksi botnet IoT.
- Sharmila & Nagapadma (2023) untuk RT-IoT2022 dan referensi penelitian lanjutan.

## Cek Lampiran

Lulus.

Lampiran menunjuk artefak utama berikut:

- `results/metrics/`
- `results/tables/`
- `results/figures/`
- `dashboard/data/`
- `dashboard/demo.html`
- dokumen review BAB 1 sampai BAB 5 di `docs/`

Path yang disebut dalam lampiran sudah dicek secara lokal dan tersedia di repo. Lampiran juga memberi catatan bahwa screenshot dashboard final perlu diambil saat penyusunan Word jika Gambar 4.4 akan dimasukkan sebagai gambar.

## Cek Klaim dan Scope

Lulus.

- Tidak ada klaim IDS produksi *real-time*.
- Tidak ada klaim PCAP *replay* aktual.
- Tidak ada klaim dashboard sebagai sistem operasional.
- Tidak ada klaim fitur penting sebagai penyebab kausal serangan.
- Tidak ada lampiran raw dataset, kredensial, atau artefak besar yang tidak sesuai untuk naskah.

## Final Recommendation

**APPROVED untuk finalisasi Daftar Pustaka dan Lampiran.** Bagian ini aman untuk digabungkan setelah BAB 5 dalam dokumen Word. Jika halaman naskah melebihi batas 15 halaman, Lampiran H dapat diringkas atau tidak dimasukkan penuh, karena fungsinya lebih sebagai jejak proses internal repo.