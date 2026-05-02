# IoT DoS Forensics IDS

Repositori ini berisi proyek UAS individu mata kuliah Internet of Things Semester 6.

## Judul

**Sistem Analisis Serangan DoS pada Arsitektur IoT Berbasis Machine Learning dan Network Forensics Menggunakan Dataset BoT-IoT**

## Ringkasan

Proyek ini menganalisis trafik IoT normal dan serangan DoS/DDoS menggunakan dataset BoT-IoT. Fokus utamanya adalah klasifikasi biner normal vs DoS/DDoS, evaluasi model *machine learning*, interpretasi fitur trafik sebagai artefak *network forensics*, serta visualisasi hasil melalui dashboard statis dan SOC *replay* edukatif.

Sistem yang dibuat adalah prototipe akademik berbasis dataset. Proyek ini tidak melakukan serangan terhadap perangkat IoT asli, tidak menjalankan PCAP *replay* aktual, dan tidak diklaim sebagai IDS produksi *real-time*.

## Dataset

- Dataset utama: BoT-IoT, UNSW  
  https://research.unsw.edu.au/projects/bot-iot-dataset
- Dataset alternatif untuk penelitian lanjutan: RT-IoT2022, UCI Machine Learning Repository  
  https://archive.ics.uci.edu/dataset/942/rt-iot2022

Dataset mentah tidak disimpan di repositori karena ukurannya besar. Repositori hanya menyimpan kode, notebook, ringkasan hasil, tabel, grafik, dan data dashboard yang aman untuk dibagikan.

## Struktur Repositori

```text
backend/      Backend demo SOC replay berbasis FastAPI
dashboard/    Dashboard statis dan halaman SOC replay edukatif
data/         Folder lokal untuk dataset mentah/proses, tidak di-commit
notebooks/    Notebook EDA, preprocessing, modeling, dan analisis forensik
references/   Literatur, BibTeX, dan metadata sumber
reports/      Draft naskah ilmiah, daftar pustaka, dan lampiran
results/      Tabel, metrik, dan gambar hasil eksperimen
scripts/      Script reproducible untuk audit, preprocessing, modeling, dan dashboard
tests/        Unit test untuk script penting
```

## Naskah Ilmiah

Bagian naskah tersedia pada folder `reports/`:

- `reports/manuscript-draft-bab1.md`
- `reports/manuscript-draft-bab2.md`
- `reports/manuscript-draft-bab3.md`
- `reports/manuscript-draft-bab4.md`
- `reports/manuscript-draft-bab5.md`
- `reports/manuscript-daftar-pustaka.md`
- `reports/manuscript-lampiran.md`

## Dashboard

- Dashboard GitHub Pages: https://feb027.github.io/iot-dos-forensics-ids/
- SOC replay edukatif: https://iot.aquarise.my.id/soc-demo/demo.html

Dashboard membaca data dari folder `dashboard/data/` dan artefak hasil pada folder `results/`. Visualisasi dashboard digunakan untuk mendukung penjelasan hasil eksperimen, bukan sebagai sistem keamanan operasional.

## Reproduksi Ringkas

Siapkan Python dan dependensi:

```bash
pip install -r requirements.txt
```

Jalankan pemeriksaan dan pembuatan data dashboard:

```bash
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 scripts/generate_dashboard_data.py
```

Menjalankan dashboard lokal:

```bash
python3 -m http.server 8000 -d dashboard
```

Lalu buka:

```text
http://localhost:8000/
http://localhost:8000/demo.html
```

## Artefak Utama

Beberapa artefak penting:

- `results/metrics/preprocessing_summary.json`
- `results/metrics/baseline_summary.json`
- `results/metrics/advanced_summary.json`
- `results/metrics/forensic_summary.json`
- `results/tables/baseline_dataset_tracks.csv`
- `results/tables/advanced_model_metrics.csv`
- `results/tables/advanced_confusion_matrices.csv`
- `results/tables/advanced_shap_summary.csv`
- `results/figures/advanced_macro_f1_vs_baseline.png`
- `results/figures/advanced_confusion_matrix_grid.png`
- `results/figures/advanced_shap_summary.png`

## Batasan

- Analisis hanya memakai dataset dan fitur trafik yang tersedia.
- Fokus eksperimen adalah normal vs DoS/DDoS.
- Hasil tidak diklaim berlaku universal untuk semua jaringan IoT.
- Dashboard dan SOC replay bersifat edukatif.
- Tidak ada raw dataset, kredensial, file PCAP besar, atau model besar yang disimpan di repositori.
