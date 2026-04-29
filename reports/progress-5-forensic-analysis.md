# Progress 5 — Forensic Analysis

Tanggal: 2026-04-29

## Ringkasan

Fase 5 menjalankan analisis forensik dari baseline Fase 4. Output utama adalah feature importance, permutation importance, error analysis, contoh FP/FN, dan dashboard update.

Script utama:

```bash
source .venv/bin/activate
python scripts/run_forensic_analysis.py
python scripts/generate_dashboard_data.py
```

Notebook wrapper:

```text
notebooks/03_forensic_analysis.ipynb
```

## Output Artifact

Tabel:

- `results/tables/forensic_feature_importance.csv`
- `results/tables/forensic_error_analysis.csv`
- `results/tables/forensic_error_examples.csv`

Gambar:

- `results/figures/forensic_feature_importance.png`
- `results/figures/forensic_confusion_error_summary.png`

Summary JSON:

- `results/metrics/forensic_summary.json`

## Top Feature Groups

| Rank | Feature Group | Mean Normalized Importance | Interpretasi Forensik |
|---:|---|---:|---|
| 1 | `N_IN_Conn_P_DstIP` | 0.7406 | jumlah koneksi masuk per destination IP; nilai tinggi relevan untuk konsentrasi serangan ke target IoT |
| 2 | `N_IN_Conn_P_SrcIP` | 0.0760 | jumlah koneksi masuk per source IP; nilai tinggi relevan untuk pola flood dari sumber tertentu |
| 3 | `stddev` | 0.0517 | deviasi statistik flow; membantu membedakan kestabilan trafik normal dan variasi trafik serangan |
| 4 | `srate` | 0.0411 | source packet rate; nilai tinggi dapat menunjukkan pengiriman paket agresif dari sumber serangan |
| 5 | `mean` | 0.0218 | rata-rata statistik flow; dapat merepresentasikan intensitas umum trafik |
| 6 | `max` | 0.0198 | nilai maksimum statistik flow; membantu menangkap spike intensitas trafik |


## Error Analysis Selected Runs

| Item | Count |
|---|---:|
| False positive normal → attack | 2 |
| False negative attack → normal | 17 |
| FP/FN examples saved | 16 |

## Interpretasi Awal

- Fitur koneksi masuk per destination IP (`N_IN_Conn_P_DstIP`) menjadi sinyal dominan. Secara forensik, ini masuk akal karena DoS/DDoS cenderung menghasilkan konsentrasi koneksi ke target IoT.
- `N_IN_Conn_P_SrcIP` juga muncul sebagai fitur penting, mendukung pola flood dari sumber/pola sumber tertentu.
- Fitur statistik flow seperti `stddev`, `srate`, dan `mean` membantu membaca intensitas dan variasi trafik.
- False negative lebih berbahaya secara keamanan karena attack dapat lolos sebagai normal. Jumlah FN selected runs: 17.
- False positive juga perlu dibahas karena normal traffic bisa salah dianggap attack. Jumlah FP selected runs: 2.

## Limitation Statement

Hasil Fase 5 tidak boleh dibaca sebagai bukti deteksi sempurna. Dataset memiliki normal class sangat kecil dan audit sebelumnya mencatat risiko split-similarity. Karena itu klaim final harus berbasis feature importance, error analysis, dan limitation yang eksplisit.

## Keputusan

Fase 5 artifact siap untuk Codex technical/lecturer review:

- feature importance tersedia,
- permutation importance tersedia,
- FP/FN analysis tersedia,
- dashboard data sudah membaca forensic artifact,
- interpretasi dan limitasi sudah terdokumentasi.
