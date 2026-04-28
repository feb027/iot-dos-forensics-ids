# Dashboard Specification

## Tujuan

Dashboard berfungsi sebagai visual evidence viewer untuk hasil analisis serangan DoS pada trafik IoT.

## Teknologi

- Static HTML/CSS/JS
- Data dari `dashboard/data/dashboard-data.json`
- Data JSON dihasilkan oleh `scripts/generate_dashboard_data.py`
- Target deployment: GitHub Pages

## Sections

1. Project Overview
2. Dataset Summary
3. Attack/Class Distribution
4. Model Performance
5. Confusion Matrix
6. Feature Importance
7. Forensic Interpretation
8. Conclusion and Links

## Design Direction

- Light/white academic style
- Clean cards
- Readable tables/charts
- No unnecessary dark theme
- No unsupported claims

## Data Contract Draft

```json
{
  "project": {},
  "dataset_summary": {},
  "class_distribution": [],
  "model_comparison": [],
  "confusion_matrix": {},
  "feature_importance": [],
  "forensic_notes": []
}
```
