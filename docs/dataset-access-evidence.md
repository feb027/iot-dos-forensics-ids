# Dataset Access Evidence — Fase 2

Tanggal audit: 2026-04-29

## Sumber resmi

- BoT-IoT UNSW: https://research.unsw.edu.au/projects/bot-iot-dataset
- GitHub dataset page: https://github.com/DrNickolaosKoroniotis/Bot-IoT-Dataset
- Dataset paper: Koroniotis et al., *Future Generation Computer Systems*, 2019.

Ringkasan sumber resmi:

- PCAP asli: 69.3 GB, lebih dari 72 juta record.
- CSV flow penuh: 16.7 GB.
- Subset 5%: 4 file, sekitar 1.07 GB, sekitar 3 juta record.
- Kategori serangan tersedia: DDoS, DoS, OS/Service Scan, Keylogging, Data Exfiltration.
- DDoS dan DoS dipisah lagi berdasarkan protokol.

## Working mirror yang diaudit

Karena dataset resmi besar dan disediakan lewat UNSW/SharePoint, Fase 2 memakai mirror publik Hugging Face untuk audit praktis awal:

- Mirror: https://huggingface.co/datasets/Mireu-Lab/UNSW-IoT
- File diaudit:
  - `Data/train.csv`
  - `Data/test.csv`
- Total file terunduh lokal: 461.384.981 bytes.
- Total baris diaudit: 3.668.522.

Catatan metodologis: sumber ilmiah tetap BoT-IoT UNSW. Mirror Hugging Face hanya dipakai sebagai akses praktis untuk inspeksi CSV train/test. Jika nanti hasil akhir ingin sangat konservatif, lampirkan catatan bahwa data operasional berasal dari mirror publik dan label/skema dicocokkan dengan struktur BoT-IoT.

## Exact Mirror Access Method

Hugging Face dataset metadata saat audit:

- Dataset ID: `Mireu-Lab/UNSW-IoT`
- Repository SHA/revision: `b33d67c3a80bc483dcf54fb2d492d9923f0dce40`
- Gated/private status: public and not gated at audit time, based on `references/raw-metadata/hf-unsw-iot-api-phase2.json`.

Download commands used for the audited local files:

```bash
mkdir -p data/raw/bot-iot-hf
curl -L --fail --retry 3 --retry-delay 3 \
  -o data/raw/bot-iot-hf/train.csv \
  https://huggingface.co/datasets/Mireu-Lab/UNSW-IoT/resolve/main/Data/train.csv
curl -L --fail --retry 3 --retry-delay 3 \
  -o data/raw/bot-iot-hf/test.csv \
  https://huggingface.co/datasets/Mireu-Lab/UNSW-IoT/resolve/main/Data/test.csv
sha256sum data/raw/bot-iot-hf/train.csv data/raw/bot-iot-hf/test.csv
python3 scripts/audit_botiot_dataset.py
```

For a pinned revision, replace `/resolve/main/` with `/resolve/b33d67c3a80bc483dcf54fb2d492d9923f0dce40/`.

## Bukti lokal

Raw data disimpan di path ter-*ignore*:

```text
data/raw/bot-iot-hf/train.csv
data/raw/bot-iot-hf/test.csv
```

Raw data tidak di-commit karena `.gitignore` melarang `data/raw/*`.

Checksum:

| Split | Bytes | SHA256 |
|---|---:|---|
| train | 369.103.929 | `047e577cd9c7f8f61d44ac170114497904c33091bf80d1dd5e682e353a69c15b` |
| test | 92.281.052 | `8617de2ac5d6ca4c2f77272c7409253a396f2a9e667c29c8e797ab9f57a1868e` |


Evidence kecil yang di-commit:

- `references/raw-sources/bot-iot-github-readme-phase2.md`
- `references/raw-sources/bot-iot-read-me-pdf-extract-phase2.md`
- `references/raw-metadata/hf-unsw-iot-api-phase2.json`
