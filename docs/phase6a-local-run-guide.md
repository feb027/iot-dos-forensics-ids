# Fase 6A Local WSL Run Guide

Panduan ini untuk menjalankan advanced/SOTA modeling di PC lokal WSL2 (`Aqua`) dengan RAM WSL sekitar 13–14GB.

## 1. Posisi Repo

```bash
cd ~/iot-dos-forensics-ids
```

Jika repo belum ada:

```bash
git clone https://github.com/feb027/iot-dos-forensics-ids.git ~/iot-dos-forensics-ids
cd ~/iot-dos-forensics-ids
git checkout phase-6a-advanced-modeling
```

Jika repo sudah ada:

```bash
cd ~/iot-dos-forensics-ids
git fetch origin
git checkout phase-6a-advanced-modeling
git pull --ff-only origin phase-6a-advanced-modeling
```

## 2. Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika `python3 -m venv` gagal karena `ensurepip`/`python3.12-venv` belum tersedia dan tidak ingin memakai sudo, gunakan `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv venv .venv --python python3
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 3. Dataset

Runner membutuhkan cached CSV:

```text
data/raw/bot-iot-hf/train.csv
data/raw/bot-iot-hf/test.csv
```

Raw dataset tetap tidak boleh di-commit karena sudah di-ignore.

## 4. Smoke Test

```bash
source .venv/bin/activate
python scripts/run_advanced_modeling.py --tracks B_balanced_controlled_1_to_1 --models lightgbm --max-train-rows 20000 --max-test-rows 10000 --shap-sample 100
```

Expected:

- script selesai tanpa error,
- `results/tables/advanced_model_metrics.csv` terisi,
- `results/metrics/advanced_summary.json` valid.

## 5. Full Default Run

```bash
source .venv/bin/activate
python scripts/run_advanced_modeling.py --models all --tracks all --shap-sample 3000
python scripts/generate_dashboard_data.py
```

Default ini menjalankan:

- LightGBM pada Track A/B/C,
- XGBoost pada Track B/C,
- CatBoost pada Track B/C,
- sampled SHAP maksimal 3000 rows per run.

## 6. Heavier Optional Run

Jalankan hanya jika RAM aman:

```bash
source .venv/bin/activate
python scripts/run_advanced_modeling.py --models all --tracks all --include-heavy-track-a --shap-sample 3000
```

Ini menambahkan XGBoost/CatBoost pada Track A yang lebih berat.

## 7. Validasi Setelah Run

```bash
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 -m json.tool results/metrics/advanced_summary.json >/dev/null
python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null
node --check dashboard/app.js
```

## 8. Artifact yang Harus Ada

```text
results/tables/advanced_model_metrics.csv
results/tables/advanced_confusion_matrices.csv
results/tables/advanced_feature_importance.csv
results/tables/advanced_shap_summary.csv
results/tables/advanced_skipped_runs.csv
results/metrics/advanced_summary.json
results/figures/advanced_macro_f1_vs_baseline.png
results/figures/advanced_mcc_vs_baseline.png
results/figures/advanced_confusion_matrix_grid.png
results/figures/advanced_shap_summary.png
```

## 9. Troubleshooting

### RAM terlalu tinggi

Turunkan SHAP sample:

```bash
python scripts/run_advanced_modeling.py --models all --tracks all --shap-sample 1000
```

Atau jalankan controlled tracks dulu:

```bash
python scripts/run_advanced_modeling.py --tracks B_balanced_controlled_1_to_1 C_balanced_controlled_1_to_2 --models all --shap-sample 3000
```

### Dependency gagal

Upgrade pip lalu install ulang:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Jika LightGBM gagal dengan `libgomp.so.1`, WSL belum punya OpenMP runtime. Tanpa sudo, gunakan library dari wheel XGBoost/scikit-learn:

```bash
GOMP=$(find .venv/lib/python*/site-packages/xgboost.libs .venv/lib/python*/site-packages/scikit_learn.libs -name 'libgomp*.so*' | head -1)
ln -sf "$PWD/$GOMP" .venv/lib/libgomp.so.1
export LD_LIBRARY_PATH="$PWD/.venv/lib:${LD_LIBRARY_PATH:-}"
```

Tambahkan `export LD_LIBRARY_PATH="$PWD/.venv/lib:${LD_LIBRARY_PATH:-}"` sebelum menjalankan runner jika memakai workaround ini.

### Track A berat

Default sudah hanya menjalankan LightGBM pada Track A. Jangan pakai `--include-heavy-track-a` kecuali RAM aman.
