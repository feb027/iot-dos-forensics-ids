# Dashboard Specification

## Tujuan

Dashboard berfungsi sebagai *visual evidence viewer* untuk hasil analisis serangan DoS/DDoS pada trafik IoT. Fokusnya bukan sekadar menampilkan skor model, tetapi memperlihatkan alur bukti dari audit dataset, distribusi kelas, baseline, advanced modeling, confusion matrix, dan interpretasi forensik fitur.

## Teknologi

- Static HTML/CSS/JS tanpa build tool.
- Data utama dari `dashboard/data/dashboard-data.json`.
- JSON dihasilkan oleh `scripts/generate_dashboard_data.py` dari artifact committed di `results/tables/` dan `results/metrics/`.
- Target deployment: GitHub Pages.
- Chart.js dan Lucide boleh dipakai via CDN, tetapi dashboard wajib tetap punya fallback statis/mobile jika CDN gagal atau chart terlalu padat.

## Sections

1. Project Overview / command center hero.
2. Dataset Summary dan audit scope.
3. Attack/Class Distribution.
4. Baseline vs Advanced Model Performance.
5. Confusion Matrix dan FP/FN interpretation.
6. Feature Evidence / SHAP.
7. Advanced/SOTA Track A realistic highlight.
8. Artifact, limitation, dan claim policy.
9. Footer/link artifact.

## Design Direction

- Fase 6 memakai dark SOC/cybersecurity command-center style yang sudah disetujui user.
- Desain tetap harus akademik, readable, dan tidak terlalu dekoratif sampai mengganggu klaim ilmiah.
- Gunakan kontras tinggi, kartu terstruktur, heading jelas, dan mobile fallback bars untuk chart padat.
- Dark theme tidak boleh menjadi alasan overclaim; limitation dan claim policy harus tetap terlihat.
- Jika arah visual berubah lagi, `docs/phase6-dashboard-design-brief.md` menjadi referensi desain Fase 6 yang lebih spesifik.

## Data Contract

`dashboard/data/dashboard-data.json` harus minimal memuat struktur berikut ketika artifact fase terkait tersedia:

```json
{
  "project": {},
  "dataset_summary": {},
  "class_distribution": [],
  "eda_summary": {},
  "model_comparison": [],
  "confusion_matrix": [],
  "forensic_summary": {},
  "feature_importance": [],
  "error_analysis": [],
  "advanced_summary": {},
  "advanced_models": [],
  "advanced_confusion": []
}
```

## Claim Rules

- Jangan menjadikan accuracy sebagai klaim utama karena normal class sangat kecil.
- Track A realistic harus dibedakan dari Track B/C controlled subset.
- Controlled subset boleh dipakai sebagai eksperimen pembanding, bukan bukti generalisasi dunia nyata.
- SHAP/global feature importance adalah bukti pendukung berbasis dataset, bukan bukti kausal atau jaminan deteksi sempurna.
- Setiap angka dashboard harus bisa dilacak ke `results/tables/`, `results/metrics/`, atau JSON generator.

## Verification

Sebelum merge/publish:

```bash
python3 scripts/generate_dashboard_data.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null
node --check dashboard/app.js
```

Jika tersedia, jalankan smoke test browser/mobile untuk memastikan tidak ada JavaScript error dan tidak ada horizontal overflow.
