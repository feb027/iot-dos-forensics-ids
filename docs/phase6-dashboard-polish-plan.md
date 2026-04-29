# Fase 6 Dashboard Polish Plan

Tanggal: 2026-04-29

## Tujuan

Memoles dashboard static GitHub Pages setelah Fase 6A Advanced/SOTA Modeling merge agar pembaca melihat alur bukti dari dataset audit, EDA, baseline, forensic analysis, sampai advanced/SOTA modeling tanpa overclaim.

## Scope

1. Verifikasi GitHub Pages dan `dashboard/data/dashboard-data.json` dari `main`.
2. Pastikan semua angka dashboard berasal dari artifact committed, bukan hardcoded manual.
3. Tampilkan highlight Track A realistis secara jelas karena itu skenario paling relevan dibanding controlled subset.
4. Jelaskan bahwa best overall Track C controlled tidak boleh dianggap bukti generalisasi dunia nyata.
5. Bedakan global aggregated SHAP dari Track A-specific SHAP saat nanti masuk manuscript.
6. Review visual dashboard: readability, layout, label metrik, dan catatan limitation.

## Deliverables

- Dashboard data regenerated from `scripts/generate_dashboard_data.py`.
- Dashboard GitHub Pages verified HTTP 200.
- Optional dashboard polish commit if visual/copy issues ditemukan.
- Dashboard reviewer file, e.g. `docs/REVIEW_phase6_dashboard.md`.

## Validation Commands

```bash
python3 scripts/generate_dashboard_data.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null
node --check dashboard/app.js
```

## Claim Rules

- Klaim utama Fase 6A: LightGBM Track A meningkatkan macro F1 dibanding baseline Track A.
- Best overall XGBoost Track C boleh ditampilkan sebagai controlled-subset result, bukan klaim generalisasi utama.
- Normal class kecil dan split-similarity risk harus tetap terlihat sebagai limitation.
- SHAP global adalah agregat lintas run; jangan ditulis seolah-olah identik untuk semua track/model.
