# Fase 7 Manuscript Plan

## Tujuan

Menulis naskah ilmiah final untuk UAS IoT berdasarkan artifact yang sudah tersedia di repo, tanpa mengarang angka, sitasi, atau klaim.

## Scope Naskah

Judul utama:

**Sistem Analisis Serangan DoS pada Trafik IoT Berbasis Machine Learning dan Network Forensics Menggunakan Dataset BoT-IoT**

Struktur target:

1. Abstrak
2. Pendahuluan
3. Tinjauan Pustaka
4. Metodologi
5. Hasil dan Pembahasan
6. Analisis Forensik
7. Kesimpulan dan Saran
8. Daftar Pustaka

## Artifact Sources

Gunakan hanya data dari:

- `references/literature-matrix.md`
- `references/references.bib`
- `results/metrics/*.json`
- `results/tables/*.csv`
- `results/figures/*.png`
- `reports/progress-*.md`
- `dashboard/data/dashboard-data.json`

## Claim Rules

- Jangan menjadikan accuracy sebagai klaim utama.
- Jelaskan normal class sangat kecil sebagai batasan metodologi.
- Pisahkan Track A realistic dari Track B/C controlled subset.
- Gunakan Track B/C sebagai eksperimen sensitivitas/kontrol, bukan bukti generalisasi dunia nyata.
- SHAP dan feature importance ditulis sebagai evidence pendukung berbasis dataset, bukan bukti kausal.
- Semua angka harus bisa dilacak ke artifact repo.

## Deliverables

- Draft naskah utama di `reports/manuscript-draft.md`.
- Tabel/daftar gambar yang mengacu ke `results/tables/` dan `results/figures/`.
- Review Codex lecturer/technical untuk naskah.
- Final revision setelah review.

## Validation

Sebelum review Fase 7:

```bash
python3 scripts/generate_dashboard_data.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null
```

Tambahan manual:

- Cek semua angka naskah punya sumber artifact.
- Cek semua sitasi ada di `references/references.bib`.
- Cek bahasa natural Indonesia akademik, tidak terlalu AI-polished.
