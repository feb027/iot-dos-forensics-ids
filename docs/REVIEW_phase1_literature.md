# Review Fase 1 Literature Review

Tanggal review: 2026-04-28T15:53:52+00:00

Reviewer: Dosen IoT Semester 6, fokus IoT Security, IDS, DoS/DDoS, Digital Forensics, dan reproducible ML research.

## Verdict

Skor: **88/100**

Verdict: **APPROVED**

Fase 1 sudah layak menjadi fondasi awal naskah ilmiah dan sudah cukup untuk masuk ke Fase 2 Dataset Audit. Syarat minimal jumlah referensi terpenuhi, cakupan topik inti sudah ada, dan dokumen tidak mengarang hasil eksperimen proyek. Namun, ada beberapa revisi wajib minor yang perlu dibereskan sebelum artefak Fase 1 dianggap rapi untuk dikutip di naskah akhir.

## Validasi yang Dilakukan

- `git status -sb`: branch aktif `phase-1-literature-review`; terdapat perubahan Fase 1 yang belum di-commit pada `docs/project-control.md`, `docs/research-log.md`, `references/literature-matrix.md`, `references/references.bib`, serta artefak baru `references/raw-*` dan `reports/progress-1-literature-review.md`.
- Jumlah sumber di `references/literature-matrix.md`: **16**.
- Jumlah entry BibTeX di `references/references.bib`: **16**.
- Target minimal 10-15 referensi: **terpenuhi**.
- Raw evidence: **28 file** pada `references/raw-search/`, `references/raw-sources/`, dan `references/raw-metadata/`; tidak ditemukan file kosong.
- `python3 -m py_compile scripts/*.py`: **pass**.
- `python3 -m pytest -q`: **pass, 3 passed in 0.27s**.

## Penilaian Granular

| Aspek | Skor | Catatan |
|---|---:|---|
| Kecukupan jumlah dan jenis sumber | 18/20 | Matrix berisi 16 sumber: dataset, paper eksperimen, survey, dan metodologi evaluasi. Ini sudah melewati target Fase 1. |
| Cakupan topik wajib | 24/30 | BoT-IoT/RT-IoT2022, IoT IDS, DoS/DDoS ML, dan leakage sudah jelas. Network forensics ada, tetapi masih tipis dan lebih banyak diturunkan dari BoT-IoT serta feature importance. |
| Kualitas sintesis dan gap riset | 17/20 | Gap yang dipilih realistis: pipeline auditable, audit dataset, baseline ML, leakage, dan interpretasi forensik. Ini cocok untuk proyek UAS individu. |
| Reproducibility dan audit trail | 14/15 | Research log, raw search, raw source, dan raw metadata tersedia. Fase 2 sudah diarahkan ke audit label, duplikasi, split, dan leakage. |
| Validitas sitasi/DOI | 8/10 | DOI mayoritas valid via Crossref. DOI UCI `10.24432/C5P338` tidak ada di Crossref, tetapi resolver `doi.org` mengarah benar ke halaman UCI, jadi tidak dicurigai palsu. Ada satu masalah format BibTeX pada entri TON_IoT. |
| Kesiapan dokumentasi fase | 7/5 | `progress-1`, `research-log`, `project-control`, `phase-gates`, dan `dataset-notes` saling konsisten untuk fase review. Nilai ekstra karena risiko Fase 2 sudah ditulis eksplisit. |

Total normalisasi: **88/100**.

## Cakupan Kelompok Referensi

- Dataset BoT-IoT/RT-IoT2022: **terpenuhi** melalui Koroniotis et al., UNSW BoT-IoT, UCI RT-IoT2022, dan QAE RT-IoT2022.
- IoT IDS: **terpenuhi** melalui paper BoT-IoT IDS dan beberapa survey IoT IDS.
- DoS/DDoS ML detection: **terpenuhi** melalui lightweight DDoS ML dan dua survey DDoS IoT.
- Leakage/evaluation methodology: **terpenuhi minimal** melalui Bouke & Abdullah serta catatan risiko split/duplikasi/label-like features.
- Network forensics: **terpenuhi sebagian**. Tema forensik muncul dari paper BoT-IoT dan rencana interpretasi fitur, tetapi belum ada referensi metodologis forensik jaringan yang berdiri sendiri.

## Temuan Utama

1. **BibTeX entri TON_IoT perlu diperbaiki.**  
   Pada `references/references.bib:32`, judul terbaca sebagai `TON	extunderscore IoT`, yang menunjukkan escape underscore bermasalah. Ini bukan masalah metodologi, tetapi wajib diperbaiki agar sitasi tidak rusak saat dipakai di naskah atau citation processor.

2. **Network forensics masih kurang kuat sebagai klaster teori.**  
   `references/literature-matrix.md:7`, `references/literature-matrix.md:13`, dan `reports/progress-1-literature-review.md:32-34` sudah mengarah ke forensik jaringan, tetapi belum ada sumber yang secara khusus membahas metodologi network forensics untuk trafik, flow, log, atau artefak investigasi. Untuk judul yang membawa "Digital Forensics", satu referensi metodologis tambahan akan membuat fondasi BAB II lebih defensible.

3. **Leakage sudah dicatat, tetapi Fase 2 perlu mengubahnya menjadi checklist operasional.**  
   `docs/dataset-notes.md` sudah menyebut duplikasi, split temporal/random, fitur label-like, IP/port memorization, dan imbalance. Pada Fase 2, poin ini harus berubah menjadi output audit yang eksplisit, bukan hanya catatan risiko.

4. **Tidak ditemukan klaim hasil eksperimen proyek yang belum ada.**  
   Dokumen konsisten menyatakan Fase 1 bukan eksperimen. Klaim kuantitatif yang muncul terkait RT-IoT2022 bersumber dari halaman UCI dan tidak dipakai sebagai hasil proyek.

## Revisi Wajib

- Perbaiki format BibTeX TON_IoT pada `references/references.bib:32`, misalnya gunakan `TON_IoT`, `{TON\_IoT}`, atau format lain yang valid sesuai citation tool yang akan dipakai.
- Tambahkan minimal satu sumber metodologis tentang *network forensics* atau *network traffic forensic analysis* agar aspek Digital Forensics tidak hanya bergantung pada paper BoT-IoT dan interpretasi feature importance.
- Pada awal Fase 2, buat checklist audit dataset yang menghasilkan artefak konkret: label mapping, daftar fitur yang dikeluarkan, duplikasi, class distribution, missing values, dan strategi split.

## Revisi Sebaiknya

- Di `literature-matrix`, pisahkan lebih jelas antara "paper dataset", "paper eksperimen", "survey", dan "paper metodologi", karena saat ini beberapa klaster bercampur antara fungsi teori dan fungsi pembanding.
- Tambahkan catatan singkat untuk sumber eksperimen BoT-IoT tentang apakah evaluasinya memakai random split, cross-validation, atau skenario lain jika informasi tersedia dari paper.
- Pastikan `docs/phase-gates.md` dicentang hanya setelah review ini ditindaklanjuti dan artefak Fase 1 final sudah siap commit.

## Revisi Opsional

- Tambahkan satu kolom atau catatan "akan dipakai di bagian naskah mana" untuk memudahkan Paper Writer menyusun BAB Pendahuluan, Tinjauan Pustaka, Metodologi, dan Diskusi.
- Tambahkan sumber pembanding lama/klasik tentang IDS evaluation pitfalls jika nanti ingin memperkuat argumen leakage dan evaluation bias.
- Rapikan konsistensi istilah `DoS/DDoS`, `DDoS`, `network forensics`, dan `forensik jaringan` agar naskah akhir tidak terasa campur aduk.

## Keputusan Lanjut Fase

Fase 1 **boleh lanjut ke Fase 2 Dataset Audit** karena tidak ada isu kritis, tidak ada fabrikasi hasil eksperimen, dan cakupan referensi sudah memenuhi standar minimum. Revisi wajib di atas bersifat minor tetapi tetap perlu dikerjakan sebelum Fase 1 ditutup permanen dan sebelum referensi dipakai dalam naskah ilmiah akhir.
