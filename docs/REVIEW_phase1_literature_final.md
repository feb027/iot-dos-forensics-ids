# Final Verification Review — Fase 1 Literature Review

Tanggal review: 2026-04-28T16:10:00+00:00

Peran reviewer: Dosen mata kuliah IoT Semester 6

## Verdict Final

**Score: 84/100**

**Verdict: NEEDS REVISION**

Fase 1 sudah jauh lebih kuat dibanding review pertama: jumlah referensi memadai, sumber *network forensics* sudah berdiri sendiri, dan arah Fase 2 untuk audit dataset sudah operasional. Namun, satu revisi wajib belum terpenuhi sepenuhnya: entry BibTeX TON_IoT masih memakai `\textunderscore`, sehingga masalah format yang diminta untuk diperbaiki belum benar-benar selesai. Karena ini termasuk revisi wajib dari review pertama, Fase 1 belum dapat diberi verdict final `APPROVED`.

## Validasi Wajib

| Pemeriksaan | Hasil | Catatan |
|---|---:|---|
| `git status -sb` | Terverifikasi | Branch `phase-1-literature-review`; ada perubahan/untracked artefak Fase 1 yang belum dikomit. |
| Jumlah sumber matrix | 18 | Dihitung dari baris sumber pada `references/literature-matrix.md`. |
| Jumlah entry BibTeX | 18 | Dihitung dari entry `@...` pada `references/references.bib`. |
| Cek `textunderscore` rusak | Gagal | `references/references.bib` masih memuat `title = {{TON\textunderscore IoT} ...}`. |
| Sumber *network forensics* berdiri sendiri | Lulus | Ada Wu et al. 2021 dan Koroniotis et al. 2020 sebagai sumber metodologis/kerangka forensik jaringan. |
| Arah checklist audit dataset Fase 2 | Lulus | `docs/research-log.md` dan `reports/progress-1-literature-review.md` sudah memuat audit label, fitur, duplikasi, split, distribusi kelas, subset, dan leakage. |
| `python3 -m py_compile scripts/*.py` | Lulus | Tidak ada error kompilasi. |
| `python3 -m pytest -q` | Lulus | 3 tests passed. |

## Revisi Wajib yang Dicek

1. **Perbaiki format BibTeX TON_IoT**
   - Status: **belum terpenuhi**.
   - Bukti: entry `alsaedi2020toniot` pada `references/references.bib` masih memakai `\textunderscore`.
   - Perbaikan actionable: ganti judul menjadi format BibTeX yang aman, misalnya:

```bibtex
title = {{TON\_IoT} Telemetry Dataset: A New Generation Dataset of {IoT} and {IIoT} for Data-Driven Intrusion Detection Systems},
```

2. **Tambahkan minimal satu sumber metodologis *network forensics* / *network traffic forensic analysis***
   - Status: **terpenuhi**.
   - Bukti: `references/literature-matrix.md` memuat Wu et al. 2021 tentang analisis trafik IoT untuk investigator forensik dan Koroniotis et al. 2020 tentang kerangka *network forensic* IoT.

3. **Pastikan Fase 2 memiliki arah checklist audit dataset operasional**
   - Status: **terpenuhi**.
   - Bukti: catatan Fase 2 sudah menyebut larangan memasukkan kolom label ke fitur, pengecekan duplikasi flow/baris, risiko split random, distribusi kelas, pemilihan subset, imbalance, dan leakage.

## Catatan Reviewer

Secara substansi akademik, Fase 1 sudah layak untuk mendukung BAB II dan transisi ke audit dataset. Literatur tidak hanya berisi IDS umum, tetapi sudah mencakup dataset utama, dataset alternatif, DoS/DDoS, risiko evaluasi, dan *network forensics*. Klaim kuantitatif juga belum dipaksakan di luar artefak yang tersedia.

Masalah yang tersisa bersifat teknis tetapi wajib: BibTeX harus bersih sebelum fase ini ditutup. Setelah entry TON_IoT diperbaiki dan validasi singkat diulang, fase ini dapat naik ke `APPROVED` tanpa perlu perubahan substansi besar.

## Actionable Revision

- Ubah hanya entry `alsaedi2020toniot` di `references/references.bib` agar tidak lagi memakai `\textunderscore`; gunakan `TON\_IoT` atau bentuk aman lain yang konsisten dengan BibTeX/LaTeX.
- Jalankan ulang:

```bash
rg -n "textunderscore" references/references.bib
python3 -m py_compile scripts/*.py
python3 -m pytest -q
```

- Jika `rg` tidak menemukan `textunderscore` dan dua command validasi tetap lulus, Fase 1 dapat disetujui.
