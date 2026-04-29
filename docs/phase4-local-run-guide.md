# Fase 4 Local Run Guide — Baseline Modeling

## Environment

Direkomendasikan menjalankan dari WSL2/Linux atau Colab. Di repo lokal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Catatan VPS/CPU lama: `requirements.txt` mem-pin `numpy==2.1.0` karena wheel NumPy terbaru dapat gagal dengan error `X86_V2` pada CPU tanpa AVX2.

## Run Smoke Test

```bash
source .venv/bin/activate
python scripts/run_baseline_modeling.py --tracks B_balanced_controlled_1_to_1 --models gaussian_nb decision_tree --max-train-rows 20000 --max-test-rows 8000
```

## Run Full Fase 4

```bash
source .venv/bin/activate
python scripts/run_baseline_modeling.py
python scripts/generate_dashboard_data.py
```

## Expected Outputs

- `results/tables/baseline_model_metrics.csv`
- `results/tables/baseline_confusion_matrices.csv`
- `results/tables/baseline_dataset_tracks.csv`
- `results/metrics/baseline_summary.json`
- `results/figures/baseline_macro_f1_comparison.png`
- `results/figures/baseline_mcc_comparison.png`
- `results/figures/baseline_confusion_matrix_grid.png`

## Interpretation Rule

Jangan memakai accuracy sebagai klaim utama. Gunakan macro F1, MCC, balanced accuracy, recall normal, recall attack, dan confusion matrix.
