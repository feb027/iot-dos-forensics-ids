# Results Directory

Folder ini menyimpan artifact yang boleh di-commit untuk mendukung laporan dan dashboard.

## Struktur

- `tables/` — CSV ringkasan, class distribution, model comparison, feature importance.
- `figures/` — grafik EDA, confusion matrix, model comparison, feature importance.
- `metrics/` — JSON metrik model dan metadata eksperimen.
- `models/` — model binary besar, di-ignore oleh Git kecuali `.gitkeep`.

## Aturan

- Jangan commit model besar (`.pkl`, `.joblib`, `.pt`, dll.).
- Commit tabel/grafik/metrik yang dipakai di laporan.
- Setiap angka di naskah ilmiah harus dapat dilacak ke artifact di folder ini atau sumber referensi.
