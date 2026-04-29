# Review Fase 6B — Interactive AI SOC Demo

**Skor:** 88/100  
**Verdict:** APPROVED

## Ringkasan Penilaian

Implementasi Fase 6B sudah relevan dengan tema proyek **Sistem Analisis Serangan DoS pada Arsitektur IoT** karena demo menampilkan alur SOC interaktif untuk trafik DoS/DDoS IoT, memakai fitur flow BoT-IoT, memuat risiko FP/FN, dan menjaga batas klaim bahwa sistem adalah prototipe edukatif berbasis artifact, bukan production real-time IDS. Struktur frontend sudah modular, backend FastAPI cukup aman untuk konteks akademik, dan catatan deployment sudah menjelaskan PM2 serta Caddy runtime route yang belum persisten.

Review ini menyetujui fase untuk lanjut, tetapi terdapat beberapa perbaikan penting agar klaim demo tetap benar-benar artifact-first saat digunakan dalam presentasi dan naskah akhir.

## Kesesuaian terhadap Kriteria

### 1. Kesesuaian dengan IoT Security, IDS, dan Digital Forensics

**Status:** Baik.

- Demo memusatkan analisis pada trafik DoS/DDoS IoT, fitur koneksi, packet rate, proto, dan statistik flow.
- Report SOC memasukkan evidence chain, risiko false positive/false negative, rekomendasi mitigasi, serta batasan attribution.
- Narasi akademik sudah konsisten: hasil dibaca sebagai interpretasi artifact eksperimen BoT-IoT, bukan klaim deteksi dunia nyata.

### 2. Modularitas dan Skalabilitas Frontend

**Status:** Baik.

Frontend tidak dibangun sebagai satu file monolitik. Pemisahan sudah jelas:

- Entry demo: `dashboard/demo.html` dan `dashboard/scripts/demo.js`.
- Modul data/API: `dashboard/scripts/demo/api-client.js`, `scenario-store.js`.
- Modul logika demo: `what-if-engine.js`, `soc-narrative.js`.
- Komponen tampilan: `components/analyst-report.js`, `timeline.js`, `evidence-bar.js`.
- Utilitas umum: `core/dom.js`, `core/format.js`, `core/data-loader.js`.
- CSS juga sudah dipisah ke `base.css`, `layout.css`, `components.css`, dan `demo.css`.

Struktur ini cukup siap untuk penambahan fitur seperti scenario filter, export report, atau mode pembanding model tanpa membongkar seluruh kode.

### 3. Keamanan Akademik Backend FastAPI

**Status:** Cukup baik, dengan catatan penting.

Hal positif:

- Endpoint `POST /api/predict` memanggil validasi fitur dan menolak leakage/label columns melalui `LEAKAGE_COLUMNS`.
- Endpoint `POST /api/flow/analyze` juga menolak kolom seperti `attack`, `category`, `subcategory`, `pkSeqID`, `saddr`, `daddr`, dan port sebelum prediksi.
- Unknown feature columns ditolak sehingga input tidak bebas memasukkan fitur yang tidak didukung.
- Response dan report mencantumkan batasan bahwa output bukan production IDS dan bukan bukti attribution dunia nyata.
- `/api/chat` bersifat deterministik dan hanya menjawab topik yang tersedia pada artifact demo.

Catatan:

- `POST /api/soc/analyze` menerima `prediction` dari client. Walaupun fitur divalidasi, report dapat dibangun dari prediksi yang dikirim client tanpa pemeriksaan konsistensi terhadap hasil `predict(features)`. Untuk demo akademik ini belum menjadi isu kritis, tetapi agar lebih aman sebaiknya backend selalu menghitung ulang prediksi server-side atau minimal memverifikasi bahwa prediksi client sama dengan hasil server.
- CORS `allow_origins=["*"]` masih dapat diterima untuk demo publik tanpa credential, tetapi perlu diberi catatan bahwa ini bukan konfigurasi production.

### 4. Demo Data dan Grounding Artifact

**Status:** Cukup baik, tetapi perlu penguatan.

Hal positif:

- Generator `scripts/generate_demo_scenarios.py` membaca artifact yang sudah ada, antara lain `results/tables/forensic_error_examples.csv`, `results/tables/advanced_shap_summary.csv`, `results/tables/forensic_feature_importance.csv`, dan `results/metrics/advanced_summary.json`.
- Skenario FN dan FP berasal dari baris artifact forensic error examples.
- Konteks metrik Track A LightGBM (`macro_f1`, `mcc`, `fp`, `fn`) diambil dari `advanced_summary.json`, bukan diketik manual di JSON akhir.
- File output mencantumkan `sources` dan `claim_boundary`.

Catatan penting:

- Dua skenario `simulated-high-confidence-dos` dan `simulated-low-risk-normal` dibuat dari nilai fitur hard-coded di script, walaupun diberi `scenario_type: constructed_from_artifact_patterns`. Ini masih dapat dipakai sebagai simulasi edukatif, tetapi jangan disebut sebagai replay aktual atau TP/TN artifact kecuali nilainya diambil dari baris nyata hasil evaluasi.
- Nama “Replay” pada skenario simulasi berpotensi menimbulkan kesan bahwa flow tersebut benar-benar berasal dari artifact row. Sebaiknya diganti menjadi “Simulated Pattern” atau generator mengambil contoh TP/TN nyata dari artifact evaluasi.
- Weight dan denominator surrogate IDS di backend/frontend bersifat rule-based manual. Karena itu istilah “artifact-grounded surrogate IDS” masih perlu dijelaskan sebagai heuristic demonstrasi berbasis interpretasi artifact, bukan model LightGBM/XGBoost aktual.

### 5. Deployment, Caddy, dan PM2

**Status:** Baik.

- Tersedia `deploy/ecosystem.soc-demo.config.cjs` untuk PM2 backend pada port 8766.
- Tersedia `deploy/Caddyfile.soc-demo-snippet` untuk route `/soc-demo/*` dan `/soc-demo/api/*`.
- Progress report menjelaskan bahwa route Caddy saat ini diterapkan dengan runtime `caddy reload --config /tmp/Caddyfile.iot-soc-demo`, bukan edit persisten `/etc/caddy/Caddyfile`, karena keterbatasan akses sudo. Catatan ini sudah memenuhi kriteria review.

### 6. Validasi yang Dijalankan

Validasi dijalankan dari `/home/aqua/iot-dos-forensics-ids`.

| Pemeriksaan | Hasil |
|---|---|
| `python3 scripts/generate_demo_scenarios.py` | Lulus; menulis ulang demo JSON dan menghasilkan `scenarios=4`. Perubahan timestamp/output kemudian dikembalikan agar review ini tidak memodifikasi file lain. |
| `python3 -m py_compile scripts/*.py` | Lulus. |
| `python3 -m compileall -q backend` | Lulus. |
| `python3 -m pytest -q` | Lulus, `25 passed in 3.30s`. |
| `node --check dashboard/scripts/demo.js` | Lulus. |
| `node --check dashboard/scripts/core/*.js dashboard/scripts/components/*.js dashboard/scripts/demo/*.js` | Lulus. |

Keterbatasan validasi: review ini tidak melakukan verifikasi browser interaktif/visual secara langsung. Pemeriksaan yang dilakukan terbatas pada inspeksi kode, artifact, validasi sintaks, unit test, dan konsistensi dokumentasi deployment.

## Critical Issues

Tidak ada critical issue yang menghalangi fase ini untuk diterima.

## Important Issues

1. **Prediksi pada `/api/soc/analyze` masih bisa dipercayakan ke client.**  
   Backend sebaiknya menghitung ulang prediksi dari `features` atau memverifikasi kesamaan prediksi client sebelum membuat SOC report. Ini penting agar report tetap grounded ke logika server dan tidak mudah menjadi report atas payload prediksi arbitrer.

2. **Skenario simulasi hard-coded perlu diperjelas atau diganti dengan artifact-derived rows.**  
   Skenario high-confidence dan low-risk saat ini dibuat manual dari pola artifact. Untuk menjaga prinsip tidak membuat data/hasil eksperimen yang berpotensi disalahpahami, generator sebaiknya mengambil TP/TN nyata dari artifact evaluasi jika tersedia. Jika tidak tersedia, label UI dan JSON harus eksplisit menyebut “simulasi edukatif”, bukan “replay”.

3. **Surrogate scoring perlu dokumentasi batasan yang lebih eksplisit.**  
   Bobot dan denominator pada `predictor.py` dan `what-if-engine.js` tampak sebagai heuristic manual. Ini boleh untuk demo, tetapi harus dinyatakan jelas di report/progress/manuscript bahwa risk score bukan output model LightGBM aktual dan bukan metrik performa baru.

## Minor Issues

1. Endpoint `POST /api/flow/analyze` hanya membaca baris pertama CSV. Ini cukup untuk demo, tetapi UI/API documentation sebaiknya menyebut bahwa mode ini single-flow, bukan batch analysis.
2. Konfigurasi CORS wildcard dapat dipertahankan untuk demo publik tanpa credential, tetapi sebaiknya diberi komentar sebagai konfigurasi non-production.
3. API base path di frontend (`/soc-demo/api` atau `/api`) masih hard-coded. Untuk skalabilitas deployment, dapat dipindah ke konfigurasi kecil atau `data-*` attribute di HTML.
4. Test sudah baik, tetapi belum menguji `/api/soc/analyze` terhadap prediksi client yang tidak konsisten dengan fitur.

## Required Fixes

Sebelum fase ini dipakai sebagai bahan presentasi/naskah final, lakukan perbaikan berikut:

1. Ubah `POST /api/soc/analyze` agar prediksi dihitung ulang server-side, atau tambahkan validasi konsistensi antara `request.prediction` dan `predict(request.features)`.
2. Ganti skenario `simulated-high-confidence-dos` dan `simulated-low-risk-normal` menjadi contoh TP/TN nyata dari artifact jika tersedia; jika tidak, ubah penamaan dan narasi agar jelas sebagai simulasi edukatif, bukan replay artifact.
3. Tambahkan catatan eksplisit di dokumentasi bahwa risk score surrogate adalah heuristic demonstrasi berbasis fitur penting/SHAP dan bukan skor probabilitas model produksi.
4. Dokumentasikan bahwa `/api/flow/analyze` adalah single-row flow analyzer.

## Keputusan Review

Fase 6B dinilai **APPROVED** karena sudah memenuhi tujuan utama demo interaktif: modular, relevan dengan IoT DoS/IDS/forensics, memiliki backend FastAPI yang menolak leakage columns, berbasis artifact, serta dilengkapi catatan deployment PM2/Caddy. Perbaikan di atas diperlukan untuk memperkuat integritas akademik dan mencegah pembaca mengira skenario simulasi atau surrogate score sebagai hasil eksperimen/model produksi.
