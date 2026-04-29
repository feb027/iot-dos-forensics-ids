# Review Fase 3 EDA & Preprocessing

## Score
88

## Verdict
APPROVED

## Critical Issues
Tidak ada critical issue. Fase 3 cukup untuk melewati gate EDA & Preprocessing sebelum baseline modeling, dengan catatan follow-up penting di bawah perlu dibereskan saat masuk Fase 4.

## Important Issues
1. Logic `normal` saat ini memakai kondisi `attack in {"0", "0.0"} or category.lower() == "normal"` di `scripts/run_eda_preprocessing.py`. Untuk data yang sudah diaudit, hasilnya konsisten dengan Fase 2: Normal 370 train dan 107 test; DoS/DDoS 2.861.463 train dan 715.421 test; `other_attack` tetap terpisah. Namun sebelum modeling, sebaiknya tambahkan validasi eksplisit bahwa `attack=0` selalu `category=Normal` dan bahwa `category in {Reconnaissance, Theft}` tidak pernah masuk target normal. Ini mencegah label tidak konsisten diam-diam lolos jika dataset/sumber berubah.
2. Test `tests/test_run_eda_preprocessing.py` masih lebih dekat ke smoke test. Test sudah membuktikan script berjalan dan artifact utama dibuat, tetapi belum mengunci exact scope counts, exact excluded leakage columns, policy `other_attack_policy=exclude_from_binary_baseline`, dan track `C_balanced_controlled_1_to_2`. Untuk fase modeling, test tersebut perlu diperketat agar regresi preprocessing tidak lolos.
3. Notebook `notebooks/01_eda_preprocessing.ipynb` hanya wrapper sederhana dan memakai path `../scripts/run_eda_preprocessing.py`. Ini valid jika kernel berjalan dari folder `notebooks/`, tetapi bisa gagal jika kernel working directory adalah root repo. Karena script CLI adalah sumber reproducibility utama dan sudah lulus, ini tidak memblokir gate, tetapi notebook perlu dibuat lebih robust jika akan dijalankan/dinilai langsung.

## Minor Issues
1. `results/metrics/preprocessing_summary.json` memakai `generated_at_utc`, sehingga rerun script mengubah timestamp walaupun statistik sama. Ini wajar untuk artifact run, tetapi saat review/commit perlu sadar bahwa rerun akan menimbulkan diff.
2. `docs/phase3-method-notes.md` sudah relevan dan tidak overclaim, tetapi daftar Exa/SOTA masih berupa catatan cepat. Untuk paper final, sumber tersebut perlu dipetakan ke sitasi bibliografi yang valid; jangan langsung dijadikan klaim akademik tanpa metadata.
3. `scripts/generate_dashboard_data.py` hanya memasukkan track A dan B ke `eda_summary.dataset_plan`, sementara `preprocessing_dataset_plan.csv` juga memiliki track C. UI dashboard saat ini tidak menampilkan plan detail, jadi tidak ada klaim palsu, tetapi lebih konsisten jika JSON memuat semua track atau menjelaskan filter A/B.

## Evidence Checked
- Branch: `phase-3-eda-preprocessing`.
- File yang diperiksa: `scripts/run_eda_preprocessing.py`, `tests/test_run_eda_preprocessing.py`, `notebooks/01_eda_preprocessing.ipynb`, `docs/phase3-method-notes.md`, `reports/progress-3-eda-preprocessing.md`, `results/metrics/preprocessing_summary.json`, `results/tables/eda_binary_scope_distribution.csv`, `results/tables/eda_numeric_feature_summary.csv`, `results/tables/preprocessing_feature_plan.csv`, `results/tables/preprocessing_dataset_plan.csv`, `results/figures/eda_*.png`, `scripts/generate_dashboard_data.py`, `dashboard/data/dashboard-data.json`, `dashboard/app.js`, `dashboard/index.html`, `docs/project-control.md`, dan `docs/phase-gates.md`.
- Validasi CLI:
  - `python3 scripts/run_eda_preprocessing.py` lulus; output total rows 3.668.522.
  - `python3 -m py_compile scripts/*.py` lulus.
  - `python3 -m pytest -q` lulus: 5 passed.
  - `python3 -m json.tool results/metrics/preprocessing_summary.json` lulus.
  - `python3 -m json.tool dashboard/data/dashboard-data.json` lulus.
  - `python3 scripts/generate_dashboard_data.py` lulus.
  - `node --check dashboard/app.js` lulus.
- Konsistensi dengan audit Fase 2:
  - Total row Fase 3 sama dengan audit Fase 2: train 2.934.817, test 733.705, total 3.668.522.
  - Distribusi category/scope cocok dengan `results/tables/class_distribution.csv` dan `results/metrics/dataset_audit.json`.
  - `other_attack` tidak dipetakan ke normal: train 72.984 dan test 18.177 tetap dilaporkan sebagai scope terpisah.
  - DoS/DDoS dihitung dari `DoS + DDoS`: train 1.320.148 + 1.541.315 = 2.861.463; test 330.112 + 385.309 = 715.421.
- Leakage handling:
  - `preprocessing_feature_plan.csv` mengecualikan `attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, dan `dport`.
  - Candidate features hanya `proto`, `stddev`, `N_IN_Conn_P_SrcIP`, `min`, `state_number`, `mean`, `N_IN_Conn_P_DstIP`, `drate`, `srate`, dan `max`.
- Dataset besar:
  - Raw CSV ada di `data/raw/bot-iot-hf/` dan ter-ignore oleh `.gitignore`.
  - `git ls-files data/raw data/processed results/models` hanya menampilkan `.gitkeep`; raw dataset besar tidak terlacak git.
- Dashboard:
  - `dashboard/data/dashboard-data.json` menyimpan `model_comparison: []`, `confusion_matrix: {}`, dan `feature_importance: []`.
  - `dashboard/index.html` menyatakan hasil model/confusion matrix/feature importance akan ditambahkan setelah eksperimen tersedia. Tidak ada hasil modeling palsu.
- Figure artifact:
  - Semua `results/figures/eda_*.png` valid sebagai PNG dan bukan placeholder kosong berdasarkan metadata file.

## Required Fixes Before Next Phase
Tidak ada blocker yang harus menahan Fase 4. Sebelum atau pada commit awal Fase 4 baseline modeling, lakukan perbaikan berikut:

1. Tambahkan assertion/test label consistency untuk memastikan `attack=0` hanya normal, `DoS/DDoS` hanya masuk `dos_or_ddos`, dan `Reconnaissance/Theft` tetap `other_attack`.
2. Perketat test preprocessing agar memeriksa exact excluded columns, exact scope counts pada fixture, exact dataset-plan policy, dan keberadaan track A/B/C.
3. Buat notebook wrapper tidak bergantung pada working directory relatif yang rapuh, atau dokumentasikan bahwa notebook harus dijalankan dari folder `notebooks/`.
