# Progress 2 — Dataset Audit

Tanggal: 2026-04-29

## Ringkasan

Fase 2 melakukan audit awal dataset BoT-IoT untuk memastikan data yang akan dipakai pada eksperimen tidak langsung masuk ke tahap modeling tanpa memahami label, fitur, ukuran, imbalance, dan risiko leakage.

Audit dilakukan menggunakan script reproducible:

```bash
python3 scripts/audit_botiot_dataset.py
```

Output utama:

- `results/metrics/dataset_audit.json`
- `results/tables/dataset_files.csv`
- `results/tables/class_distribution.csv`
- `results/tables/column_profile.csv`
- `results/tables/split_leakage_checks.csv`

## Sumber Dataset

Sumber ilmiah utama tetap BoT-IoT UNSW. Karena file resmi sangat besar, audit praktis memakai mirror Hugging Face `Mireu-Lab/UNSW-IoT` yang menyediakan `train.csv` dan `test.csv`. Raw CSV disimpan di `data/raw/bot-iot-hf/` dan tidak di-commit.

## Hasil Audit

| Split | Rows | Columns | Exact duplicates | Duplicate pkSeqID |
|---|---:|---:|---:|---:|
| train | 2.934.817 | 19 | 0 | 0 |
| test | 733.705 | 19 | 0 | 0 |


Total baris yang diaudit: **3.668.522**.

Kolom label:

- `attack`
- `category`
- `subcategory`

Kolom yang direkomendasikan untuk dikeluarkan dari baseline:

```text
attack, category, daddr, dport, pkSeqID, saddr, seq, sport, subcategory
```

Kolom fitur kandidat:

```text
proto, stddev, N_IN_Conn_P_SrcIP, min, state_number, mean, N_IN_Conn_P_DstIP, drate, srate, max
```

## Temuan Utama

1. **DoS/DDoS tersedia dan dominan.**  
   Kategori `DoS` dan `DDoS` tersedia di train dan test, sehingga judul masih sesuai.

2. **Normal class sangat kecil.**  
   Normal hanya 370 baris di train dan 107 baris di test. Ini risiko besar untuk binary classification normal vs DoS/DDoS.

3. **Tidak ada overlap ID dan tidak ada exact duplicate row antar split.**  
   `pkSeqID overlap train/test = 0` dan `Exact full-row overlap train/test = 0`.

4. **Ada kemiripan fitur agregat antar split.**  
   Model-feature signature overlap train/test setelah ID, network identifier, dan label dikeluarkan = **327.338**. Ini harus ditulis sebagai risiko split similarity, bukan langsung dianggap fatal.

5. **Network identifier harus dikeluarkan.**  
   `saddr`, `sport`, `daddr`, dan `dport` berisiko membuat model menghafal topology lab.

6. **Duplicate signature di dalam split juga tinggi.**  
   Setelah identifier, network identifier, dan label dikeluarkan, duplicate model-feature rows adalah 1.487.901 pada train dan 202.630 pada test. Ini perlu ditulis sebagai risiko sampling/evaluasi di Fase 3.

## Keputusan untuk Fase 3

Fase 3 boleh lanjut ke EDA dan preprocessing dengan syarat:

- Binary target utama: `normal` vs `dos_or_ddos`.
- `other_attack` tidak dipakai untuk baseline binary utama; boleh dipakai di analisis opsional.
- Baseline tidak memakai `attack`, `category`, `subcategory`, `pkSeqID`, `seq`, `saddr`, `sport`, `daddr`, `dport`.
- Evaluasi tidak boleh mengandalkan accuracy saja.
- Wajib laporkan imbalance normal class dan potensi split similarity.

## Status

Fase 2 secara artifact sudah siap untuk review. Belum boleh masuk Fase 3 sampai Codex review menyatakan APPROVED atau isu kritisnya diperbaiki.
